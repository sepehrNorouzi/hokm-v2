from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email=None, device_id=None, password=None, **extra_fields):
        if not email and not device_id:
            raise ValueError('Users must have an email or device ID')
        username = email or device_id
        if "username" in extra_fields.keys():
            del extra_fields['username']
        user = self.model(
            username=username,
            email=self.normalize_email(email) if email else None,
            device_id=device_id,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username=email, email=email, password=password, **extra_fields)
