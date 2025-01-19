from rest_framework import serializers

from social.models import FriendshipRequest
from user.serializers import PlayerProfileSerializer


class FriendshipRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    sender = serializers.SerializerMethodField()
    receiver_id = serializers.IntegerField(write_only=True, required=True)
    sender_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = FriendshipRequest
        fields = ['id', 'sender', 'receiver_id', 'sender_id', 'created_time']

    @staticmethod
    def get_sender(obj):
        return PlayerProfileSerializer(obj.sender.player).data


class RequestedFriendshipSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = FriendshipRequest
        fields = ['id', 'receiver', 'created_time', ]

    @staticmethod
    def get_receiver(obj):
        return PlayerProfileSerializer(obj.receiver.player).data
