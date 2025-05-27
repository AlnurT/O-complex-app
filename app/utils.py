import httpx

from app.schemas import SWeather


async def fetch_weather(city: str) -> SWeather:
    async with httpx.AsyncClient() as client:
        geo_url = (
            f"https://geocoding-api.open-meteo.com/v1/search"
            f"?name={city}&count=1"
        )
        geo_response = await client.get(geo_url)
        geo_data = geo_response.json()

        try:
            result = geo_data['results'][0]
        except KeyError:
            raise KeyError

        latitude = result['latitude']
        longitude = result['longitude']
        country_name = result['country']
        city_name = result['name']

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&current_weather=true"
        )
        weather_response = await client.get(weather_url)
        weather_data = weather_response.json()
        current_weather = weather_data.get('current_weather')

        if not current_weather:
            raise ValueError

        temperature = current_weather["temperature"]
        windspeed = current_weather['windspeed']

        return SWeather(
            country=country_name,
            city=city_name,
            temperature=temperature,
            windspeed=windspeed,
        )
