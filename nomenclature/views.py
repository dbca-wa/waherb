from django.http import JsonResponse
from django.views.generic import View
from mptt.utils import get_cached_trees
from .models import Name


def recurse_name_to_dict(name):
    """Accepts a Name object that has already been passed through the `get_cached_trees`
    utility function, and returns that object as a dict (including recursive child nodes).
    """
    return {
        'id': name.id,
        'name': name.name,
        'rank': name.rank,
        'children': [recurse_name_to_dict(child) for child in name._cached_children]
    }


class TaxonTreeView(View):
    """Return a serialised full taxon tree for a Name.
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        name = Name.objects.get(pk=kwargs['pk'])
        root = get_cached_trees(name.get_family())[0]
        taxon_tree = recurse_name_to_dict(root)
        return JsonResponse(taxon_tree, safe=False)
