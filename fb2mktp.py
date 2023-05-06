#!/usr/bin/env python3
# File name          : fb2mktp.py
# Author             : C3n7ral051nt4g3ncy (aka @OSINT_Tactical)
# Date created       : May 2023

# Python libs
import requests
from parsel import Selector
import webbrowser
import time
import sys

# FB2MKTP Banner
print("""========================================================================
=        ==      =======   =====  =====  ==  ====  ==        ==       ==
=  ========  ===  ====   =   ===   ===   ==  ===  ======  =====  ====  =
=  ========  ====  ==   ===   ==  =   =  ==  ==  =======  =====  ====  =
=  ========  ===  ========   ===  == ==  ==  =  ========  =====  ====  =
=      ====      ========   ====  =====  ==     ========  =====       ==
=  ========  ===  ======   =====  =====  ==  ==  =======  =====  =======
=  ========  ====  ====   ======  =====  ==  ===  ======  =====  =======
=  ========  ===  ====   =======  =====  ==  ====  =====  =====  =======
=  ========      ====        ===  =====  ==  ====  =====  =====  =======
========================================================================""")
print()
print("FB2MKTP ==> Facebook to Marketplace")
print("Go fast from a Facebook profile URL to the target's Marketplace Profile")
print()
print()


# Facebook URL or can input a few URLs with a space
urls = input("Paste Facebook URL ==> ")


# Convert the input into a list of URLs
urls = urls.strip().split()


# Cookies, Device Pixel Ratio, wd Facebook cookie
cookies = {
    'dpr': '2',
    'wd': '1280x649',
}


# Define http headers (domain request is sent to, user-agent, browser, version)
headers = {
    'authority': 'www.facebook.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36',
    'viewport-width': '640',
}

# GET request including headers and cookies, pass to selector from scrapy library to extract data from HTML response
for url in urls:
    res = requests.get(url, headers=headers, cookies=cookies)
    response = Selector(text=res.text, type="html")

    id = response.xpath('//meta[@property="al:android:url"]/@content')
    if id:
        id = id.get().split("/")[-1]
    else:
        id = response.xpath('//script[contains(text(), "TimeSliceImpl")]').re_first('\"entity_id\":\"(\d+)\"')

    if not id:
        data = {
            'fburl': url,
            'check': 'Lookup',
        }

        # Lookup-id.com headers
        headers = {
            'authority': 'lookup-id.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/'
                      '*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'uk,en-US;q=0.9,en;q=0.8,id;q=0.7',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/109.0.0.0 Safari/537.36',
        }

        res = requests.post('https://lookup-id.com/', headers=headers, data=data)
        response = Selector(text=res.text, type="html")
        

        # Extract ID using css selector
        id = response.css('span#code::text').get()


    # Print user ID or let user know the ID wasn't found
    if not id:
        id = 'Facebook ID Not found please try again'
    print()
    print(f'For the Facebook profile => {url}, the ID Found is ==> {id}')


    # With the ID found, pivot straight to the Target Marketplace profile with automatic browser opening
    marketplace_url = f'https://www.facebook.com/marketplace/profile/{id}'
    webbrowser.open(marketplace_url)

sys.exit(0)