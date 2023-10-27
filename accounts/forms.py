from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import (  # isort: split
    AuthenticationForm as BaseAuthenticationForm,
    PasswordChangeForm as BasePasswordChangeForm,
    PasswordResetForm as BasePasswordResetForm
)
from django.forms.models import ModelFormMetaclass, fields_for_model

from core.bootstrap.forms import BootstrapForm

from .models import UserProfile

User = get_user_model()


class UserCreationFormMeta(ModelFormMetaclass):
    def __new__(mcs, *args, **kwargs):
        new_class = super().__new__(mcs, *args, **kwargs)

        meta_options = getattr(new_class, 'Meta', None)
        exclude = getattr(meta_options, 'exclude', None)
        user_profile_fields = fields_for_model(UserProfile, exclude=exclude)
        all_fields = {**new_class.base_fields, **user_profile_fields}

        new_class.base_fields = all_fields
        new_class.profile_fields = user_profile_fields
        return new_class


class UserCreationForm(
    BootstrapForm,
    forms.ModelForm,
    metaclass=UserCreationFormMeta
):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = 'email', 'password', 'first_name', 'last_name'
        exclude = 'user', 'favourites'

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not zip_code.isdigit():
            raise forms.ValidationError('The ZIP code shouldn\'n contain letters')
        return zip_code

    def clean(self):
        if 'terms' not in self.data:
            raise forms.ValidationError('You have to agree for the agreement first', code='terms')
        return super().clean()

    def save(self, commit=True):
        user = super().save(commit)
        password = self.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        profile_fields = {name: self.cleaned_data.get(name) for name in self.profile_fields}
        user_profile = UserProfile(user=user, **profile_fields)
        user_profile.save()
        return user

    @property
    def terms_errors(self):
        return [error.message for error in self.non_field_errors().as_data() if error.code == 'terms']


class AuthenticationForm(BootstrapForm, BaseAuthenticationForm):
    pass


class PasswordChangeForm(BootstrapForm, BasePasswordChangeForm):
    pass


class PasswordResetForm(BootstrapForm, BasePasswordResetForm):
    pass
