from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.login_page, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_page, name="logout"),
]
