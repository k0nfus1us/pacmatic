#a small helper function using python to parse the arch linux RSS news feed
#parameter: date/time of last feed to be considered
import sys
import feedparser
import html2text
import datetime
from time import mktime
from colorama import init, Fore, Style
init()

str_dots = ":: "
str_cdots = Fore.BLUE + Style.BRIGHT + str_dots + Fore.RESET
time_days_fetch = 365*2 #2 years should be enough
f_log = 0

if len(sys.argv) == 2 or len(sys.argv) == 3: 
    if int(sys.argv[1]) >0:
        time_days_fetch = int(sys.argv[1]) 

if len(sys.argv) == 3: 
    outfile = sys.argv[2]
    f_log=open(outfile,"a+")
    
# Feed URL
rss_url = "https://www.archlinux.org/feeds/news/"

# Parse RSS feed with feedparser
feed = feedparser.parse(rss_url)

str_feed_upd = feed.feed.updated_parsed
feed_date = datetime.date.fromtimestamp(mktime(str_feed_upd))
fetch_date = datetime.date.today() - datetime.timedelta(days=time_days_fetch)

if(feed_date < fetch_date):
    print(str_cdots + 'RSS: no updates since ' + str(feed_date) + Style.RESET_ALL)
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
        if f_log:
            f_log.write(str_dots + text + '\n')

    print(Style.RESET_ALL)

    for text in lines[2:]:
        print(text)    
        if f_log:
            f_log.write(text + '\n')

if f_log:
    f_log.close()
