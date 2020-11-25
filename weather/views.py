from django.shortcuts import render, redirect
import requests
from weather.models import City
from weather.forms import CityForm

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=7c53a442042b665d89f938ec5d59c4bb'

    error_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    error_msg = 'City does not exits'

            else:
                error_msg = 'City Already exists'
        if error_msg:
            message = error_msg
            message_class = 'is-danger'
        else:
            message = 'City added Successfully'
            message_class = 'is-success'

    form = CityForm()
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']

        }
        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data,
        'form':form,
        'message': message,
        'message_class': message_class
    }
    return render(request,'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

def weather_details(request, city_name):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=7c53a442042b665d89f938ec5d59c4bb'
    city = City.objects.get(name=city_name)
    #weather_data = []


    r = requests.get(url.format(city)).json()

    weather_data = {
        'city': city.name,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
        'min_temp': r['main']['temp_min'],
        'max_temp': r['main']['temp_max'],
        'humidity': r['main']['humidity'],
        'wind_speed': r['wind']['speed'],
        'sunrise': r['sys']['sunrise'],
        'sunset': r['sys']['sunset'],
    }
    #weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data,
    }
    return render(request,'weather/weather_detail.html', context)
