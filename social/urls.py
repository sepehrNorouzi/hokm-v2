from rest_framework.routers import DefaultRouter

from social.views import FriendshipRequestViewSet

router = DefaultRouter()

router.register("social/friendship_request", FriendshipRequestViewSet, basename="social-friendship-request")
