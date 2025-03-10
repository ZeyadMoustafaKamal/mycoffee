from django_htmx.middleware import HtmxDetails as BaseHTMXDetails
from django_htmx.middleware import HtmxMiddleware as BaseHTMXMiddeware


class HTMXMiddleware(BaseHTMXMiddeware):
    def __call__(self, request):
        if not self.async_mode:
            request.htmx = HTMXDetails(request)
            return self.get_response(request)
        return super().__call__()


class HTMXDetails(BaseHTMXDetails):
    def __bool__(self):
        if self._get_header_value("HX-Fullpage") == "true":
            return False
        return super().__bool__()
