// Handles fetching real weather data from OpenWeatherMap API
// Uses Geocoding API + 5-day forecast API

import axios from "axios";

export async function getWeatherForDate(
  dateString,
  city = "Delhi",
  countryCode = "IN",
) {
  const apiKey = process.env.OPEN_WEATHER_API_KEY;

  if (!apiKey) {
    console.warn("Weather Service Warning: Missing OpenWeatherMap API key");
    return {
      temperature: null,
      condition: "Unknown",
      description: "Unavailable",
    };
  }

  try {
    // Convert city name into latitude and longitude coordinates
    const geo = await axios.get(
      "https://api.openweathermap.org/geo/1.0/direct",
      {
        params: { q: `${city},${countryCode}`, limit: 1, appid: apiKey },
      },
    );

    if (!geo.data.length) throw new Error(`Location not found: ${city}`);
    const { lat, lon } = geo.data[0];

    // Request the 5-day weather forecast using the coordinates
    const forecastRes = await axios.get(
      "https://api.openweathermap.org/data/2.5/forecast",
      {
        params: { lat, lon, units: "metric", appid: apiKey },
      },
    );

    const targetDate = new Date(dateString).toDateString();

    // Filter the API results to find the forecast for the user's booking date
    const dayForecast =
      forecastRes.data.list.find(
        (item) => new Date(item.dt_txt).toDateString() === targetDate,
      ) || forecastRes.data.list[0]; // Fallback to current weather if exact date is far out

    // Return structured data for the frontend to use in seating suggestions
    return {
      temperature: dayForecast.main.temp,
      condition: dayForecast.weather[0].main,
      description: dayForecast.weather[0].description,
    };
  } catch (error) {
    console.error("Weather Service Error:", error.message);
    return {
      temperature: null,
      condition: "Unknown",
      description: "Unavailable",
    };
  }
}
