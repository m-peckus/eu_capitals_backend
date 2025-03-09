#!/usr/bin/env python3

eu_data = {
    "Vienna": {"country": "Austria", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "at"},
    "Brussels": {"country": "Belgium", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "be"},
    "Sofia": {"country": "Bulgaria", "currency_name": "Bulgarian Lev", "currency_code": "BGN", "iso_code": "bg"},
    "Zagreb": {"country": "Croatia", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "hr"},
    "Nicosia": {"country": "Cyprus", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "cy"},
    "Prague": {"country": "Czech Republic", "currency_name": "Czech Koruna", "currency_code": "CZK", "iso_code": "cz"},
    "Copenhagen": {"country": "Denmark", "currency_name": "Danish Krone", "currency_code": "DKK", "iso_code": "dk"},
    "Tallinn": {"country": "Estonia", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "ee"},
    "Helsinki": {"country": "Finland", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "fi"},
    "Paris": {"country": "France", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "fr"},
    "Berlin": {"country": "Germany", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "de"},
    "Athens": {"country": "Greece", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "gr"},
    "Budapest": {"country": "Hungary", "currency_name": "Hungarian Forint", "currency_code": "HUF", "iso_code": "hu"},
    "Dublin": {"country": "Ireland", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "ie"},
    "Rome": {"country": "Italy", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "IT"},
    "Riga": {"country": "Latvia", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "lv"},
    "Vilnius": {"country": "Lithuania", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "lt"},
    "Luxembourg": {"country": "Luxembourg", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "lu"},
    "Valletta": {"country": "Malta", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "mt"},
    "Amsterdam": {"country": "Netherlands", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "nl"},
    "Warsaw": {"country": "Poland", "currency_name": "Polish Zloty", "currency_code": "PLN", "iso_code": "pl"},
    "Lisbon": {"country": "Portugal", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "pt"},
    "Bucharest": {"country": "Romania", "currency_name": "Romanian Leu", "currency_code": "RON", "iso_code": "ro"},
    "Bratislava": {"country": "Slovakia", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "sk"},
    "Ljubljana": {"country": "Slovenia", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "si"},
    "Madrid": {"country": "Spain", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "es"},
    "Stockholm": {"country": "Sweden", "currency_name": "Swedish Krona", "currency_code": "SEK", "iso_code": "se"}
}


# city population added
eu_data_extended = {
    "Vienna": {"country": "Austria", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "at", "city_population": 1950000},
    "Brussels": {"country": "Belgium", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "be", "city_population": 186000},
    "Sofia": {"country": "Bulgaria", "currency_name": "Bulgarian Lev", "currency_code": "BGN", "iso_code": "bg", "city_population": 1230000},
    "Zagreb": {"country": "Croatia", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "hr", "city_population": 806000},
    "Nicosia": {"country": "Cyprus", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "cy", "city_population": 353000},
    "Prague": {"country": "Czech Republic", "currency_name": "Czech Koruna", "currency_code": "CZK", "iso_code": "cz", "city_population": 1330000},
    "Copenhagen": {"country": "Denmark", "currency_name": "Danish Krone", "currency_code": "DKK", "iso_code": "dk", "city_population": 647000},
    "Tallinn": {"country": "Estonia", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "ee", "city_population": 444000},
    "Helsinki": {"country": "Finland", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "fi", "city_population": 658000},
    "Paris": {"country": "France", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "fr", "city_population": 2148000},
    "Berlin": {"country": "Germany", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "de", "city_population": 3769000},
    "Athens": {"country": "Greece", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "gr", "city_population": 664000},
    "Budapest": {"country": "Hungary", "currency_name": "Hungarian Forint", "currency_code": "HUF", "iso_code": "hu", "city_population": 1740000},
    "Dublin": {"country": "Ireland", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "ie", "city_population": 588000},
    "Rome": {"country": "Italy", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "it", "city_population": 2873000},
    "Riga": {"country": "Latvia", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "lv", "city_population": 605000},
    "Vilnius": {"country": "Lithuania", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "lt", "city_population": 544000},
    "Luxembourg": {"country": "Luxembourg", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "lu", "city_population": 132000},
    "Valletta": {"country": "Malta", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "mt", "city_population": 6000},
    "Amsterdam": {"country": "Netherlands", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "nl", "city_population": 872000},
    "Warsaw": {"country": "Poland", "currency_name": "Polish Zloty", "currency_code": "PLN", "iso_code": "pl", "city_population": 1794000},
    "Lisbon": {"country": "Portugal", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "pt", "city_population": 545000},
    "Bucharest": {"country": "Romania", "currency_name": "Romanian Leu", "currency_code": "RON", "iso_code": "ro", "city_population": 1883000},
    "Bratislava": {"country": "Slovakia", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "sk", "city_population": 437000},
    "Ljubljana": {"country": "Slovenia", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "si", "city_population": 286000},
    "Madrid": {"country": "Spain", "currency_name": "Euro", "currency_code": "EUR", "iso_code": "es", "city_population": 3266000},
    "Stockholm": {"country": "Sweden", "currency_name": "Swedish Krona", "currency_code": "SEK", "iso_code": "se", "city_population": 975000}
}

city_data = eu_data_extended["Athens"]
country = city_data["country"]
currency_name = city_data["currency_name"]
currency_code = city_data["currency_code"]
iso_code = city_data["iso_code"]
city_population = city_data["city_population"]
#print(eu_data_extended["Vilnius"]["city_population"])