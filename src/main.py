from quart import Quart
from apis.weather import *
from datetime import datetime, timedelta


app = Quart(__name__)

@app.route('/')
async def hello():
    return "hello world!"
   

@app.route('/get_moon_phase')
async def test6():
    s = await get_moon_phase(datetime.utcnow())
    
    return "The moon phase forecast for the next 7 days is: " +str(s)
    

# takes long, lat as arg to return daily weather for the next 7 days
@app.route('/fetch_daily_weather')
async def test7():
    s = await fetch_daily_weather(44.0682,-114.7420)
    return str(s)

# takes long, lat as arg to return hourly weather for the next 7 days
@app.route('/fetch_hourly_weather')
async def test8():
    s  = await fetch_hourly_weather(44.0682,-114.7420)
    return str(s)


if __name__ == '__main__':
    app.run()
