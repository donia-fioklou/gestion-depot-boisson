from django.urls import path
from .views import change_password, UserPermissionsView

urlpatterns = [
    path('change-password/', change_password, name='change-password'),
    path('api/user-permissions/', UserPermissionsView.as_view(), name='user-permissions'),
]