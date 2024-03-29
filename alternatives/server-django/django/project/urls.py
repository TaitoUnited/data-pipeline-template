"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('example/', include('example.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from infra import views as infraViews

urlpatterns = [
    path("example/sales/", include("example.urls")),
    path("admin/", admin.site.urls),
    path("config/", infraViews.get_config, name="get_config"),
    path("uptimez/", infraViews.get_uptimez, name="get_uptimez"),
    path("healthz/", infraViews.get_healthz, name="get_healthz"),
]
