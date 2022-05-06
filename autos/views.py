from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from autos.models import Auto, Brand

# Create your views here.

class MainView(LoginRequiredMixin, View):
    def get(self, request):
        brands = Brand.objects.all().count()
        autos = Auto.objects.all()
        context = {'brand_count': brands, 'auto_list': autos}
        return render(request, 'autos/auto_list.html', context)
        
class BrandView(LoginRequiredMixin, View):
    def get(self, request):
        brands = Brand.objects.all()
        context = {'brand_list': brands}
        return render(request, 'autos/brand_list.html', context)

class BrandCreate(LoginRequiredMixin, CreateView):
    model = Brand
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

class BrandUpdate(LoginRequiredMixin, UpdateView):
    model = Brand
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

class BrandDelete(LoginRequiredMixin, DeleteView):
    model = Brand
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

class AutoCreate(LoginRequiredMixin, CreateView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

class AutoUpdate(LoginRequiredMixin, UpdateView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

class AutoDelete(LoginRequiredMixin, DeleteView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')
