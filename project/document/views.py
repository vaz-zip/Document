from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from datetime import datetime
# from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, RedirectView
from .models import Document, Image
from .filters import DocFilter
from .forms import DocumentCreateForm, DocumentForm
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from django.urls import reverse_lazy


class DocumentList(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'list.html'
    context_object_name = 'documents'
    queryset = Document.objects.all()
    filter_class = DocFilter 
    paginate_by = 7

    def get_queryset(self):
        self.filter = self.filter_class(self.request.GET, super().get_queryset().filter(author_id=self.request.user.id))
        return self.filter.qs.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['list_in_page'] = self.paginate_by
        context['filter'] = DocFilter(self.request.GET, queryset=self.get_queryset())
        return context


class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = Document
    template_name = 'document_edit.html'
    form_class = DocumentForm

    def get_success_url(self) -> str:
        return reverse('document:document_list')

    # def get_object(self, **kwargs):
    #     id = self.kwargs.get('pk')
    #     return Document.objects.get(pk=id)
    

class DocumentDetailView(DetailView): #LoginRequiredMixin, 
    model = Document
    template_name = 'document_detail.html'
    context_object_name = 'document'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Document.objects.get(pk=id)
    

    

def document_pdf(request, document_id):
        document = get_object_or_404(Document, id=document_id)
        html = render_to_string('pdf.html', 
                                {'document': document},
                            )
        # html = HTML(string=html_string, base_url=request.build_absolute_uri())
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename={document.id}_{document.title}.pdf'
        weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')])
        return response   


class DocumentCreateView(LoginRequiredMixin, CreateView): #LoginRequiredMixin,
    template_name = 'document_add.html'
    form_class = DocumentCreateForm

    def get_success_url(self) -> str:
        return 'document:document_list'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('images')
        if form.is_valid():
            form.cleaned_data.pop('images')
            document = Document.objects.create(**(form.cleaned_data) | {'author': request.user})
            Image.objects.bulk_create(
                [Image(file=file, document=document) for file in files]
            )
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form) 
        

class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = 'document_delete.html'
    context_object_name = 'document'
    def get_success_url(self) -> str:
        return reverse_lazy('document:document_list')

            
           
# class ImageDeleteView(LoginRequiredMixin, RedirectView):
#     def post(self, request, image_id: int, *args, **kwargs):
#         document_id = Image.objects.filter(id=image_id).values('document_id').first()['document_id']
#         Image.objects.filter(id=image_id).delete()

#         return redirect(to=reverse('document:document_detail', kwargs={
#             'pk': document_id,
#         }))

class ImageDeleteView(LoginRequiredMixin, RedirectView):
    def post(self, request, image_id: int, *args, **kwargs):
        document_id = Image.objects.filter(id=image_id).values('document_id').first()['document_id']
        Image.objects.filter(id=image_id).delete()
        return redirect(to=reverse('document:document_detail', kwargs={
            'pk': document_id,
            }))