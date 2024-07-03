# views.py

from django.http import JsonResponse
from django.views.decorators.http import require_GET
import requests

def get_client_ip(request):
    # Check if the X-Forwarded-For header exists (it should in a proxy environment like PythonAnywhere)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # The actual client IP address will be the first one in the list
        client_ip = x_forwarded_for.split(',')[0]
    else:
        # If there is no proxy, use REMOTE_ADDR
        client_ip = request.META.get('REMOTE_ADDR')
    return client_ip

@require_GET
def hello_api(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')
    client_ip = get_client_ip(request)

    if not client_ip:
        return JsonResponse({'error': 'Cannot fetch IP address'}, status=500)

    try:
        # Get weather data using IP
        api_key = '3256268559ec8bacb647c6d9cbf7e5ef'
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat=0&lon=0&appid={api_key}&units=metric'

        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if weather_response.status_code == 200:
            temperature = weather_data['main']['temp']
            city = weather_data['name']

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




# from django.http import JsonResponse
# from django.views.decorators.http import require_GET
# import requests

# def get_client_ip():
#     try:
#         response = requests.get('https://api.ipify.org?format=json')
#         if response.status_code == 200:
#             return response.json()['ip']
#         else:
#             return None
#     except requests.exceptions.RequestException:
#         return None

# @require_GET
# def hello_api(request):
#     visitor_name = request.GET.get('visitor_name', 'Guest')
#     client_ip = get_client_ip()

#     if not client_ip:
#         return JsonResponse({'error': 'Cannot fetch IP address'}, status=500)

#     try:
#         # Get weather data directly using IP
#         api_key = '3256268559ec8bacb647c6d9cbf7e5ef'
#         weather_url = f'http://api.openweathermap.org/data/2.5/weather?ip={client_ip}&appid={api_key}&units=metric'

#         weather_response = requests.get(weather_url)
#         weather_data = weather_response.json()

#         if weather_response.status_code == 200:
#             temperature = weather_data['main']['temp']
#             city = weather_data['name']

#             greeting = f"Hello, {visitor_name}! The temperature is {temperature:.0f} degrees Celsius in {city}"

#             response_data = {
#                 "client_ip": client_ip,
#                 "location": city,
#                 "greeting": greeting
#             }

#             return JsonResponse(response_data)
#         else:
#             return JsonResponse({'error': 'Failed to fetch weather data'}, status=weather_response.status_code)

#     except requests.exceptions.RequestException as e:
#         print(f"Request error: {str(e)}")
#         return JsonResponse({'error': f'Request error: {str(e)}'}, status=500)
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return JsonResponse({'error': f'Error: {str(e)}'}, status=500)