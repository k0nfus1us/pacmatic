#a small helper function using python to parse the arch linux RSS news feed
#parameter: date/time of last feed to be considered
import sys
import feedparser
import html2text
import datetime
from time import mktime
from colorama import init, Fore, Style
init()

str_cdots = Fore.BLUE + Style.BRIGHT + ":: " + Fore.RESET
time_days_fetch = 30
if len(sys.argv) == 2: 
    if int(sys.argv[1]) >0:
        time_days_fetch = int(sys.argv[1]) 
    else:
        time_days_fetch = 365*10 #10 years should be enough

# Feed URL
rss_url = "https://www.archlinux.org/feeds/news/"

# Parse RSS feed with feedparser
feed = feedparser.parse(rss_url)

str_feed_upd = feed.feed.updated_parsed
feed_date = datetime.date.fromtimestamp(mktime(str_feed_upd))
fetch_date = datetime.date.today() - datetime.timedelta(days=time_days_fetch)

if(feed_date < fetch_date):
    print(str_cdots + 'no RSS updates since {:s} [{:s}]'.format(str(feed_date),rss_url))
    print(Style.RESET_ALL)
    exit()
# Store feed items in an array
items = feed["items"]

# Initialize variable to use as a container for html extracted form feed
html = ""

# Store needed item elements in html variable in a reverse order
# Also, add some HTML tags to make the text more readable
for item in reversed(items):
    item_date = datetime.date.fromtimestamp(mktime(item["published_parsed"])) 
    if item_date >= fetch_date:
        #datetime(*timetup[:6]).isoformat()  
        html = html + "<hr>" + item["published"] + "<br>" + \
            item["title"] + "<br>" + \
            item["summary"] + "<br>"

# print on screen using html2text
h2t = html2text.HTML2Text()
h2t.ignore_images = True
h2t.body_width = 0
h2t.single_line_break = True
rss_str = h2t.handle(html)
rss_str_arr = filter(None,rss_str.split("* * *"))

for item in rss_str_arr:
    lines = list(filter(None,item.splitlines()))

    for text in lines[:2]:
        print(str_cdots + text)    

    print(Style.RESET_ALL)

    for text in lines[2:]:
        print(" " + text)    

