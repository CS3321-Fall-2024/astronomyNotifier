import ephem
from datetime import timedelta

async def get_moon_phase(current_date): # getting the moon phase for specific dates
    phases = []
    # Moon phase names and their corresponding values
    phase_names = [
        (0, "New Moon"),
        (50, "Waxing Crescent"),
        (100, "First Quarter"),
        (150, "Waxing Gibbous"),
        (200, "Full Moon"),
        (250, "Waning Gibbous"),
        (300, "Last Quarter"),
        (350, "Waning Crescent"),
    ]
    
    # Function to calculate the moon phase for a given date
    def get_phase_name(date):
        moon = ephem.Moon(date)
        moon_phase = moon.phase

        for phase_value, phase_name in phase_names:
            if moon_phase < phase_value:
                return phase_name
        return "Waning Crescent"  # Default to Waning Crescent if phase is not found

    # Calculate moon phases for the next 7 days
    for i in range(7):
        future_date = current_date + timedelta(days=i)
        phase_name = get_phase_name(future_date)
        phases.append(phase_name)

    
    return ", ".join(phases)