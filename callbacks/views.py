from uuid import uuid4

from django.views.generic import RedirectView, TemplateView, View
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.utils import timezone

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class HomeView(RedirectView):
    """Initial page, just sends the visitor to an unique url"""

    def get_redirect_url(self):
        uuid = str(uuid4())
        return f"{reverse_lazy('callback-check')}?cb={uuid}"


class CheckView(TemplateView):
    """Renders the page where users can monitor webhook

    The activity shown is filtered by the unique ID assigned to
    the visitor
    """

    template_name = "callbacks/check.html"


class CallbackView(View):
    """Webhook receiver view

    This view receives any HTTP request, collects all the information
    possible about the request, then sends it through the proper channel
    """

    def dispatch(self, request, *args, **kwargs):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            kwargs["uuid"], {"type": "new_request", "data": self.request_data(request)}
        )
        return HttpResponse()

    def request_data(self, request):
        return {
            "method": request.method,
            "query_params": request.GET,
            "body": request.POST,
            "headers": request.META,
            "received_at": timezone.now().isoformat(),
        }
