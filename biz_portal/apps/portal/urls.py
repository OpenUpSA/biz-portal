from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"businesses", views.BusinessViewSet)

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "municipality/",
        views.MunicipalityDetailView.as_view(),
        name="municipality_detail",
    ),
    path("businesses/", views.BusinessListView.as_view(), name="business_list"),
    path(
        "businesses/<int:pk>",
        views.BusinessDetailView.as_view(),
        name="business_detail",
    ),
    path(
        "businesses/<int:pk>/download",
        views.BusinessDetailPDFView.as_view(),
        name="business_detail_pdf",
    ),
    # API
    path(r"api/v1/", include((router.urls, "portal"), namespace="api")),
]
