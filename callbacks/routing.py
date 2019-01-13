from django.conf.urls import url

from .consumers import WebhookConsumer

websocket_urlpatterns = [url(r"^ws/callback/(?P<uuid>[^/]+)/$", WebhookConsumer)]
