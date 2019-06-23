from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="portal/home.html"), name="home"),
    path("businesses/<int:pk>", views.BusinessView.as_view(), name="business"),
    # UI WIP to be integrated in django templates
    path(
        "portal-test",
        TemplateView.as_view(template_name="portal/portal.html"),
        name="portal",
    ),
]
