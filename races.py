from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from geopy.geocoders import Here as Geolocator
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded
import win_unicode_console
import math
import time
#I need import this because I have s problem with encoding in my notebook
win_unicode_console.enable()
#I need import this because I have s problem with encoding in my notebook

page_count = 91
date_column = []
place_column = []
name_column = []
latitude_column = []
longitude_column = []
app_id = 'LJYFl2AZbHtLHftkJeWA'
app_code = 'C7sHEhOBFLTVZCQ2K8S4-A'
geolocator = Geolocator(app_id=app_id, app_code=app_code)

def do_geocode(place, attempts=0):
    if attempts > 3:
        print('Too many failed attempts.')
        return None
    elif attempts == 2:
        print('Good night!')
        time.sleep(3*60)
        return do_geocode(place, attempts + 1)

    try:
        return geolocator.geocode(place)
    #we need to handle connection problems to the server.
    except GeocoderTimedOut:
        print('GeocoderTimedOut!!!!')
        time.sleep(2)
        #recursion is a new attempt, it calls the the function itself
        return do_geocode(place, attempts + 1)
    #we need to handle quota of maximum requests per some time period
    except GeocoderQuotaExceeded:
        print('Quota exceeded!!!')
        time.sleep(10)
        #recursion is a new attempt, it calls the function itself
        return do_geocode(place, attempts + 1)


for i in range(0, math.ceil(page_count/10) + 1):
    first_page = i * 10
    last_page = first_page + 10
    for p in range(first_page,last_page):
        page = str(p)
        print('scrapuju stranku '+ page)
        my_url = 'https://ceskybeh.cz/terminovka/?region=0&dfrom=01.%2001.%202019&dto=31.%2003.%202021&rlength=0&rtype=0&advanced=1&search=&page=' + page
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")


        # This function find list with 35 items, which have selector "class = row".
        # Unfortunately I am not able to find more relevant selector in the web page to find a specific container with races.
        containers = page_soup.findAll("div", { "class" : "row"})
        #print(len(containers))
        # I found by trial-error method that container with relevant content is the 13th one.
        # So I need to select container with index 12.
        # print(container)
        container = containers[12]
        # This function will find a list of items, which contains two kinds of span with "class = text-muted iframe-hidden".
        # First is for date of the race, the second for the place of the race.
        date_place = container.findAll("span", {"class" : "text-muted iframe-hidden"})
        # I decided to take a place of the race from another (for me more suitable part) of the webpage, so right now
        # I need only each second item from the list (starting from the first item).
        # I decided delete every second item from the list (starting from the second item).
        del date_place[1::2]
        dates = date_place
        for d in dates:
            d = dates[0]
            date_with_days = d.text
            sliced_date = date_with_days.split(' ')
            day_with_one_digit = int(sliced_date[1].strip('.'))
            if day_with_one_digit < 10:
                day = '0' + str(day_with_one_digit)
            else:
                day = str(day_with_one_digit)
            #Because of our database I need to change names of months to numbers,
            #starting with 0, if the number of the month is smaller than 10. At first I made it with a condition,
            #but it is a quite long and same code. So I tried to make it through dictionary.
            #Keys of dictionary are names of months in the form of the word the same as at the page.
            names_of_months = { 'ledna': '01', 'února': '02', 'března': '03', 'dubna': '04', 'května': '05', 'června':'06', 'července': '07', 'srpna': '08', 'září': '09', 'října': '10', 'listopadu': '11', 'prosince': '12' }
            name_of_month = sliced_date[2]
            if name_of_month in names_of_months:
                month = names_of_months[name_of_month]
            else:
                raise RuntimeError("U závodu není uvedeno datum v potřebném formátu.")
            year = sliced_date[3].replace(',', ' ').strip()
            sliced_date[1] = year
            sliced_date[2] = month
            sliced_date[3] = day
            # '-'.join(only_date) - previous used, not so understadable?
            #only_date = sliced_date[1:4]
            # the name of the column in our database in PostgreSQL should be the same -> "date_of_race" instead of "datum_zavodu"
            date_of_race = year + '-' + month + '-' + day
            date_column.append(date_of_race)

        place = container.findAll("p", {"class" : "iframe-visible cb-iframe-place"})
        for p in place:
            # the name of the column in our database in PostgreSQL should be the same -> "place_of_race" instead of "misto_zavodu"
            place_of_race = p.text.strip('()')
            location = do_geocode(place_of_race)
            if location is None:
                latitude_column.append(.0)
                longitude_column.append(.0)
            else:
                latitude_column.append(location.latitude_column)
                longitude_column.append(location.longitude_column)
            place_column.append(place_of_race)

        name = container.findAll("h4", {"class": "mt-0 mb-0"})
        for n in name:
            #the name of the column in our database in PostgreSQL should be the same -> "name_of_race" instead of "nazev_zavodu"
            #some of the names have "DOPORUČUJEME" in the name co we need to delete this word
            name_of_race = n.text.strip()
            if name_of_race.startswith('DOPORUČUJEME'):
                name_of_race = name_of_race[12:]
            name_column.append(name_of_race)
    print('Finished ten page, going to sleep for 10 seconds.')
    time.sleep(10)

filename = "C:/Users/fischerova/Desktop/bezcisobe/races.csv"
f = open(filename, "w", encoding='UTF-8')
headers="datum_zavodu,misto_zavodu,latitude,longitude,nazev\n"
f.write(headers)

all_races = zip(date_column, place_column, latitude_column, longitude_column, name_column)

for race in all_races:
    #f.write(race[0] + ';\'' + race[1] + '\';\'' + race[2] + '\'' + '\n')
    #f.write(race[0] + ";'" + race[1] + "';'" + str(race[2]).strip('') + '\';\'' + str(race[3]).strip('') + '\';\'' + race[4] + '\'' + '\n')
    f.write("{};'{}';{};{};'{}'\n".format(race[0], race[1], str(race[2]), str(race[3]), race[4]))
f.close()
