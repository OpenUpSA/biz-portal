from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("portal-test", TemplateView.as_view(template_name="pages/portal.html"), name="portal"),
]
