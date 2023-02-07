from django.urls import path, include

from .views import CreateAnnouncementView, AnnouncementDetailView, AnnouncementEditView, AnnouncementsView, UserRespView, DeleteRespView, accept_response


urlpatterns = [
    path('', AnnouncementsView.as_view(), name='home_page'),
    path('new/', CreateAnnouncementView.as_view(), name='new_announcement'),
    path('<int:pk>/', AnnouncementDetailView.as_view(), name='announcement'),
    path('<int:pk>/update/', AnnouncementEditView.as_view(), name='update'),
    path('latest/', AnnouncementsView.as_view(), name='latest'),
    path('latest/<int:pk>/', AnnouncementsView.as_view(), name='latest_response'),
    path('user/<int:pk>/resp/', UserRespView.as_view(), name='user_resp'),
    path('user/resp/<int:pk>/delete/', DeleteRespView.as_view(), name='delete_resp'),
    path('user/resp/<int:pk>/accept/', accept_response, name='accept_resp'),
]