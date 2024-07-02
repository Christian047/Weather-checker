
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import requests

@require_GET
def hello_api(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')

    try:
        # Get IP and geolocation data from ipapi.co
        ip_url = 'https://ipapi.co/json/'
        ip_response = requests.get(ip_url)
        
        if ip_response.status_code == 200:
            ip_data = ip_response.json()
            client_ip = ip_data.get('ip', 'Unknown')
            city = ip_data.get('city', 'Unknown')
        else:
            return JsonResponse({'error': 'Failed to fetch IP and geolocation data'}, status=ip_response.status_code)

        # Get weather data
        api_key = '3256268559ec8bacb647c6d9cbf7e5ef'
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if weather_response.status_code == 200:
            temperature = weather_data['main']['temp']

            greeting = f"Hello, {visitor_name}! The temperature is {temperature:.0f} degrees Celsius in {city}"

            response_data = {
                "client_ip": client_ip,
                "location": city,
                "greeting": greeting
            }

            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Failed to fetch weather data'}, status=weather_response.status_code)

    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return JsonResponse({'error': f'Request error: {str(e)}'}, status=500)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)