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


class TwoModelsModelFormMeta(ModelFormMetaclass):
    """ I love to build my own things
        So what is this now ... alright this is just a thing that will make me able to use 2 models in the same form
    """
    def __new__(mcs, *args, **kwargs):
        new_class = super().__new__(mcs, *args, **kwargs)
        opts = getattr(new_class, 'Meta', None)
        second_model = getattr(opts, 'model2', None)
        fields = getattr(opts, 'fields2', None)
        exclude = getattr(opts, 'exclude2', None)

        second_fields = fields_for_model(second_model, fields=fields, exclude=exclude)
        new_class.base_fields = {**new_class.base_fields, **second_fields}
        new_class.second_fields = second_fields
        return new_class


class UserCreationForm(
    BootstrapForm,
    forms.ModelForm,
    metaclass=TwoModelsModelFormMeta
):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = 'email', 'password', 'first_name', 'last_name'

        model2 = UserProfile
        exclude2 = 'user', 'favourites'

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

        profile_fields = {field: self.cleaned_data.get(field) for field in self.second_fields}
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


class UserUpdateForm(
    BootstrapForm,
    forms.ModelForm,
    metaclass=TwoModelsModelFormMeta
):
    class Meta:
        model = User
        fields = 'first_name', 'last_name'

        model2 = UserProfile
        exclude2 = 'user', 'favourites'

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not zip_code.isdigit():
            raise forms.ValidationError('The ZIP code shouldn\'n contain letters')
        return zip_code

    def save(self, commit=True):
        user = super().save(commit)
        user_profile = UserProfile.objects.get(user=user)
        profile_fields = {name: self.cleaned_data.get(name) for name in self.second_fields}
        for field in profile_fields:
            setattr(user_profile, field, profile_fields[field])
        user_profile.save()
        return user
