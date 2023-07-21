# Create your views here.
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView

from Kinogor import settings

from .forms import ContactForm
from .models import Movie, MovieLinks


class HomeView(ListView):
    model = Movie
    template_name = '../templates/movie/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['top_rated'] = Movie.objects.filter(status='TR').order_by('?')[:6]
        context['most_watched'] = Movie.objects.filter(status='MW').order_by('?')[:6]
        context['recently_added'] = Movie.objects.filter(status='RA').order_by('?')[:6]
        context['movie_all'] = Movie.objects.all()
        return context


class MovieList(ListView):
    model = Movie
    paginate_by = 2


class MovieDetail(DetailView):
    model = Movie

    def get_object(self):
        object = super(MovieDetail, self).get_object()

        object.views_count += 1
        object.save()
        return object


def get_context_data(self, **kwargs):
    context = super(MovieDetail, self).get_context_data(**kwargs)
    context['links'] = MovieLinks.objects.filter(movie=self.get_object())
    context['related_movies'] = Movie.objects.filter(
        category=self.get_object().category)  # .order_by['created'][0:6]
    return context


class MovieCategory(ListView):
    model = Movie
    paginate_by = 2

    def get_queryset(self):
        self.category = self.kwargs['category']
        return Movie.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(MovieCategory, self).get_context_data(**kwargs)
        context['movie_category'] = self.category
        return context

class MovieSerial(ListView):
    model = Movie
    paginate_by = 2

    def get_queryset(self):
        self.serial = self.kwargs['serial']
        return Movie.objects.filter(serial=self.serial)

    def get_context_data(self, **kwargs):
        context = super(MovieSerial, self).get_context_data(**kwargs)
        context['movie_serial'] = self.serial
        return context


class MovieLanguage(ListView):
    model = Movie
    paginate_by = 2

    def get_queryset(self):
        self.language = self.kwargs['lang']
        return Movie.objects.filter(language=self.language)

    def get_context_data(self, **kwargs):
        context = super(MovieLanguage, self).get_context_data(**kwargs)
        context['movie_language'] = self.language
        return context


class MovieSearch(ListView):
    model = Movie
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)

        else:
            object_list = self.model.objects.none()

        return object_list


# class MovieYear(YearArchiveView):
#     queryset = Movie.objects.all()
#     date_field = 'year_of_production'
#     make_object_list = True
#     allow_future = True
#
#     print(queryset)

class MovieYear(ListView):
    model = Movie
    paginate_by = 2

    def get_queryset(self):
        self.year = self.kwargs['year']
        return Movie.objects.filter(year=self.year)

    def get_context_data(self, **kwargs):
        context = super(MovieYear, self).get_context_data(**kwargs)
        context['movie_year'] = self.year
        return context

def contact(request):
    title = 'Contact Us'
    title_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        # print email, message, full_name
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'youotheremail@email.com']
        contact_message = "%s: %s via %s" % (
            form_full_name,
            form_message,
            form_email)
        some_html_message = """
        <h1>hello</h1>
        """
        send_mail(subject,
                  contact_message,
                  from_email,
                  to_email,
                  html_message=some_html_message,
                  fail_silently=True)

    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }
    return render(request, "../templates/others/contact.html", context)






def change_password(request):
    lis_form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        lis_form = PasswordChangeForm(user=request.user, data=request.POST)
        if lis_form.is_valid():
            lis_form.save()
            update_session_auth_hash(request, lis_form.user)
            return render(request, 'registration/change-done.html',
                          {'pass_form': lis_form,
                           'pass_msg': 'Password Updated'})
    return render(request, 'registration/password-reset.html',
                  {'form': lis_form})





