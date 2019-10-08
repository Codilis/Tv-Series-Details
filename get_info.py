from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
import datetime


class grabber:
    def __init__(self):
        pass

    def check_date(self, date):
        if(date==0):
            return 0
        today=datetime.datetime.now()
        dd=today.day
        mm=today.month
        yyyy=today.year
        if len(str(date))==4:
          if yyyy<=int(date):
            return date
          else:
            return 0
        d=int(date%100)
        date=date/100
        m=int(date%100)
        date=date/100
        y=int(date)
        if yyyy<y:
          return datetime.date(y,m,d)
        elif yyyy==y:
          if mm<m:
            return datetime.date(y,m,d)
          elif mm==m:
            if dd<=d:
              return datetime.date(y,m,d)
            else:
              return 0
          else:
            return 0
        else:
          return 0



    def get_numbered_date(self, date):
        if len(date)==0:
          return 0
        datesDict = {'Jan.':1,
        'Feb.':2,
        'Mar.':3,
        'Apr.':4,
        'May':5,
        'Jun.':6,
        'Jul.':7,
        'Aug.':8,
        'Sep.':9,
        'Oct.':10,
        'Nov.':11,
        'Dec.':12
        }
        numberedDate = 1
        if(len(date) == 4):
            numberedDate = int(date)
            return numberedDate
        splits = date.split(" ")
        if len(splits)==3:
          date,month,year = splits
          month = datesDict[month]
        else:
          date=date[0:1]
          month=date[2:-4]
          year=date[-4:]
        numberedDate = int(year)
        numberedDate *= 100
        numberedDate += int(month)
        numberedDate *= 100
        numberedDate += int(date)
        return numberedDate


    

    def information(self, series):
        series_name = "+".join(series.split(" "))
        search_link = "https://www.imdb.com/find?ref_=nv_sr_fn&q="
        url=search_link+series_name+"&s=all"
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        l=[]

        for link in soup.findAll('a', href=True):
            if(series in str(link.string).lower()):
                l.append("https://www.imdb.com"+link['href'])
        if len(l) == 0:
            return "Information for " + series + " is not available or maybe series does not exist"
        semi_final_link=l[0]
        quote_page = semi_final_link
        page = urlopen(quote_page)
        soup = BeautifulSoup(page, 'html.parser')
        name_box = soup.find('div', attrs={'class': 'seasons-and-year-nav'})
        a=name_box.find_all('a')
        done=1
        t=0
        check=0
        p=1
        for x in a:
            if check==1:
                check=2
            season=x['href']
            final_link='https://www.imdb.com'+season
            #print(final_link)
            quote_page = final_link
            page = urlopen(quote_page)
            soup = BeautifulSoup(page, 'html.parser')
            name_box = soup.find_all('span', attrs={'class': 'nobr'})
            name = name_box[0].text.strip()
            if name[-2]!=" " and name[-2]!="-":
              release_date= "The show " + series + " has finished streaming all its episodes."
              done=0
            else:
              page = urlopen(final_link)
              soup = BeautifulSoup(page, 'html.parser')
              name_box = soup.find_all('div', attrs={'class': 'airdate'})
              l=0
              for item in name_box:
                name = item.text.strip()
                ab=self.get_numbered_date(name)
                if len(name)!=0:
                  if self.check_date(int(ab))!=0 and len(name)==4:
                    release_date="The next season of " + series + " begins in "+str(name)
                    done=0
                    break
                  elif self.check_date(ab)!=0:
                    release_date="The next episode of " + series + " will air on "+str(self.check_date(ab))
                    done=0
                    break
                  else:
                    l=1
                    continue
                else:
                  release_date="Information for " + series + " is not available or maybe series does not exist"
                  done=1
                  check=1
                  break
              
            if done==0:
              return release_date
            elif l==1:
              return "Information for " + series + " is not available or maybe series does not exist" 
            elif check==2:
              return "Information for " + series + " is not available or maybe series does not exist"
            elif done==1:
              continue

