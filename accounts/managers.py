from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('You have to add an email while creating a superuser')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_supseruser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields['is_staff'] is not True:
            raise ValueError('You have to mark is_staff as True while creating a superuser')

        if extra_fields['is_superuser'] is not True:
            raise ValueError('You have to mark is_superuser as True while creating a superuser')
        return self._create_user(email, password, **extra_fields)
