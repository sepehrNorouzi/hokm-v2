from django.http import Http404
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from social.models import FriendshipRequest
from social.serializers import FriendshipRequestSerializer, RequestedFriendshipSerializer


class FriendshipRequestViewSet(GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin,
                               mixins.CreateModelMixin):
    queryset = FriendshipRequest.objects.filter(is_active=True)
    serializer_class = FriendshipRequestSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user)

    def get_requested_friendships(self):
        return self.queryset.filter(sender=self.request.user)

    def get_object(self):
        obj: FriendshipRequest = super(FriendshipRequestViewSet, self).get_object()
        if obj.receiver == self.request.user or obj.sender == self.request.user:
            return obj
        raise Http404

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, 'sender_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['GET'], detail=False, url_path='requested', url_name='requested',
            serializer_class=RequestedFriendshipSerializer)
    def requested_friendships(self, request, *args, **kwargs):
        queryset = self.get_requested_friendships()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='requested', url_name='requested',
            serializer_class=RequestedFriendshipSerializer)
    def requested_friendships(self, request, *args, **kwargs):
        queryset = self.get_requested_friendships()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
