

from django.urls import path
from .views import MovieList, MovieDetail, MovieCategory, MovieLanguage, MovieSearch, MovieYear, MovieSerial, contact, \
    change_password

urlpatterns = [


    path('password-change/', change_password, name='password_change'),
    path('', MovieList.as_view() , name='movie_list'),
    path('category/<str:category>', MovieCategory.as_view() , name='movie_category'),
    path('serial/<str:serial>', MovieSerial.as_view() , name='movie_serial'),
    path('language/<str:lang>', MovieLanguage.as_view() , name='movie_language'),
    path('search/', MovieSearch.as_view() , name='movie_search'),
    path('<slug:slug>', MovieDetail.as_view() , name='movie_detail'),
    path('year/<int:year>', MovieYear.as_view() , name='movie_year'),




]



