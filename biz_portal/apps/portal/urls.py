from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"businesses", views.BusinessViewSet)

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("businesses/", views.BusinessListView.as_view(), name="business_list"),
    path(
        "businesses/<int:pk>",
        views.BusinessDetailView.as_view(),
        name="business_detail",
    ),
    # API
    path(r"api/v1/", include((router.urls, "portal"), namespace="api")),
    # UI WIP to be integrated in django templates
    path("portal-test", views.DevView.as_view(), name="portal"),
]
