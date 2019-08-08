#a small helper function using python to parse the arch linux RSS news feed
#parameter: date/time of last feed to be consider
import feedparser
import html2text
import datetime
from time import mktime, strftime
from colorama import init, Fore, Style
init()

str_dots = ":: "
str_cdots = Fore.BLUE + Style.BRIGHT + str_dots + Fore.RESET
f_log = 0


# Feed URL
def fetchRSS(rss_url, logfile, fetch_date): #time_days_fetch
    if not rss_url:
      rss_url = "https://www.archlinux.org/feeds/news/"

    print(str_cdots + "Fetching RSS updates from " + rss_url)
    # Parse RSS feed with feedparser
    feed = feedparser.parse(rss_url)

    str_feed_upd = feed.feed.updated_parsed
    feed_date = datetime.date.fromtimestamp(mktime(str_feed_upd))

    if(feed_date < fetch_date):
        print(str_cdots + 'RSS: no updates since ' + str(feed_date) + Style.RESET_ALL)
        return

    # Store feed items in an array
    items = feed["items"]

    # Initialize variable to use as a container for html extracted form feed
    html = ""

    # Store needed item elements in html variable in a reverse order
    # Also, add some HTML tags to make the text more readable
    for item in reversed(items):
        item_date = datetime.date.fromtimestamp(mktime(item["published_parsed"]))  
        if item_date > fetch_date:
            date_str = "[{:s}]".format(strftime("%Y-%m-%d %H:%M",item["published_parsed"]))
            html = html + "<hr>" + date_str + "<br>" + \
                item["title"] + "<br>" + \
                item["summary"] + "<br>"

    # print on screen using html2text
    h2t = html2text.HTML2Text()
    h2t.ignore_images = True
    h2t.body_width = 0
    h2t.single_line_break = True
    rss_str = h2t.handle(html)
    rss_str_arr = filter(None,rss_str.split("* * *"))

    if logfile:
      f_log=open(logfile,"a+")

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
