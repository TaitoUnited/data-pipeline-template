from django.urls import path
from . import views

urlpatterns = [
    path("", views.sales, name="sales"),
    path("<str:id>", views.sale, name="sale"),
]
