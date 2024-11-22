import requests
import json
import csv
import pymongo
from pymongo.errors import ConnectionFailure

# MongoDB connection string (replace with your own)
MONGO_URI = "mongodb+srv://ih1004569bero:SMR7ANshotUm1ImH@cluster0.deuhb.mongodb.net/weather_data?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
try:
     # The ismaster command is cheap and does not require auth 
     client.admin.command('ismaster') 
     print("MongoDB connection: Successful") 
except ConnectionFailure: print("MongoDB connection: Failed")
db = client['weather_data']  # Name of the database
collection = db['forecast']  # Name of the collection
# Step 1: Extract data from the OpenWeatherMap API

API_KEY = "772f524d88d9b3db8a4e758a22d1544c"  # Replace with your OpenWeatherMap API key
# List of 200 cities
cities = [
    "London", "New York", "Paris", "Tokyo", "Sydney", "Berlin", "Moscow", "Rio de Janeiro", "Los Angeles", "Rome",
    "Toronto", "Mexico City", "Dubai", "Seoul", "Hong Kong", "Istanbul", "Singapore", "Barcelona", "Buenos Aires", "Chicago",
    "Bangkok", "Delhi", "Mumbai", "Lagos", "Kuala Lumpur", "Jakarta", "Cape Town", "São Paulo", "Cairo", "Lagos",
    "Madrid", "Santiago", "Buenos Aires", "Lima", "Shenzhen", "Chicago", "Dubai", "Beijing", "Milan", "Paris",
    "Melbourne", "Bangkok", "Toronto", "San Francisco", "Montreal", "Cape Town", "Zurich", "Vienna", "Stockholm", "Moscow",
    # "San Diego", "Kuala Lumpur", "Manila", "Dubai", "London", "Lisbon", "Paris", "Rome", "Madrid", "Hamburg",
    # "Vienna", "Berlin", "Frankfurt", "Munich", "Warsaw", "Budapest", "Copenhagen", "Helsinki", "Oslo", "Barcelona",
    # "Athens", "Istanbul", "Montreal", "Montpellier", "Auckland", "Brisbane", "Sydney", "New Orleans", "Cairo", "Chennai",
    # "Jakarta", "Vancouver", "Toronto", "Kyiv", "Tel Aviv", "Tunis", "Kigali", "Santiago", "Medellin", "Addis Ababa",
    # "São Paulo", "Rio de Janeiro", "Toronto", "New York", "Vancouver", "Cape Town", "Dublin", "Berlin", "Vienna",
    # "Lagos", "Hong Kong", "Jakarta", "Milan", "Dubai", "Mexico City", "Toronto", "Lima", "San Francisco", "Seoul",
    # "Manila", "Istanbul", "Nairobi", "Singapore", "Shanghai", "Montreal", "Cape Town", "Berlin", "Vancouver", "Toronto",
    # "Oslo", "Paris", "Los Angeles", "Chicago", "Vienna", "Rome", "Barcelona", "Buenos Aires", "Chicago", "Madrid",
    # "Mumbai", "Delhi", "London", "San Diego", "Bangkok", "Shenzhen", "Melbourne", "Vancouver", "New York", "Mexico City",
    # "Lagos", "Toronto", "Chennai", "Berlin", "Singapore", "Hong Kong", "Los Angeles", "Toronto", "Paris", "San Francisco",
    # "Beijing", "Tokyo", "Rome", "Sao Paulo", "Mumbai", "Delhi", "Lagos", "Cairo", "Nairobi", "Cape Town", "Seoul",
    # "Sydney", "London", "Tokyo", "New York", "Dubai", "Moscow", "Paris", "Istanbul", "Mumbai", "Rio de Janeiro",
    # "San Francisco", "Melbourne", "Madrid", "Cairo", "Rome", "Hong Kong", "Singapore", "Vienna", "Warsaw", "Buenos Aires",
    # "Mexico City", "Kuala Lumpur", "Tokyo", "Manila", "Jakarta", "Berlin", "Cape Town", "Dublin", "Seoul", "Barcelona",
    # "Santiago", "Bangkok", "Mumbai", "Berlin", "Istanbul", "Buenos Aires", "London", "Paris", "Tokyo", "Dubai", "San Diego",
    # "Rome", "Shanghai", "Vancouver", "Los Angeles", "San Francisco", "Delhi", "Barcelona", "Montreal", "Warsaw", "Paris"
]


weather_data = []

# Loop through the cities and fetch weather data
for city in cities:
    # Step 1: Extract data from the OpenWeatherMap API
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(URL)
    
    if response.status_code == 200:
        data = response.json()
        # Step 2: Transform data (extract specific columns)
        # Extract relevant weather data
        weather_info = {
            "city": city,
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "pressure": data['main']['pressure'],
            "wind_speed": data['wind']['speed'],
            "cloudiness": data['clouds']['all'],
            "timestamp": data['dt']
        }
        
        # Add to the weather data list
        weather_data.append(weather_info)
        # Add the weather info to the MongoDB collection
        collection.insert_one(weather_info)  # Insert data into the MongoDB collection
        print(f"Weather data for {city} inserted into MongoDB")
    else:
        print(f"Error fetching data for {city}")

print(len(weather_data))
print(weather_data)
# # Step 3: Load the transformed data into a CSV file
# # Save data to CSV file
# with open('weather_forecast_data.csv', mode='w', newline='', encoding='utf-8') as file:
#     fieldnames = ["city", "temperature", "humidity", "pressure", "wind_speed", "cloudiness", "timestamp"]
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     # Write the header
#     writer.writeheader()
#     # Write the transformed data as a row in the CSV
#     writer.writerows(weather_data)

# print("Weather data written to weather_forecast_data.csv")
# save the requirements in my project : pip freeze > requirements.txt