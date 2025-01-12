from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from shop.models import Market, ShopPackage, ShopSection
from shop.serializers import ShopPackageSerializer, ShopSectionSerializer, MarketSerializer


class MarketViewSet(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Market.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination
    serializer_class = MarketSerializer


class ShopViewSet(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = ShopPackage.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination
    serializer_class = ShopPackageSerializer
    view_cache_timeout = 60 * 60

    @method_decorator(cache_page(view_cache_timeout, key_prefix='SHOP_PACKAGE_CACHE'))
    def list(self, request, *args, **kwargs):
        section = self.request.query_params.get('section', None)
        market = self.request.user.shop_info.player_market
        qs = self.get_queryset().filter(markets__in=[market])
        if section and isinstance(section, int):
            qs = self.get_queryset().filter(section_id=int(section))
        pagination = self.paginate_queryset(qs)
        serializer = self.get_serializer(pagination, many=True)
        response = self.get_paginated_response(serializer.data)
        return response

    @method_decorator(cache_page(view_cache_timeout, key_prefix='SHOP_SECTION_CACHE'))
    @action(methods=['GET'], url_path='section', url_name='section', detail=False,
            serializer_class=ShopSectionSerializer)
    def sections(self, request, *args, **kwargs):
        sections = ShopSection.objects.filter(is_active=True)
        return Response(data=self.serializer_class(sections, many=True).data, status=status.HTTP_200_OK)

