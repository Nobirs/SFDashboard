import django_filters
from django_filters import FilterSet, ModelChoiceFilter


from .models import Resp, Announcement


class RespFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        self.announcement = ModelChoiceFilter(queryset=Announcement.objects.filter(author=kwargs['request'].user))
        super().__init__(*args, **kwargs)

    class Meta:
        model = Resp
        fields = ['announcement']