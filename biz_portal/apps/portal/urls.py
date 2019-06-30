from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"businesses", views.BusinessViewSet)

urlpatterns = [
    path("", TemplateView.as_view(template_name="portal/home.html"), name="home"),
    path("businesses/", views.BusinessListView.as_view(), name="business_list"),
    path("businesses/<int:pk>", views.BusinessDetailView.as_view(), name="business_detail"),

    # API
    path(r"api/v1/", include(router.urls)),

    # UI WIP to be integrated in django templates
    path(
        "portal-test",
        TemplateView.as_view(template_name="portal/portal.html"),
        name="portal",
    ),
]
