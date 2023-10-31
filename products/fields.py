import random
import string

from django.db import models


class RandomField(models.Field):

    def __init__(self, lenght=10, allowed_chars=None, *args, **kwargs):
        self.lenght = lenght
        self.allowd_chars = allowed_chars or string.digits
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add:
            value = ''.join(random.choice(self.allowd_chars) for _ in range(self.length))
            setattr(model_instance, self.attname, value)
        else:
            getattr(model_instance, self.attname)
        return value

    def get_internal_type(self):
        return 'CharField'
