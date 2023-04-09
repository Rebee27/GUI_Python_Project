import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, \
    QTableWidgetItem, QLabel, QProgressBar, QSpacerItem, QSizePolicy, QLineEdit
from helpers.TazzExtractor import Extractor


# RestaurantTable is a PyQt widget that displays the extracted data in a table format
class RestaurantTable(QWidget):
    def __init__(self, data):
        super().__init__()
        self.title = "Tazz Partner Restaurants"
        self.width = 800
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(200, 200, self.width, self.height)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # group the restaurants by city and sort them alphabetically by name
        dataByCity = {}
        for city, restaurants in data.items():
            sorted_restaurants = sorted(restaurants, key=lambda r: r['name'])
            dataByCity[city] = [(r['name'], r['description'], r['stars']) for r in sorted_restaurants]

        # sort the cities alphabetically
        sorted_cities = sorted(dataByCity.keys())
        for city in sorted_cities:
            restaurants = dataByCity[city]
            cityLabel = QLabel(city)
            cityLabel.setStyleSheet("font-size: 24px; font-weight: bold; padding-top: 20px;")
            layout.addWidget(cityLabel)

            if len(restaurants) == 0:
                noRestaurantsLabel = QLabel("There are no restaurants available!")
                noRestaurantsLabel.setStyleSheet("font-size: 18px;")
                layout.addWidget(noRestaurantsLabel)
            else:
                self.table_widget = QTableWidget()
                self.table_widget.setRowCount(len(restaurants))
                self.table_widget.setColumnCount(3)
                self.table_widget.setMinimumSize(800, 400)
                self.table_widget.setHorizontalHeaderLabels(['Restaurant', 'Description', 'Stars'])
                for i, (name, description, stars) in enumerate(restaurants):
                    self.table_widget.setItem(i, 0, QTableWidgetItem(name))
                    self.table_widget.setItem(i, 1, QTableWidgetItem(description))
                    self.table_widget.setItem(i, 2, QTableWidgetItem(stars))

                layout.addWidget(self.table_widget)

                # add spacer between cities
                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                layout.addItem(spacer)

        self.setLayout(layout)


# MainWindow is the main PyQt window that contains two buttons for extracting and showing the data
class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.extractor = Extractor()
        self.title = "Tazz Cities"
        self.width = 800
        self.height = 500
        self.setWindowTitle(self.title)
        self.setGeometry(200, 200, self.width, self.height)
        self.extractor.progressBar.valueChanged.connect(self.updateProgressBar)

        layout = QVBoxLayout()
        layout.setSpacing(70)
        layout.setAlignment(Qt.AlignCenter)

        layout.addStretch(1)

        # the extract button
        self.extractButton = QPushButton("Extract Data")
        self.extractButton.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px;")
        self.extractButton.setFixedWidth(500)
        self.extractButton.clicked.connect(self.extractData)
        layout.addWidget(self.extractButton)

        # the progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setStyleSheet("QProgressBar {border: 2px solid grey; border-radius: 5px; padding: 1px;}"
                                       "QProgressBar::chunk {background-color: #05B8CC;}")
        self.progressBar.setFixedWidth(500)
        layout.addWidget(self.progressBar)

        # the label with the progress of the extracting data
        self.statusLabel = QLabel('')
        self.statusLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.statusLabel)

        # the show data button
        self.showButton = QPushButton("Show all cities")
        self.showButton.setStyleSheet("background-color: #05B8CC; color: white; font-size: 18px;")
        self.showButton.setFixedWidth(500)
        self.showButton.clicked.connect(self.showData)
        layout.addWidget(self.showButton)

        # the search bar
        self.searchLabel = QLabel('Search city:')
        self.searchLabel.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.searchLabel)

        self.searchLayout = QHBoxLayout()
        self.searchLayout.setSpacing(20)

        self.searchBox = QLineEdit()
        self.searchBox.setPlaceholderText("Enter city...")
        self.searchBox.setStyleSheet("font-size: 18px;")
        self.searchBox.setFixedWidth(500)
        self.searchLayout.addWidget(self.searchBox)

        self.searchButton = QPushButton("Search")
        self.searchButton.setStyleSheet("background-color: #05B8CC; color: white; font-size: 18px;")
        self.searchButton.clicked.connect(self.searchCities)
        self.searchLayout.addWidget(self.searchButton)

        layout.addLayout(self.searchLayout)

        layout.addStretch(1)

        self.setLayout(layout)

    def extractData(self):
        self.extractor.extractData()
        self.progressBar.setValue(100)
        self.statusLabel.setText("Data extraction complete!")
        self.statusLabel.setStyleSheet("color: green; font-size: 18px;")

    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

    def searchCities(self):
        query = self.searchBox.text().lower()

        try:
            # Load the extracted data from the JSON file and filter the cities by the search query
            with open('tazz_data.json', 'r') as f:
                data = json.load(f)

                filtered_data = {}
                for city, restaurants in data.items():
                    if query in city.lower():
                        filtered_data[city] = restaurants

                # Create a new window with the table widget
                self.tableWindow = RestaurantTable(filtered_data)
                self.tableWindow.show()

        except Exception as e:
            print(e)

    def showData(self):
        try:
            # Load the extracted data from the JSON file and create a list of tuples to display it in a table
            with open('tazz_data.json', 'r') as f:
                data = json.load(f)

                # Create a new window with the table widget
                self.tableWindow = RestaurantTable(data)
                self.tableWindow.show()

        except Exception as e:
            print(e)

