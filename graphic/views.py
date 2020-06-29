from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.generic import View
from .models import Node, Edge


class NodeSelect(View):
    """Endpoint to serialise and return the details of a specific node, given the ID.
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        d = {
            'success': False,
            'message': 'ERROR: node ID not valid',
        }

        if 'pk' in kwargs:
            try:
                node = Node.objects.get(pk=kwargs['pk'])
                d = {
                    'success': True,
                    'message': '',
                    'response': {
                        'id': node.pk,
                        'class': node.content_type.model_class()._meta.verbose_name.capitalize(),
                        'object': str(node.content_object),
                        'metadata': node.metadata,
                    },
                }
            except Node.DoesNotExist:
                pass

        return JsonResponse(d, safe=False)


class NodeEdgeCount(View):
    """Endpoint to return a count of each type of edge associated with a given node, aggregated
    by the edge label.
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        d = {
            'success': False,
            'message': 'ERROR: node id not valid',
        }

        if 'pk' in kwargs:
            try:
                node = Node.objects.get(pk=kwargs['pk'])
                edges = Edge.objects.filter(Q(source=node) | Q(target=node))
                edges_count = edges.values('type').annotate(count=Count('pk'))
                d = {
                    'success': True,
                    'message': '',
                    'response': {e['type']: e['count'] for e in edges_count},
                }
            except Node.DoesNotExist:
                pass

        return JsonResponse(d, safe=False)


class NodeEdgeSelect(View):
    """Similar output to NodeSelect, but includes a dict of all edges associated with the node
    (outgoing and incoming). This dict will contain two keys (`out` and `in`), the value of each
    consisting of another dict containing the edge labels as keys and a list of nodes as values.
    E.g. {'out': {'is_parent_of': [1, 2, 3], 'is_child_of': [4]}, 'in': {}}
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        d = {
            'success': False,
            'message': 'ERROR: node id not valid',
        }

        if 'pk' in kwargs:
            try:
                node = Node.objects.get(pk=kwargs['pk'])
                if 'type' in request.GET and request.GET['type']:
                    edges_out = node.source.filter(type=request.GET['type'])
                    edges_in = node.target.filter(type=request.get['type'])
                else:
                    edges_out = node.source.all()
                    edges_in = node.target.all()

                # Get lists of all the unique labels in the two edge querysets.
                labels_out = edges_out.values_list('type', flat=True).distinct()
                labels_in = edges_in.values_list('type', flat=True).distinct()

                # For each edge queryset, construct a dict where key == label, value == [node.id, ...]
                # E.g. {'is_parent_of': [1, 2, 3], 'is_child_of': [4]}
                out_nodes = {label: [edge.target.pk for edge in edges_out.filter(type=label)] for label in labels_out}
                in_nodes = {label: [edge.source.pk for edge in edges_in.filter(type=label)] for label in labels_in}

                d = {
                    'success': True,
                    'message': '',
                    'response': {
                        'id': node.pk,
                        'class': node.content_type.model_class()._meta.verbose_name.capitalize(),
                        'object': str(node.content_object),
                        'metadata': node.metadata,
                        'edges': {
                            'out': out_nodes,
                            'in': in_nodes,
                        },
                    },
                }
            except Node.DoesNotExist:
                pass

        return JsonResponse(d, safe=False)


class EdgeSelect(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        d = {
            'success': False,
            'message': 'ERROR: edge id not valid',
        }

        if 'pk' in kwargs:
            try:
                edge = Edge.objects.get(pk=kwargs['pk'])
                d = {
                    'success': True,
                    'message': '',
                    'response': {
                        'id': edge.pk,
                        'source': edge.source.pk,
                        'type': edge.type,
                        'target': edge.target.pk,
                    },
                }
            except Edge.DoesNotExist:
                pass

        return JsonResponse(d, safe=False)
