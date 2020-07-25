from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("auth/",include('rest_framework.urls',namespace="rest_framework")),
    path('get-token/', obtain_auth_token),
    path("content/<pk>/",views.DetailView.as_view(),name="get_delete_update_content"),
    path("content/",views.CreateView.as_view(),name="get_post_content")
]
