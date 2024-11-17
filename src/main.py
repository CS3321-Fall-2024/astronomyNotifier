from quart import Quart
from apis.weather import *
from datetime import datetime, timedelta


app = Quart(__name__)

@app.route('/')
async def hello():
    return "hello world!"
   

@app.route('/test5')
async def test6():
    s = await get_moon_phase(datetime.utcnow())
    
    return "The moon phase forecast for the next 7 days is: " +str(s)
    

@app.route('/test6')
async def test7():
    s = await fetch_daily_weather(44.0682,-114.7420)
    return str(s)

@app.route('/test7')
async def test8():
    s  = await fetch_hourly_weather(44.0682,-114.7420)
    return str(s)


if __name__ == '__main__':
    app.run()
