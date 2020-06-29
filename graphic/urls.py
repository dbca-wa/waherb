from django.urls import path
from .views import NodeSelect, NodeEdgeCount, NodeEdgeSelect, EdgeSelect

app_name = 'graphic'
urlpatterns = [
    path('graph/node/<int:pk>/', NodeSelect.as_view(), name='node_select'),
    path('graph/node/<int:pk>/edge-count/', NodeEdgeCount.as_view(), name='node_edge_count'),
    path('graph/node/<int:pk>/edge-select/', NodeEdgeSelect.as_view(), name='node_edge_select'),
    path('graph/edge/<int:pk>/', EdgeSelect.as_view(), name='edge_select'),
]
