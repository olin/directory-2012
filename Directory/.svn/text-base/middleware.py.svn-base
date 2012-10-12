import re

from django.http import HttpResponseRedirect
from django.conf import settings
from Directory.models import *

class UrlRedirectMiddleware:
    """
    This middleware lets you match a specific url and redirect the request to a
    new url.

    You keep a tuple of url regex pattern/url redirect tuples on your site
    settings, example:

    URL_REDIRECTS = (
        (r'www\.example\.com/hello/$', 'http://hello.example.com/'),
        (r'www\.example2\.com/$', 'http://www.example.com/example2/'),
    )

    """
    def process_request(self, request):
        redirect_url = '/createuser/'
        if request.user.is_authenticated():
            if not UserProfile.objects.filter(user=request.user).exists():
                if redirect_url != request.path:
                    return HttpResponseRedirect(redirect_url)

