import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm 
# Create your views here.

def index(request):
    url="https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=587f4e55b287b4fb11ee681c62486177"

    if request.method=='POST':
        form=CityForm(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data['city']
            if City.objects.filter(city=new_city).count()==0:
                r=requests.get(url.format(new_city)).json()
                if r['cod']==200:
                    form.save()
                    err_msg="Successful"
                else:
                    err_msg="City doesnot exist"
            else:
                err_msg="City already exist"

    print(err_msg)
    form=CityForm()
    cities=City.objects.all()
    weather=[]
    for city in cities:
        r=requests.get(url.format(city)).json()
        # print(r.text)

        city_weather ={
            'city': city.city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icons': r['weather'][0]['icon']
        }
        weather.append(city_weather)
    # print(weather)
    context={'weather':weather,'form':form}
    return render(request,'the_weather/weather.html',context)