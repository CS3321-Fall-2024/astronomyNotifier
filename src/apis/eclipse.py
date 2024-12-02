import astronomy
import datetime

async def get_next_eclipse(lat, lon):
    
    location = astronomy.Observer(latitude=lat, longitude=lon)
    
    time_instance = astronomy.Time(datetime.now().strftime('%Y-%m-%d'))
    
    next_eclipse = astronomy.SearchLocalSolarEclipse(time_instance, location)
    
    return next_eclipse 