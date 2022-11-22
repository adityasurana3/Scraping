import requests
from bs4 import BeautifulSoup
import json
import csv
import time

class Scrapper():
    results = []
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'zguid=24|%24ce82b94b-18bd-4a60-8b75-f96495c5a8a7; zgsession=1|4e595000-06f7-40d3-b58e-99a8d42bc231; _ga=GA1.2.732219597.1669025108; _gid=GA1.2.2127027571.1669025108; zjs_user_id=null; zg_anonymous_id=%2221896a38-f7ed-4480-b4a2-f5f01c61a926%22; zjs_anonymous_id=%22ce82b94b-18bd-4a60-8b75-f96495c5a8a7%22; pxcts=fb4e3b8c-6983-11ed-b1a3-44794859646d; _pxvid=fb4e3028-6983-11ed-b1a3-44794859646d; _gcl_au=1.1.1357084585.1669025112; KruxPixel=true; DoubleClickSession=true; __gads=ID=1e26a3a87fb4d369:T=1669025112:S=ALNI_MboUPyfPx8giab5vPlgHlWNhshEGQ; __gpi=UID=00000b802e9bb9a6:T=1669025112:RT=1669025112:S=ALNI_MZoUogRnL_8v8bFKQupaME9jGn_CQ; __pdst=0922fbfeab4345498afd9bc1ada692af; utag_main=v_id:018499a6256b003ab12cf2c556a005065001d05d00bd0$_sn:1$_se:1$_ss:1$_st:1669026913452$ses_id:1669025113452%3Bexp-session$_pn:1%3Bexp-session; _fbp=fb.1.1669025114118.234962297; _pin_unauth=dWlkPU16QmtObUZoT1RZdE16QmpPUzAwWmpsaExUbGpaREV0TWpZek5EaGxOamcwTWpOaw; _clck=13csrym|1|f6r|0; KruxAddition=true; JSESSIONID=CAE6963AFDE7A1182A65F652A454FCD2; g_state={"i_p":1669034651595,"i_l":1}; _px3=eb603395e93e9b7b3bb39b95fe240448d60b693e31cdc8a0194eabd69f52f9dd:VLS81xod3bgVvJB3FeXcBvqxzOIbkyr6rwuvmuirlrJOo7HuuiAtU4LXEu2U6zhiexNj6tPEL+NVlYXrW/iGDA==:1000:vjImU5zTWDst1lLvuh1sUI2gh415hsrpfAf5AfOlActyB1kdtaEXLOuQ5cH8XNr0IYkQrLi9UQUCGngtmjzf4b2us8En69v29IltOpfLVArxSJFipD6m002d6whry7kDEiCziSeSER+cyTC+5cjKt+Zw1UrGzS9pExxbOAXSryKCTb0J3z3Uyyg+TihOi6gx7JCZFvDs+fFaZ7x/PbL0Xg==; _uetsid=fd9ac5e0698311ed928af177ac08339f; _uetvid=fd9d2090698311ed9d5db752fff0226d; AWSALB=IcMaxgYupFllaOW/JsRxeZK3uo+DYaiJe2KjFWVVoKCY8OJSWssFbOmgo6nHTeUX0fPOlnLLhMbLEk+6kv2cYNLqTEGCgLxBd1P6T726VaBy23x6YYrBwdtG7Bs4; AWSALBCORS=IcMaxgYupFllaOW/JsRxeZK3uo+DYaiJe2KjFWVVoKCY8OJSWssFbOmgo6nHTeUX0fPOlnLLhMbLEk+6kv2cYNLqTEGCgLxBd1P6T726VaBy23x6YYrBwdtG7Bs4; search=6|1671619968787%7Crect%3D40.86163436407077%252C-73.2202510683594%252C40.533665095403244%252C-74.73911093164065%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26lt%3Dfsbo%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%09%096181%09%09%09%09%09%09; _clsk=1tnkr6e|1669027969112|7|0|b.clarity.ms/collect; _gat=1',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}
    def fetch(self,url,params):
        # Fetch the status code 200 if we are getting the correct responce
        response = requests.get(url=url,headers=self.headers,params=params)
        print(response.status_code)
        return response
        
    def parse(self,response):
        content = BeautifulSoup(response,'lxml')
        deck = content.find('ul',{'class':'List-c11n-8-73-8__sc-1smrmqp-0 srp__sc-1psn8tk-0 bfcHMx photo-cards with_constellation'})
        for card in deck.contents:
            script = card.find('script',{'type':'application/ld+json'})
            print(script)
            if script:
                script_json =json.loads(script.contents[0])
                self.results.append({
                    'feature':script_json['@type'],
                    'address':script_json['name'],
                    'floorSize':script_json['floorSize'],
                    'price':card.find('div',{'class':'StyledPropertyCardDataArea-c11n-8-73-8__sc-yipmu-0 hRqIYX'}).text,
                    'sqft': card.find('div', {'class': 'StyledPropertyCardDataArea-c11n-8-73-8__sc-yipmu-0 ghGYOB'}).findAll('span')[3].text,
                    'url':script_json['url'],
                })
        # print(self.results)
    def csv(self):
        with open('text.csv','w') as f:
            writer = csv.DictWriter(f,fieldnames=self.results[0].keys())
            writer.writeheader()
            
            for row in self.results:
                writer.writerow(row)
    
    def run(self):
        url = "https://www.zillow.com/new-york-ny/fsbo"
    
        
        params = {
            'searchQueryState': '{"pagination":{"currentPage":1},"mapBounds":{"west":-74.40093013281245,"east":-73.55498286718745,"south":40.4487909557045,"north":40.96202658306895},"regionSelection":[{"regionId":6181,"regionType":6}],"isMapVisible":false,"filterState":{"isForSaleByAgent":{"value":false},"isNewConstruction":{"value":false},"isForSaleForeclosure":{"value":false},"isComingSoon":{"value":false},"isAuction":{"value":false}},"isListVisible":true}' 
        }
        
        for page in range(1,10):
            params = {
            'searchQueryState': '{"pagination":{"currentPage":%s},"mapBounds":{"west":-74.40093013281245,"east":-73.55498286718745,"south":40.4487909557045,"north":40.96202658306895},"regionSelection":[{"regionId":6181,"regionType":6}],"isMapVisible":false,"filterState":{"isForSaleByAgent":{"value":false},"isNewConstruction":{"value":false},"isForSaleForeclosure":{"value":false},"isComingSoon":{"value":false},"isAuction":{"value":false}},"isListVisible":true}' %page
        }
            res = self.fetch(url,params)
            self.parse(res.text)
            time.sleep(2)
        self.csv()
if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.run()
    
    

# {'@type': 'SingleFamilyResidence', '@context': 'http://schema.org', 'name': '605 Park Ave #12ab, New York, NY 10065', 'floorSize': {'@type': 'QuantitativeValue', '@context': 'http://schema.org', 'value': '2,400'}, 'address': {'@type': 'PostalAddress', '@context': 'http://schema.org', 'streetAddress': '605 Park Ave #12AB', 'addressLocality': 'New York', 'addressRegion': 'NY', 'postalCode': '10065'}, 'geo': {'@type': 'GeoCoordinates', '@context': 'http://schema.org', 'latitude': 40.7663, 'longitude': -73.9668}, 'url': 'https://www.zillow.com/homedetails/605-Park-Ave-12AB-New-York-NY-10065/2060663800_zpid/'}
