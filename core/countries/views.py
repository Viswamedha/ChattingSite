from django.shortcuts import render

from .models import Country

class NoCountry:

    name = 'None Specified'

    capital = 'None Specified'
    population = 0
    
    other_large_cities = 'None Specified'

    national_language = 'Gibberish'
    national_animal = 'The egg'
    national_sport = 'Living'

    currency = 'Money'
    key_landmarks = 'A Sore Sight'
    flag = 'flags/default.png'
    location = 'url'
    content = 'There is no country selected! '


def country(request, slug = 'unspecified', *args, **kwargs):

    context = dict()

    try:
        country = Country.objects.get(slug = slug)
    except:
        country = NoCountry()
    
    
    countries = Country.objects.all()

    context['country'] = country 
    context['countries'] = countries

    return render(request, template_name = 'countries/country.html', context = context)
