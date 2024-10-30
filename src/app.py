# import the module
import python_weather
import asyncio
import os
import geocoder

def get_current_city():
    g = geocoder.ip('me')
    city = ""
    city = g.city
    return city

async def getweather() -> None:
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    # fetch a weather forecast from a city
    weather = await client.get(get_current_city())
    
    # returns the current day's forecast temperature (int)
    print(weather.temperature)

if __name__ == '__main__':
    print(get_current_city())
    
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(getweather())