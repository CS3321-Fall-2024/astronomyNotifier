import httpx

async def get_current_location():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://ipinfo.io")
            data = response.json()
        
        location_str = data['loc']  
        latitude, longitude = map(float, location_str.split(','))
        
        return latitude, longitude
    except Exception as e:
        print("Error fetching location:")