from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from exceptions.player_shop import DailyRewardEligibilityError
from player_shop.models import PlayerWallet
from player_shop.serializers import PlayerWalletSerializer


class PlayerWalletViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = PlayerWallet.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PlayerWalletSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        return Response(self.serializer_class(user.shop_info).data, status=status.HTTP_200_OK)


class PlayerDailyRewardViewSet(viewsets.GenericViewSet, ):
    queryset = PlayerWallet.objects.filter(is_active=True)
    serializer_class = PlayerWalletSerializer

    @action(methods=['POST'], url_name="claim", url_path="claim", detail=False)
    def claim(self, request, *args, **kwargs):
        player = self.request.user
        player_wallet: PlayerWallet = PlayerWallet.objects.filter(player=player).first()
        if not player_wallet:
            raise RuntimeError(_("Player has no wallet."))
        try:
            player_wallet.claim_daily_reward()
            return Response(self.serializer_class(player_wallet).data, status=status.HTTP_200_OK)
        except DailyRewardEligibilityError as e:
            return Response(data={"error": _(str(e))}, status=status.HTTP_406_NOT_ACCEPTABLE)
