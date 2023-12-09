from django.urls import path
from . import views
from .views import DocumentList, DocumentCreateView, DocumentDetailView, ImageDeleteView, DocumentDeleteView, DocumentUpdateView
 #, 
# from .models import Document

app_name = 'document'

urlpatterns = [
    path('', DocumentList.as_view(), name='document_list'),
    path('<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('create', DocumentCreateView.as_view(), name='document_add'),
    path('delete/<int:pk>', DocumentDeleteView.as_view(), name='document_delete'),
    path('edit/<int:pk>', DocumentUpdateView.as_view(), name='document_edit'),
    path('deleting_an_image/<int:image_id>', ImageDeleteView.as_view(), name='deleting_an_image'),
    path('<int:document_id>/pdf/',views.document_pdf, name='document_pdf'),
]
