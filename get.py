# a script to get the full HTML of each
# HackerNews Post

from bs4 import BeautifulSoup

import collections
import os.path
import requests
import time

urls = (
(2011, 1, 'https://news.ycombinator.com/item?id=2057704'),
(2011, 2, 'https://news.ycombinator.com/item?id=2161360'),
(2011, 3, 'https://news.ycombinator.com/item?id=2270790'),
(2011, 4, 'https://news.ycombinator.com/item?id=2396027'),
(2011, 5, 'https://news.ycombinator.com/item?id=2503204'),
(2011, 6, 'https://news.ycombinator.com/item?id=2607052'),
(2011, 7, 'https://news.ycombinator.com/item?id=2719028'),
(2011, 8, 'https://news.ycombinator.com/item?id=2831646'),
(2011, 9, 'https://news.ycombinator.com/item?id=2949787'),
(2011, 10, 'https://news.ycombinator.com/item?id=3060221'),
(2011, 11, 'https://news.ycombinator.com/item?id=3181796'),
(2011, 12, 'https://news.ycombinator.com/item?id=3300290'),
(2012, 1, 'https://news.ycombinator.com/item?id=3412900'),
(2012, 2, 'https://news.ycombinator.com/item?id=3537881'),
(2012, 3, 'https://news.ycombinator.com/item?id=3652041'),
(2012, 4, 'https://news.ycombinator.com/item?id=3783657'),
(2012, 5, 'https://news.ycombinator.com/item?id=3913997'),
(2012, 6, 'https://news.ycombinator.com/item?id=4053076'),
(2012, 7, 'https://news.ycombinator.com/item?id=4184755'),
(2012, 8, 'https://news.ycombinator.com/item?id=4323597'),
(2012, 9, 'https://news.ycombinator.com/item?id=4463689'),
(2012, 10, 'https://news.ycombinator.com/item?id=4596375'),
(2012, 11, 'https://news.ycombinator.com/item?id=4727241'),
(2012, 12, 'https://news.ycombinator.com/item?id=4857714'),
(2013, 1, 'https://news.ycombinator.com/item?id=4992617'),
(2013, 2, 'https://news.ycombinator.com/item?id=5150834'),
(2013, 3, 'https://news.ycombinator.com/item?id=5304169'),       
(2013, 4, 'https://news.ycombinator.com/item?id=5472746'),
(2013, 5, 'https://news.ycombinator.com/item?id=5637663'),
(2013, 6, 'https://news.ycombinator.com/item?id=5803764'),
(2013, 7, 'https://news.ycombinator.com/item?id=5970187'),
(2013, 8, 'https://news.ycombinator.com/item?id=6139927'),
(2013, 9, 'https://news.ycombinator.com/item?id=6310234'),
(2013, 10, 'https://news.ycombinator.com/item?id=6475879'),
(2013, 11, 'https://news.ycombinator.com/item?id=6653437'),
(2013, 12, 'https://news.ycombinator.com/item?id=6827554'),
(2014, 1, 'https://news.ycombinator.com/item?id=6995020'),
(2014, 2, 'https://news.ycombinator.com/item?id=7162197'),
(2014, 3, 'https://news.ycombinator.com/item?id=7324236'),       
(2014, 4, 'https://news.ycombinator.com/item?id=7507765'),
(2014, 5, 'https://news.ycombinator.com/item?id=7679431')
)

def filename(year, month):
    return 'html/hn_%d_%d.html' % (year, month)


stack = collections.deque(urls)
tries = len(stack) * 3 # maximum attempts 3 times of number of URLs

while tries > 0:
    tries -= 1
    current = stack.pop()
    year, month, url = current

    # local html output file
    fname = filename(year, month)
    if os.path.isfile(fname):
        os.remove(fname)

    try:
        # get the HN pages for month / year
        ym_pages = [url]
        while ym_pages:
            url = ym_pages.pop()
            print "Fetching URL: %s" % (url)
            r = requests.get(url)

            # fail if bad error code
            if r.status_code != requests.codes.ok:
                raise Exception('Error from server: ' + str(r.status_code))

            text = r.text.replace('&', '_') # broken HTML escapes breaking BeautifulSoup, removing
            # write out to file in cwd
            with open(fname, 'a') as htmlfile:
                htmlfile.write(text.encode('utf-8'))

            # check for 'More' link
            soup = BeautifulSoup(text)
            links = soup.find_all('a', text='More')
            if links:
                # sometimes foward slash is being html escaped and messed
                # up by above & replacment, need to replace again
                link_url = 'https://news.ycombinator.com' + links[0]['href'].replace('_#x2F;', '/')
                ym_pages.append(link_url)

            # take a break for 30 seconds
            time.sleep(30)

    except Exception as e:
        print 'error:', e, 'currently on:', current
        # stick current URL at the begining of the queue
        stack.appendleft(current)

    # get out when stack is empty
    if not stack: break
