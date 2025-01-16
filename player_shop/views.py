from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from player_shop.models import PlayerWallet
from player_shop.serializers import PlayerWalletSerializer


class PlayerWalletViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = PlayerWallet.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PlayerWalletSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        return Response(self.serializer_class(user.shop_info).data, status=status.HTTP_200_OK)
