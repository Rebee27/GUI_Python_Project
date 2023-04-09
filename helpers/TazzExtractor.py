import requests
from PyQt5.QtWidgets import QProgressBar
from bs4 import BeautifulSoup
import json
from unidecode import unidecode


class Extractor:
    def __init__(self):
        super().__init__()
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)

    def extractData(self):
        # Extract all cities from TAZZ

        url = "https://tazz.ro"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        cities = []

        for city in soup.select('div.cities-cards-list a'):
            cities.append(city.text.strip())

        data = {}
        totalCities = len(cities)
        # Extract restaurant information for each city
        for index, city in enumerate(cities):
            # remove the discritics in the city name
            city = unidecode(city)

            # make the city name lowercase to match the https request
            city = city.lower()

            url = f"https://tazz.ro/{city}/restaurante"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            restaurants = []

            for restaurant in soup.select('div.partnersListLayout div.store-card'):
                name = restaurant.select_one('div.store-info h3')
                if name is not None:
                    name = name.text.strip()
                else:
                    name = ''
                stars = restaurant.select_one('div.store-info div.store-rating')
                if stars is not None:
                    stars = stars.text.strip()
                else:
                    stars = ''

                description = restaurant.select_one('div.store-delivery')
                if description is not None:
                    description = description.text.strip()
                else:
                    description = ''

                # put the details in the restaurant array
                restaurants.append({"name": name, "stars": stars, "description": description})

            data[city] = restaurants
            self.data = data

            # update the progress bar
            progress = int((index + 1) / totalCities * 100)
            self.progressBar.setValue(progress)

        # Store the extracted data in a JSON file
        with open("tazz_data.json", "w") as f:
            json.dump(data, f)
