from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from adverts.models import Advert, Comment, Fav
from adverts.owner import OwnerListView, OwnerDetailView, OwnerDeleteView
from adverts.forms import CreateForm, CommentForm
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q

# Create your views here.

#class AdvertListView(OwnerListView):
#    model = Advert
#    # By convention:
#    # template_name = "adverts/advert_list.html"

#class AdvertDetailView(OwnerDetailView):
#    model = Advert

#class AdvertCreateView(OwnerCreateView):
#    model = Advert
#    # List the fields to copy from the Advert model to the Advert form
#    fields = ['title', 'price', 'text']

#class AdvertUpdateView(OwnerUpdateView):
#    model = Advert
#    fields = ['title', 'price', 'text']
#    # This would make more sense
#    # fields_exclude = ['owner', 'created_at', 'updated_at']

class AdvertListView(OwnerListView):
    model = Advert
    template_name = "adverts/advert_list.html"

    def get(self, request):
        favorites = list()
        strval =  request.GET.get("search", False)
        if strval:
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval) 
            query.add(Q(text__icontains=strval), Q.OR)
            query.add(Q(tags__name__icontains=strval), Q.OR)
            advert_list = Advert.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else:
            #post_list = Post.objects.all().order_by('-updated_at')[:10]
            advert_list = Advert.objects.all()
            if request.user.is_authenticated:
                # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
                rows = request.user.favorite_adverts.values('id')
                # favorites = [2, 4, ...] using list comprehension
                favorites = [ row['id'] for row in rows ]

        # Augment the advert_list
        for obj in advert_list:
            obj.natural_updated = naturaltime(obj.updated_at)

        ctx = {'advert_list' : advert_list, 'favorites': favorites, 'search': strval}
        return render(request, self.template_name, ctx)

class AdvertDetailView(OwnerDetailView):
    model = Advert
    template_name = "adverts/advert_detail.html"
    def get(self, request, pk) :
        x = Advert.objects.get(id=pk)
        comments = Comment.objects.filter(advert=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'advert' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class AdvertCreateView(LoginRequiredMixin, View):
    template_name = 'adverts/advert_form.html'
    success_url = reverse_lazy('pics:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()

        # Adjust the model owner before saving
        inst = form.save(commit=False)
        inst.owner = self.request.user
        inst.save()
        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()

        return redirect(self.success_url)

class AdvertUpdateView(LoginRequiredMixin, View):
    template_name = 'adverts/advert_form.html'
    success_url = reverse_lazy('pics:all')

    def get(self, request, pk):
        pic = get_object_or_404(Advert, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Advert, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()

        # Adjust the model owner before saving
        inst = form.save(commit=False)
        inst.owner = self.request.user
        inst.save()
        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()

        return redirect(self.success_url)

class AdvertDeleteView(OwnerDeleteView):
    model = Advert

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        a = get_object_or_404(Advert, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, advert=a)
        comment.save()
        return redirect(reverse('adverts:advert_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "adverts/comment_delete.html"
    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        advert = self.object.advert
        return reverse('adverts:advert_detail', args=[advert.id])

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        #print("Add PK",pk)
        a = get_object_or_404(Advert, id=pk)
        fav = Fav(user=request.user, advert=a)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        #print("Delete PK",pk)
        a = get_object_or_404(Advert, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, advert=a).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()

def stream_file(request, pk):
    pic = get_object_or_404(Advert, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response
