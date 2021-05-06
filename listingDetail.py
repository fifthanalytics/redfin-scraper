import requests
import cssselect
import json
from collections import namedtuple
import pandas as pd
import lxml.html

class listingDetail:
    def __init__(self, zip_code):
        self.zip_code = zip_code
        self.detail = None

    def get_detail(self):
        base_url = 'https://www.redfin.com/zipcode/'
        url = f'{base_url}{self.zip_code}'

        Listing = namedtuple('Listing', 
                            'full_address redfin_url street_address city state postal_code country rooms price currency')
        listing_list = list()

        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
        response = requests.get(url, headers=headers)

        ## check for response here
        ##
        ##
        tree = lxml.html.fromstring(response.text)
        home_elem = tree.xpath('//*[@id="results-display"]/div[4]')
        div0 = home_elem[0]

        # check for the bulk of the home data here
        for e in div0.xpath(".//script"):
            data_array = json.loads(e.text)
            
            if isinstance(data_array, dict):
                continue
            
            data_drill = data_array[0]
            data_product = data_array[1]
            
            full_address = data_drill['name']
            sub_url = data_drill['url']
            redfin_url = f'http://www.redfin.com{url}'
            street_address = data_drill['address']['streetAddress']
            city = data_drill['address']['addressLocality']
            state = data_drill['address']['addressRegion']
            postal_code = data_drill['address']['postalCode']
            country = data_drill['address']['addressCountry']
            rooms = data_drill['numberOfRooms'] if data_drill.get('numberOfRooms') else '0'
            rooms = float(rooms)

            price = data_product['offers']['price']
            price = float(price)
            currency = data_product['offers']['priceCurrency']
            
            listing = Listing(full_address, redfin_url, street_address, city, 
                                state, postal_code, country, rooms, price, currency)

            listing_list.append(listing)


        df1 = pd.DataFrame(listing_list)

        bb_elem = tree.xpath('//*[@id="MapHomeCard_0"]/div/div/div[2]/div[2]')

        bb_elem0 = bb_elem[0]
        stats_list = list()
        Stats = namedtuple('Stats', 'href beds baths sq_ft')
        beds, baths, sq_ft = None, None, None

        for e in div0.xpath(".//*"):
            link = 'http://www.redfin.com'
            
            if e.attrib.get('href'):
                sub_link = e.attrib['href']
                href = f'{link}{sub_link}'
            
            if e.attrib.get('class'):
                clas = e.attrib['class'].rstrip()
        #         print(f'{clas}--{e.text}')
                
                if clas=='stats':
                    stat = e.text
        #             print(stat)
                    if not isinstance(stat, str):
        #                 print('passed')
                        pass
                    elif stat.find('Beds') != -1:
                        beds = stat
                        beds = beds.replace(' Beds', '')
                        beds = float(beds)

                    elif stat.find('Baths') != -1:
                        baths = stat
                        baths = baths.replace(' Baths', '')
                        baths = float(baths)

                    elif stat.find('Sq. Ft.') != -1:
                        sq_ft = stat
                        sq_ft = sq_ft.replace(',', '').replace(' Sq. Ft.', '')
                        sq_ft = float(sq_ft)
        #                 print('assigned sq ft')
                elif clas=='homeAddressV2':
        #             print('* HEYO'*5)
        #             print(beds, baths, sq_ft)
                    stats = Stats(href, beds, baths, sq_ft)
                    stats_list.append(stats)
                    beds = None
                    baths = None
                    sq_ft = None
                
        df2 = pd.DataFrame(stats_list).rename(columns={'href': 'redfin_url'})
        df_merge = pd.merge(df1, df2, how='left', on='redfin_url')

        result = df_merge.to_dict(orient='records')

        self.detail = result
        return result

    def detail(self):
        return self.detail
