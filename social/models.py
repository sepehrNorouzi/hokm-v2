from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from user.models import User


class FriendshipRequest(BaseModel):
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='requested_friendships')
    receiver = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='friendship_requests')

    class Meta:
        verbose_name = _('Friendship Request')
        verbose_name_plural = _('Friendship Requests')
        ordering = ['created_time', ]

    def reject(self):
        self.delete()
        return

    def accept(self):
        return Friendship.create_friendship(self.sender, self.receiver)

    def __str__(self):
        return f'{self.sender} requested {self.receiver}'


class Friendship(BaseModel):
    user_1 = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='l_friends')
    user_2 = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='r_friends')

    def save(self, *args, **kwargs):
        if self.user_1.id < self.user_2.id:
            self.user_1, self.user_2 = self.user_2, self.user_1
        super(Friendship, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Friendship')
        verbose_name_plural = _('Friendships')
        unique_together = (('user_1', 'user_2'),)

    def __str__(self):
        return f'{self.user_1} - {self.user_2}'

    @classmethod
    def are_friends(cls, user_1, user_2):
        if user_1.id < user_2.id:
            return cls.objects.filter(user_1=user_1, user_2=user_2).exists()

        return cls.objects.filter(user_2=user_1, user_1=user_2).exists()

    @classmethod
    def create_friendship(cls, user_1, user_2):
        return cls.objects.create(user_1=user_1, user_2=user_2)

    @classmethod
    def list_friends(cls, user):
        return cls.objects.filter(user_1=user) | cls.objects.filter(user_2=user)
