from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from shop.models import Item
class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ['uploader', 'title',"price" ,'slug', 'description', 'image']
        else:
            self.fields = ['title', 'slug', "price", 'description', 'image']
        return super().dispatch(request, *args, **kwargs)

class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.uploader = self.request.user
        return super().form_valid(form)

class AuthorAccessMixin():
    def dispatch(self, request, *args, pk, **kwargs):
        product = get_object_or_404(Item, pk=pk)
        if product.uploader == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            return Http404("You! can't see this page")

class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return Http404("You! can't see this page")
        