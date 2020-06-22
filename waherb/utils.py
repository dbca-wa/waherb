from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import smart_text
from leaflet.admin import LeafletGeoAdmin
from reversion.revisions import create_revision, set_comment
import threading


INITIAL_COMMENT = 'Initial version.'


class ActiveModelManager(models.Manager):

    def current(self):
        return self.filter(effective_to=None)

    def deleted(self):
        return self.filter(effective_to__isnull=False)


class AuditMixin(models.Model):
    """A model mixin that provides fields related to auditing: created/modified timestamps,
    created by/last modified by user fields.
    """
    class Meta:
        abstract = True

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_created', editable=False)
    modifier = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_modified', editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __init__(self, *args, **kwargs):
        super(AuditMixin, self).__init__(*args, **kwargs)
        self._changed_data = None
        self._initial = {}
        if self.pk:
            for field in self._meta.fields:
                self._initial[field.attname] = getattr(self, field.attname)

    def has_changed(self):
        """
        Returns true if the current data differs from initial.
        """
        return bool(self.changed_data)

    def _get_changed_data(self):
        if self._changed_data is None:
            self._changed_data = []
            for field, value in self._initial.items():
                if field in ["modified", "modifier_id"]:
                    continue
                if getattr(self, field) != value:
                    self._changed_data.append(field)
        return self._changed_data
    changed_data = property(_get_changed_data)

    def save(self, *args, **kwargs):
        """
        This falls back on using an admin user if a thread request object wasn't found
        """
        User = get_user_model()
        _locals = threading.local()

        if ((not hasattr(_locals, "request") or _locals.request.user.is_anonymous())):
            if hasattr(_locals, "user"):
                user = _locals.user
            else:
                try:
                    user = User.objects.get(pk=_locals.request.user.pk)
                except Exception:
                    user = User.objects.get(id=1)
                _locals.user = user
        else:
            try:
                user = User.objects.get(pk=_locals.request.user.pk)
            except Exception:
                user = User.objects.get(id=1)

        # If saving a new model, set the creator.
        if not self.pk:
            try:
                self.creator
            except ObjectDoesNotExist:
                self.creator = user

            try:
                self.modifier
            except ObjectDoesNotExist:
                self.modifier = user

            created = True
        else:
            created = False
            self.modifier = user

        super(AuditMixin, self).save(*args, **kwargs)

        if created:
            with create_revision():
                set_comment('Initial version.')
        else:
            if self.has_changed():
                comment = 'Changed ' + ', '.join(self.changed_data) + '.'
                with create_revision():
                    set_comment(comment)
            else:
                with create_revision():
                    set_comment('Nothing changed.')

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        opts = self._meta.app_label, self._meta.model_name
        return reverse("admin:%s_%s_change" % opts, args=(self.pk, ))

    def clean_fields(self, exclude=None):
        """
        Override clean_fields to do what model validation should have done
        in the first place -- call clean_FIELD during model validation.
        """
        errors = {}

        for f in self._meta.fields:
            if f.name in exclude:
                continue
            if hasattr(self, "clean_%s" % f.attname):
                try:
                    getattr(self, "clean_%s" % f.attname)()
                except ValidationError as e:
                    # TODO: Django 1.6 introduces new features to
                    # ValidationError class, update it to use e.error_list
                    errors[f.name] = e.messages

        try:
            super(AuditMixin, self).clean_fields(exclude)
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        if errors:
            raise ValidationError(errors)


class ActiveMixin(models.Model):
    '''
    Model mixin to allow objects to be saved as 'non-current' or 'inactive',
    instead of deleting those objects.
    The standard model delete() method is overridden.

    "effective_to" is used to 'delete' objects (null==not deleted).
    '''
    effective_to = models.DateTimeField(null=True, blank=True)
    objects = ActiveModelManager()

    class Meta:
        abstract = True

    def is_active(self):
        return self.effective_to is None

    def is_deleted(self):
        return not self.is_active()

    def delete(self, *args, **kwargs):
        '''
        Overide the standard delete method; sets effective_to the current date
        and time.
        '''
        if 'delete_permanent' in kwargs and kwargs['delete_permanent']:
            kwargs.pop('delete_permanent')
            super().delete(*args, **kwargs)
        else:
            self.effective_to = timezone.now()
            super().save(*args, **kwargs)


class ModelDescMixin(ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        if hasattr(self, 'model_description'):
            extra_context['model_description'] = self.model_description
        return super().changelist_view(request, extra_context=extra_context)


class ActiveAdminMixin(ModelAdmin):
    """An override of the base ModelAdmin get_queryset method for models using ActiveMixin.
    """
    def get_queryset(self, request):
        # Return 'current' (non-deleted) objects only.
        return self.model._default_manager.current()

    def delete_queryset(self, request, queryset):
        # Override delete_queryset() otherwise the model's delete() method will not be called.
        for obj in queryset:
            obj.delete()


def smart_truncate(content, length=100, suffix="....(more)"):
    """Small function to truncate a string in a sensible way, sourced from:
    http://stackoverflow.com/questions/250357/smart-truncate-in-python
    """
    content = smart_text(content)
    if len(content) <= length:
        return content
    else:
        return " ".join(content[: length + 1].split(" ")[0:-1]) + suffix


class WALeafletGeoAdmin(LeafletGeoAdmin):
    settings_overrides = {
        'DEFAULT_CENTER': (-32.0, 116.0),
        'DEFAULT_ZOOM': 8,
        'SRID': 4326,
        'RESET_VIEW': False,
    }
