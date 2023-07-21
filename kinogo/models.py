from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from embed_video.fields import EmbedVideoField
import datetime
# Create your models here.

CATEGORY_CHOICES = (
    ('драма', 'ДРАМА'),
    ('комедия', 'КОМЕДИЯ'),
    ('эротика', 'ЭРОТИКА'),
    ('мюзиклы', 'МЮЗИКЛЫ'),
    ('триллер', 'ТРИЛЛЕР'),
    ('биографии', 'БИОГРАФИИ'),
    ('военные', 'ВОЕННЫЕ'),
    ('приключения', 'ПРИКЛЮЧЕНИЯ'),
    ('ужасы', 'УЖАСЫ'),
    ('спортивные', 'СПОРТИВНЫЕ'),
)

LANGUAGE_CHOICES = (
    ('американские', 'АМЕРИКАНСКИЕ'),
    ('турецкие', 'ТУРЕЦКИЕ'),
    ('российские', 'РОССИЙСКИЕ'),
    ('индийские', 'ИНДИЙСКИЕ'),
    ('украинские', 'УКРАИНСКИЕ'),
    ('французские', 'ФРАНЦУЗСКИЕ'),
    ('казахстанские', 'КАЗАХСТАНСКИЕ'),
)

STATUS_CHOICES = (
    ('RA', 'НЕДАВНО ДОБАВЛЕННЫЙ'),
    ('MW', 'НАИБОЛЬШЕЕ КОЛИЧЕСТВО ПРОСМОТРОВ'),
    ('TR', 'САМЫЕ ПОПУЛЯРНЫЕ'),
)

SERIALS_CHOICES = (
    ('зарубежные', 'ЗАРУБЕЖНЫЕ'),
    ('турецкие', 'ТУРЕЦКИЕ'),
    ('русские', 'РУССКИЕ'),
    ('мультсериалы', 'МУЛЬТСЕРИАЛЫ'),
    ('дорамы', 'ДОРАМЫ'),
    ('аниме', 'АНИМЕ'),

)







YEARS = []


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000000)
    image = models.ImageField(upload_to='images/')
    video = models.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    serial = models.CharField(choices=SERIALS_CHOICES,max_length=20,default='')
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=20)
    status = models.CharField(choices=STATUS_CHOICES, max_length=6)
    cast = models.CharField(max_length=100)

    for r in range(2005, (datetime.datetime.now().year + 1)):
        YEARS.append((r, r))
    year = models.IntegerField(('year'), choices=YEARS,
                               default=datetime.datetime.now().year)
    views_count = models.IntegerField(default=0)
    movie_trailer = EmbedVideoField(null=True, blank=True)

    created = models.DateField(default=timezone.now)

    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    # tags
    # - download links
    # - watch links


LINK_CHOICES = (
    ('D', 'DOWNLOAD LINK'),
    ('W', 'WATCH LINK'),
)


class MovieLinks(models.Model):
    movie = models.ForeignKey(Movie, related_name='movie_watch_link', on_delete=models.CASCADE, null=True, blank=True,
                              default=True)
    type = models.CharField(choices=LINK_CHOICES, max_length=1)
    link = models.URLField()

    def __str__(self):
        return str(self.movie)
