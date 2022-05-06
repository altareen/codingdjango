from django.urls import path, reverse_lazy
from . import views

app_name='adverts'
urlpatterns = [
    path('', views.AdvertListView.as_view(), name='all'),
    path('advert/<int:pk>', views.AdvertDetailView.as_view(), name='advert_detail'),
    path('advert/create', views.AdvertCreateView.as_view(success_url=reverse_lazy('adverts:all')), name='advert_create'),
    path('advert/<int:pk>/update', views.AdvertUpdateView.as_view(success_url=reverse_lazy('adverts:all')), name='advert_update'),
    path('advert/<int:pk>/delete', views.AdvertDeleteView.as_view(success_url=reverse_lazy('adverts:all')), name='advert_delete'),
    path('advert_picture/<int:pk>', views.stream_file, name='advert_picture'),
    path('advert/<int:pk>/comment', views.CommentCreateView.as_view(), name='advert_comment_create'),
    path('comment/<int:pk>/delete', views.CommentDeleteView.as_view(success_url=reverse_lazy('adverts:all')), name='advert_comment_delete'),
    path('advert/<int:pk>/favorite', views.AddFavoriteView.as_view(), name='advert_favorite'),
    path('advert/<int:pk>/unfavorite', views.DeleteFavoriteView.as_view(), name='advert_unfavorite'),
]

# We use reverse_lazy in urls.py to delay looking up the view until all the paths are defined
