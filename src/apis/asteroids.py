import httpx

async def get_asteroids(api_key):

    url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={api_key}"
    asteroids = []

    async with httpx.AsyncClient() as client:
        while url:
            try:
                response = await client.get(url)
                response.raise_for_status()  
                data = response.json()
                asteroids.extend(data.get('near_earth_objects', []))
                url = data.get('links', {}).get('next')
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                break  
            except httpx.RequestError as e:
                print(f"Request error occurred: {e}")
                break  

    return asteroids