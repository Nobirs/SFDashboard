from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView

from .models import Announcement, Resp
from .tasks import inform_about_response, accept_user_response
from .forms import AnnouncementForm, RespForm
from .filters import RespFilter


# Create your views here.
class CreateAnnouncementView(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'desk/create_announcement.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_announcement'] = 'active'
        return context

    def form_valid(self, form):
        announcement = form.save(commit=False)
        announcement.author = self.request.user
        announcement.save()
        return HttpResponseRedirect(announcement.get_absolute_url())


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'desk/announcement_detail.html'
    context_object_name = 'announcement'


# TODO: Edit post can only author of that post
class AnnouncementEditView(PermissionRequiredMixin, UpdateView):
    permission_required = ('desk.change_announcement')
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'desk/edit_announcement.html'
    context_object_name = 'announcement'

    def form_valid(self, form):
        announcement = form.save(commit=False)
        categories = form.data.get('category', default=None)
        if categories is None:
            form.data['category'] = self.object.category.set()
        return super().form_valid(form)


class AnnouncementsView(ListView):
    model = Announcement
    template_name = 'desk/announcements.html'
    ordering = '-creation_date'
    context_object_name = 'announcements'

    def get_queryset(self):
        announcements = Announcement.objects.all().order_by('-creation_date')
        first_set = announcements[::2]
        second_set = announcements[1::2]
        if len(first_set) < len(second_set):
            first_set += [None]
        elif len(second_set) < len(first_set):
            second_set += [None]
        return list(zip(first_set, second_set))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['announcements_indexes'] = self.get_queryset()
        context['resp_form'] = RespForm()
        context['latest'] = 'active'
        print(f"Kwargs: {kwargs}")
        #context['is_author'] = self.request.user ==
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        content = self.request.POST['content']
        announcement_id = kwargs['pk']
        print(f"ID: {announcement_id}")
        new_resp = Resp(content=content, author=user, announcement=Announcement.objects.get(id=announcement_id))
        new_resp.save()

        inform_about_response.delay(resp_user=user.username, resp_content=content, announcement_id=announcement_id)
        print("In post method...")
        print(f"User: {user}\nContent: {content}")
        print(f"URL from: {request.path}\n path: {request.build_absolute_uri()}")
        print(f"announcement id: {announcement_id}")
        # TODO: Find the way to not use absolute url
        return redirect('/announcement/latest/#')


class UserRespView(LoginRequiredMixin, ListView):
    model = Resp
    template_name = 'desk/user_responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = self.request.user.resp_set.all()
        self.filterset = RespFilter(self.request.GET, queryset=queryset, request=self.request)
        return self.filterset.qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filterset'] = self.filterset
        context['user_announcements'] = Announcement.objects.filter(author=self.request.user)
        context['my_responses'] = 'active'
        print(context['user_announcements'])
        return context


class DeleteRespView(PermissionRequiredMixin, DeleteView):
    permission_required = ('desk.delete_resp')
    model = Resp
    template_name = 'desk/resp_delete.html'
    raise_exception = True
    success_url = reverse_lazy('latest')
    context_object_name = 'resp'

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['resp'] =


@permission_required('desk.change_resp')
def accept_response(request, pk):
    resp = Resp.objects.get(pk=pk)
    if not resp.accepted:
        resp.accepted = True
        resp.save()
        accept_user_response.delay(resp_id=resp.id, announcement_title=resp.announcement.title)
    return redirect('user_resp', pk=request.user.id)