from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import ModelFormMetaclass, fields_for_model
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
    PasswordChangeForm as BasePasswordChangeForm
)

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


class UserCreationForm(forms.ModelForm, metaclass=UserCreationFormMeta):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = 'email', 'password', 'first_name', 'last_name'
        exclude = 'user', 'favourites'

    def __init__(self, data=None, *args, **kwargs):
        self.post_data = data
        super().__init__(data, *args, **kwargs)
        """ I want to add something for the fields to make the user experience better.
            Some of bootstrap fields can be like this
                <div class="form-group">
                    <label for="inputAddress">Address</label>
                    <input type="text" class="form-control" id="inputAddress" placeholder="1234 Main St" required>
                </div>
            but I can add two fields in the same line like this
                <div class="form-row">
                    <div class="form-group col-md-6">
                        <label for="inputFirstName">First Name</label>
                        <input type="text" class="form-control" id="inputFirstName" required>
                    </div>
                    <div class="form-group col-md-6">
                        <label for="inputLastName">Last Name</label>
                        <input type="text" class="form-control" id="inputLastName" required>
                    </div>
                </div>
            so I think it will be better if I added the col_value which will be added for the class of the field like
            this "col-md-<col_value>" I will hardcode it for now and I may change it later
            TODO: Improve the field classes implementation
            but hey I can just use normal HTML and take care of the names of the fields then why I need all of this.
            well its all because I want to follow DRY as I want a way to show the user some details about the invaid
            fields and if I displayed the normal HTML then I will have to come to every field and add some logic to
            display the error so I thing doing this will be fine it didn't take a lot of time as I expected
           """
        col_classes = [
            {'fields': ['first_name', 'last_name'], 'col_values': [6, 6]},
            {'fields': ['city', 'state', 'zip_code'], 'col_values': [6, 4, 2]}
        ]
        for field_name, field in self.fields.items():
            class_attr = 'form-control'
            if field_name in self.errors:
                class_attr += ' is-invalid'
            for col_item in col_classes:
                if field_name in col_item['fields']:
                    # In order to use it in the template tag implementation
                    field_index = col_item['fields'].index(field_name)
                    col_value = col_item['col_values'][field_index]
                    setattr(field, 'col_value', col_value)
            field.widget.attrs['class'] = class_attr

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not zip_code.isdigit():
            raise forms.ValidationError('The ZIP code shouldn\'n contain letters')
        return zip_code

    def clean(self):
        if 'terms' not in self.post_data:
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


class AuthenticationForm(BaseAuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        for field_name, field in self.fields.items():
            class_attr = 'form-control'
            if field_name in self.errors:
                class_attr += ' is-invalid'
            field.widget.attrs['class'] = class_attr


class PasswordChangeForm(BasePasswordChangeForm):
    def __init__(self, user, *args, **kwargs: Any):
        super().__init__(user, *args, **kwargs)
        print(self.errors)
        for field_name, field in self.fields.items():
            class_attr = 'form-control'
            if field_name in self.errors:
                class_attr += ' is-invalid'
            field.widget.attrs['class'] = class_attr
