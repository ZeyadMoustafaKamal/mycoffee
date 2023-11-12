
class BootstrapForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            class_attr = 'form-control'
            if field_name in self.errors:
                class_attr += ' is-invalid'
            field.widget.attrs['class'] = class_attr
