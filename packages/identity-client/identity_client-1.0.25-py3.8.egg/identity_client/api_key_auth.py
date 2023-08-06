from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import authentication

from netaddr import IPAddress


class ApiKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        ALLOWED_SUBNETS = getattr(settings, "API_KEY_ALLOWED_SUBNET", None)
        if not ALLOWED_SUBNETS:
            return None

        client_ip = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
        if not client_ip:
            client_ip = request.META["REMOTE_ADDR"]

        auto_user = User.objects.get(email=settings.BOT_EMAIL)
        if request.headers.get("x-api-key") == settings.API_KEY:
            for ALLOWED_SUBNET in ALLOWED_SUBNETS:
                if IPAddress(client_ip) in ALLOWED_SUBNET:
                    return auto_user, None

        return None
