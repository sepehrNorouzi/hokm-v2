from rest_framework import viewsets
from rest_framework.decorators import action

from user.models import User


class UserAuthView(viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)

    @action(methods=['POST'], detail=False, url_path="player/signup", url_name="player-signup")
    def player_signup(self, request, *args, **kwargs):
        pass

    def player_email_verify(self, request, *args, **kwargs):
        pass

    @action(methods=['POST'], detail=False, url_path="player/login", url_name="player-login")
    def player_signin(self, request, *args, **kwargs):
        pass

    @action(methods=['POST'], detail=False, url_path="guest/signup", url_name="guest-signup")
    def guest_signup(self, request, *args, **kwargs):
        pass

    @action(methods=['POST'], detail=False, url_path="guest/login", url_name="guest-login")
    def guest_signin(self, request, *args, **kwargs):
        pass
