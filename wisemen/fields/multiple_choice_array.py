from django.contrib.postgres.fields import ArrayField
from django.forms import MultipleChoiceField


class ChoiceArrayField(ArrayField):
    """
    Multiple Choice field based on PostgreSQL ARRAY type.
    """

    def formfield(self, **kwargs):
        defaults = {
            'form_class': MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)