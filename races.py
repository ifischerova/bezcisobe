from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq
import win_unicode_console
#I need import this because I have s problem with encoding in my notebook
win_unicode_console.enable()
#I need import this because I have s problem with encoding in my notebook


page_list = list(range(0, 91))

for p in page_list:
    #filename = "races.csv"
    #f = open(filename, "w")

    page = str(p)

    my_url = 'https://ceskybeh.cz/terminovka/?region=0&dfrom=01.%2001.%202019&dto=31.%2003.%202021&rlength=0&rtype=0&advanced=1&search=&page=' + page

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")


    # This function find list with 35 items, which have selector "class = row".
    # Unfortunately I am not able to find more relevant selector in the web page to find a specific container with races.
    # print(len(containers))
    containers = page_soup.findAll("div", { "class" : "row"})

    # I found by trial-error method that container with relevant content is the 12th one.
    # So I need to select container with index 11.
    # print(container)
    container = containers[11]

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
        #print(names_of_months)
        name_of_month = sliced_date[2]
        if name_of_month in names_of_months:
            month = names_of_months[name_of_month]
            #print(month)
        else:
            raise RuntimeError("U závodu není uvedeno datum v potřebném formátu.")

        #Original way how I was trying to change names of months to its values.
        #if month_in_word == 'ledna':
            #sliced_date[2] = '01'
        #elif month_in_word == 'února':
            #sliced_date[2] = '02'
        #elif month_in_word == 'března':
            #sliced_date[2] = '03'
        #elif month_in_word == 'dubna':
            #sliced_date[2] = '04'
        #elif month_in_word == 'května':
            #sliced_date[2] = '05'
        #elif month_in_word == 'června':
            #sliced_date[2] = '06'
        #elif month_in_word == 'července':
            #sliced_date[2] = '07'
        #elif month_in_word == 'srpna':
            #sliced_date[2] = '08'
        #elif month_in_word == 'září':
            #sliced_date[2] = '09'
        #elif month_in_word == 'října':
            #sliced_date[2] = '10'
        #elif month_in_word == 'listopadu':
            #sliced_date[2] = '11'
        #elif month_in_word == 'prosince':
            #sliced_date[2] = '12'
        #else:
            #print("There is no month!")

        year = sliced_date[3].replace(',', ' ').strip()
        sliced_date[1] = year
        sliced_date[2] = month
        sliced_date[3] = day
        # '-'.join(only_date) - previous used, not so understadable?
        #only_date = sliced_date[1:4]
        # the name of the column in our database in PostgreSQL should be the same -> "date_of_race" instead of "datum_zavodu"
        date_of_race = year + '-' + month + '-' + day
        print(date_of_race)
        #f.write(date_of_race)

    place = container.findAll("p", {"class" : "iframe-visible cb-iframe-place"})
    for p in place:
        # the name of the column in our database in PostgreSQL should be the same -> "place_of_race" instead of "misto_zavodu"
        place_of_race = p.text.strip('()')
        print(place_of_race)
        #f.write(place_of_race)

    name = container.findAll("h4", {"class": "mt-0 mb-0"})
    for n in name:
        #the name of the column in our database in PostgreSQL should be the same -> "name_of_race" instead of "nazev_zavodu"
        name_of_race = n.text.strip()
        print(name_of_race)
        #f.write(name_of_race)
