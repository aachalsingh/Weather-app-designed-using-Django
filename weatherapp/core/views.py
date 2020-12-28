from django.shortcuts import render
#from django.http import HttpResponse

# Create your views here.


def get_html_content(request):
    import requests
    city = request.GET.get('city')
    city = city.replace(" ", "+") #this is to removie the plus from sign in 
    #also the below line is used so that google wont block us as we are using as mozilla
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content 


def home(request):
    result = None
    if 'city' in request.GET:
        # fetch the weather from html page
        html_content = get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        result = dict()
        # extracting region from inspect from google
        result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
        # extracting temperature from inspect
        result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
        # geting the day and hour from inspect , the attrs is atribute and wob is id name from the google 
        result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
        # get the actual weather
        result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    return render(request, 'core/home.html', {'result': result})
        
         
    
