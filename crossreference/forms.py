from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm, ModelChoiceField
from crispy_forms.helper import FormHelper
from .models import CrossReference


class ContentTypeChoiceField(ModelChoiceField):
    """A ModelChoiceField for ContentType that displays model verbose name as the label.
    """
    def label_from_instance(self, obj):
        return obj.model_class()._meta.verbose_name.capitalize()


class CrossReferenceForm(ModelForm):
    content_type = ContentTypeChoiceField(queryset=ContentType.objects.filter(app_label='nomenclature'))
    target_content_type = ContentTypeChoiceField(queryset=ContentType.objects.filter(app_label='nomenclature'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.help_text_inline = True

    class Meta:
        model = CrossReference
        fields = ['content_type', 'object_id', 'target_content_type', 'target_object_id', 'ref_type', 'metadata']
