from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq
import win_unicode_console # potřebuji, protože mám špatné kódování
win_unicode_console.enable() # potřebuji, protože mám špatné kódování

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

    containers = page_soup.findAll("div", { "class" : "row"})
#najde seznam o 35 prvcích
#print(len(containers))

    container = containers[11]
#print(container)

    date_place = container.findAll("span", {"class" : "text-muted iframe-hidden"})
    del date_place[1::2]
    date = date_place

    for d in date:
        datum_zavodu_se_dny = d.text
        rozsekane_datum = datum_zavodu_se_dny.split(' ')

        den_jedna_cifra = int(rozsekane_datum[1].strip('.'))
        if den_jedna_cifra < 10:
            den = '0' + str(den_jedna_cifra)
        else:
            den = str(den_jedna_cifra)

        mesic_slovo = rozsekane_datum[2]
        if mesic_slovo == 'ledna':
            rozsekane_datum[2] = '01'
        elif mesic_slovo == 'února':
            rozsekane_datum[2] = '02'
        elif mesic_slovo == 'března':
            rozsekane_datum[2] = '03'
        elif mesic_slovo == 'dubna':
            rozsekane_datum[2] = '04'
        elif mesic_slovo == 'května':
            rozsekane_datum[2] = '05'
        elif mesic_slovo == 'června':
            rozsekane_datum[2] = '06'
        elif mesic_slovo == 'července':
            rozsekane_datum[2] = '07'
        elif mesic_slovo == 'srpna':
            rozsekane_datum[2] = '08'
        elif mesic_slovo == 'září':
            rozsekane_datum[2] = '09'
        elif mesic_slovo == 'října':
            rozsekane_datum[2] = '10'
        elif mesic_slovo == 'listopadu':
            rozsekane_datum[2] = '11'
        elif mesic_slovo == 'prosince':
            rozsekane_datum[2] = '12'
        else:
            print("Tady není žádný měsíc!")

        rok = rozsekane_datum[3].replace(',', ' ').strip()
        rozsekane_datum[1] = rok
        mesic = rozsekane_datum[2]
        rozsekane_datum[3] = den
        jen_datum = rozsekane_datum[1:4]
        datum_zavodu = '-'.join(jen_datum)
        print(datum_zavodu)
        #f.write(datum_zavodu)

    place = container.findAll("p", {"class" : "iframe-visible cb-iframe-place"})
    for p in place:
        misto_zavodu = p.text.strip('()')
        print(misto_zavodu)
        #f.write(misto_zavodu)

    name = container.findAll("h4", {"class": "mt-0 mb-0"})
    for n in name:
        nazev_zavodu = n.text.strip()
        print(nazev_zavodu)
        #f.write(nazev_zavodu)

    #f.close()

