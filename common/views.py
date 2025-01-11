from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.models import Configuration


class ConfigurationViewSet(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Configuration.objects.filter(is_active=True)

    def list(self, *args, **kwargs):
        return Response(data=self.serializer_class(Configuration.load()), status=status.HTTP_200_OK)
