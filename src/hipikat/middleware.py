"""
TODOLipsum
"""
import re
from django.conf import settings


# TODO: Fill out the rest of the debug middleware stub methods.
class DebugOuterMiddleware(object):
    """Debug-mode middleware on the 'outermost' middleware layer."""

    def process_request(self, request):
        """Debug process_request, called before all other process_request middleware."""
        try:
            # Update django-hosts's PARENT_HOST while in development
            requested_host = request.META['HTTP_HOST']
            host_re_end = ':' if ':' in requested_host else '$'
            for allowed_host in settings.ALLOWED_HOSTS:
                match = re.search(re.escape(allowed_host) + host_re_end, requested_host)
                if match:
                    start = match.start() + 1 if allowed_host[0] == '.' else match.start()
                    setattr(settings, 'PARENT_HOST', requested_host[start:])
        except Exception as e:
            pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Debug process_view, called before all other process_view middleware."""


class DebugInnerMiddleware(object):
    """Debug-mode middleware on the 'innermost' middleware layer."""

    def process_request(self, request):
        """Debug process_request, called after all other process_request middleware."""
        #import pdb; pdb.set_trace()

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Debug process_view, called after all other process_view middleware."""
