"""webhook_logger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from callbacks.views import HomeView, CheckView, CallbackView

urlpatterns = [
    path("check", CheckView.as_view(), name="callback-check"),
    path("<uuid>", CallbackView.as_view(), name="callback-submit"),
    path("<uuid>/<status>", CallbackView.as_view(), name="callback-submit-response"),
    path("", HomeView.as_view(), name="callback-home"),
]
