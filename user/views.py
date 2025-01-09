from django.db import IntegrityError
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import User, NormalPlayer
from user.serializers import NormalPlayerSignUpSerializer, NormalPlayerVerifySerializer


class UserAuthView(viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)

    @action(methods=['POST'], detail=False, url_path="player/signup", url_name="player-signup",
            serializer_class=NormalPlayerSignUpSerializer)
    def player_signup(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except IntegrityError as e:
            return Response({'error': _("User already exists.")}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"message": _(f"OTP is sent to {user.email}."), "user": self.serializer_class(user).data},
                        status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, url_path="player/signup/verify", url_name="player-signup-verify",
            serializer_class=NormalPlayerVerifySerializer)
    def player_email_verify(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user: QuerySet = NormalPlayer.objects.filter(email=data['email'])
        if not user.exists():
            return Response({'error': _("Invalid email.")}, status=status.HTTP_400_BAD_REQUEST)
        user: NormalPlayer = user.first()
        verified = user.verify_email(otp=data["otp"])
        if verified:
            return Response(data={'user': self.serializer_class(user).data, "message": _("Verified successfully")},
                            status=status.HTTP_200_OK)
        return Response(data={'error': _('Invalid OTP.')}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(methods=['POST'], detail=False, url_path="player/login", url_name="player-login")
    def player_signin(self, request, *args, **kwargs):
        pass

    @action(methods=['POST'], detail=False, url_path="guest/signup", url_name="guest-signup")
    def guest_signup(self, request, *args, **kwargs):
        pass

    @action(methods=['POST'], detail=False, url_path="guest/login", url_name="guest-login")
    def guest_signin(self, request, *args, **kwargs):
        pass
