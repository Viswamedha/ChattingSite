from django.db import models
from django.utils.text import slugify 


class Country(models.Model):

    name = models.CharField(verbose_name = 'Name', max_length = 100, unique = True)
    slug = models.SlugField(blank = True, null = True)

    capital = models.CharField(verbose_name = 'Capital', max_length = 100, blank = True, null = True)
    population = models.BigIntegerField(verbose_name = 'Population', blank = True, null = True)
    
    other_large_cities = models.CharField(verbose_name = 'Other Large Cities', max_length = 1000, blank = True, null = True)

    national_language = models.CharField(verbose_name = 'National Language', max_length = 1000, blank = True, null = True)
    national_animal = models.CharField(verbose_name = 'National Animal(s)', max_length = 200, blank = True, null = True)
    national_sport = models.CharField(verbose_name = 'National Sport(s)', max_length = 200, blank = True, null = True)

    currency = models.CharField(verbose_name = 'Currency', max_length = 100, blank = True, null = True)  
    key_landmarks = models.CharField(verbose_name = 'Key Landmarks', max_length = 1000, blank = True, null = True)
    flag = models.ImageField(verbose_name = 'Flag', upload_to = 'flags/', blank = True, null = True)
    location = models.URLField(verbose_name = 'Location', blank = True, null = True)
    content = models.TextField(verbose_name = 'Content', max_length = 3000, blank = True, null = True)


    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    
