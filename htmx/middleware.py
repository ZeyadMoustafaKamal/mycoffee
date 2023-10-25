from django_htmx.middleware import (
    HtmxMiddleware as BaseHTMXMiddeware,
    HtmxDetails as BaseHTMXDetails
)

class HTMXMiddleware(BaseHTMXMiddeware):
    def __call__(self, request):
        if not self._is_coroutine:
            request.htmx = HTMXDetails(request)
            return self.get_response(request)
        return super().__call__()

class HTMXDetails(BaseHTMXDetails):
    def __bool__(self):
        if self._get_header_value("HX-Fullpage") == "true":
            return False
        return super().__bool__()
