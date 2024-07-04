from django.views.decorators.http import require_GET
import requests
from django.http import JsonResponse

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    return client_ip
@require_GET
def hello_api(request):
    visitor_name = request.GET.get('visitor_name', 'Guest').strip('"')
    client_ip = get_client_ip(request)

    if not client_ip:
        return JsonResponse({'error': 'Cannot fetch IP address'}, status=500)

    # For local testing, use a default IP
    if client_ip == '127.0.0.1':
        client_ip = '8.8.8.8'  # Example: Google's public DNS IP

    try:
        # Get location data using IP
        ip_api_url = f'http://ip-api.com/json/{client_ip}'
        ip_response = requests.get(ip_api_url)
        ip_data = ip_response.json()

        print(f"IP API Response: {ip_response.status_code}")
        print(f"IP API Data: {ip_data}")

        if ip_response.status_code == 200 and ip_data.get('status') == 'success':
            lat = ip_data['lat']
            lon = ip_data['lon']
            city = ip_data['city']
            
            # Get weather data using location
            api_key = '3256268559ec8bacb647c6d9cbf7e5ef'
            weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
            
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            print(f"Weather API Response: {weather_response.status_code}")
            print(f"Weather API Data: {weather_data}")

            if weather_response.status_code == 200:
                temperature = weather_data['main']['temp']
                
                greeting = f'Hello, {visitor_name}! The temperature is {temperature:.0f} degrees Celsius in {city}'
            
                response_data = {
                    "client_ip": client_ip,
                    "location": city,
                    "greeting": greeting
                }
                
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'Failed to fetch weather data', 'details': weather_data}, status=weather_response.status_code)
        else:
            return JsonResponse({'error': 'Failed to fetch location data', 'details': ip_data}, status=ip_response.status_code)

    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return JsonResponse({'error': f'Request error: {str(e)}'}, status=500)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)