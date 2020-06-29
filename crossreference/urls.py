from django.urls import path
from .views import CrossReferenceList, CrossReferenceCreate, CrossReferenceDetail, CrossReferenceUpdate


app_name = 'crossreference'
urlpatterns = [
    path('crossreference/', CrossReferenceList.as_view(), name='cross_reference_list'),
    path('crossreference/create/', CrossReferenceCreate.as_view(), name='cross_reference_create'),
    path('crossreference/<int:pk>/', CrossReferenceDetail.as_view(), name='cross_reference_detail'),
    path('crossreference/<int:pk>/update/', CrossReferenceUpdate.as_view(), name='cross_reference_update'),
]
