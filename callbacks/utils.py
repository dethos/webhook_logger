from django.http import HttpRequest


def get_ip_address(request: HttpRequest) -> str:
    forwarded = request.META.get("X-FORWARDED-FOR")
    if forwarded:
        return forwarded.split(",")[0]
    else:
        return request.META.get("REMOTE_ADDR")
