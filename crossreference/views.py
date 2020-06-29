from django.contrib.contenttypes.models import ContentType
from django.views.generic import ListView, DetailView, CreateView, UpdateView
import json
from .models import CrossReference
from .forms import CrossReferenceForm


class CrossReferenceList(ListView):
    model = CrossReference
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_title'] = 'WASpecies'
        context['content_types'] = [{'id': ct.pk, 'model': ct.model_class()._meta.verbose_name.capitalize()} for ct in ContentType.objects.filter(app_label='nomenclature')]
        context['ref_types'] = CrossReference.objects.values_list('ref_type', flat=True).distinct()
        context['target_content_types'] = [{'id': ct.pk, 'model': ct.model_class()._meta.verbose_name.capitalize()} for ct in ContentType.objects.filter(app_label='nomenclature')]
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if 'content_type' in self.request.GET and self.request.GET['content_type']:
            qs = qs.filter(content_type__id=self.request.GET['content_type'])
        if 'ref_type' in self.request.GET and self.request.GET['ref_type']:
            qs = qs.filter(ref_type=self.request.GET['ref_type'])
        if 'target_type' in self.request.GET and self.request.GET['target_type']:
            qs = qs.filter(target_content_type__id=self.request.GET['target_type'])
        return qs


class CrossReferenceCreate(CreateView):
    model = CrossReference
    form_class = CrossReferenceForm


class CrossReferenceDetail(DetailView):
    model = CrossReference

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_title'] = 'WASpecies'
        context['obj_metadata'] = json.dumps(self.get_object().metadata)
        return context


class CrossReferenceUpdate(UpdateView):
    model = CrossReference
    form_class = CrossReferenceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_title'] = 'WASpecies'
        context['obj_metadata'] = json.dumps(self.get_object().metadata)
        return context
