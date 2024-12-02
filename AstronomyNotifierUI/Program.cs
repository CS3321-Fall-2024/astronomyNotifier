using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace AstronomyNotifierUI
{
    internal static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static async Task Main(string[] args)
        {
            Console.WriteLine("Starting Astronomy Notifier...");

            try
            {
                var baseUrl = "https://127.0.0.1:8000/";

                var asteroidsData = await FetchDataAsync<List<Asteroid>>($"{baseUrl}get_asteroids");
                Console.WriteLine("Asteroids Data:");
                foreach (var asteroid in asteroidsData)
                {
                    Console.WriteLine($"Name: {asteroid.Name}, Magnitude: {asteroid.AbsoluteMagnitudeH}");
                }

                var moonPhase = await FetchDataAsync<string>($"{baseUrl}get_moon_phase");
                Console.WriteLine($"Moon Phase: {moonPhase}");

                var dailyWeather = await FetchDataAsync<List<WeatherForecast>>($"{baseUrl}fetch_daily_weather");
                Console.WriteLine("Daily Weather Forecast:");
                foreach (var forecast in dailyWeather)
                {
                    Console.WriteLine($"Date: {forecast.Date}, High: {forecast.HighTemp}, Low: {forecast.LowTemp}, Description: {forecast.Description}");
                }

                var nasaPicture = await FetchDataAsync<string>($"{baseUrl}get_nasa_picture_of_the_day");
                Console.WriteLine($"NASA Picture of the Day: {nasaPicture}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }
        }

        static async Task<T> FetchDataAsync<T>(string url)
        {
            using (var client = new HttpClient())
            {
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                var response = await client.GetAsync(url);
                if (response.IsSuccessStatusCode)
                {
                    var jsonData = await response.Content.ReadAsStringAsync();
                    return JsonConvert.DeserializeObject<T>(jsonData);
                }
                else
                {
                    throw new HttpRequestException($"Failed to fetch data. Status Code: {response.StatusCode}");
                }
            }
        }

        public class Asteroid
        {
            [JsonProperty("name")]
            public string Name { get; set; }

            [JsonProperty("absolute_magnitude_h")]
            public double AbsoluteMagnitudeH { get; set; }

            [JsonProperty("close_approach_data")]
            public List<CloseApproachData> CloseApproachData { get; set; }
        }

        public class CloseApproachData
        {
            [JsonProperty("miss_distance")]
            public MissDistance MissDistance { get; set; }
        }

        public class MissDistance
        {
            [JsonProperty("kilometers")]
            public string Kilometers { get; set; }
        }

        public class WeatherForecast
        {
            [JsonProperty("date")]
            public string Date { get; set; }

            [JsonProperty("high_temp")]
            public string HighTemp { get; set; }

            [JsonProperty("low_temp")]
            public string LowTemp { get; set; }

            [JsonProperty("description")]
            public string Description { get; set; }
        }

    }
}
