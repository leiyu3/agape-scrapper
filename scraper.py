import requests, bs4, re
import pandas as pd
# headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}
res = requests.get('http://www.agcweb.org/sermons')
res.raise_for_status()
webpage = bs4.BeautifulSoup(res.text, 'html.parser')
table = webpage.find('table', attrs={'class':'goog-ws-list-table'})
table_body = table.find('tbody')
rows = table_body.find_all('tr')
data = []

for row in rows:
    cols = row.find_all('td')
    
    date = cols[0].text.strip()
    title = cols[1].text.strip()
    scripture = cols[3].text.strip()
    speaker = cols[4].text.strip()

    # Scripture Link
    try:
        scripture_link = cols[3].select('a', href=True)[0]['href']
    except IndexError:
        scripture_link = ""
        print(f'Sermon on {date} has no scripture link')

    # Youtube Video Link
    try:
        link_to_sermon = cols[1].select('a', href=True)[0]['href']
        yt_page = requests.get(f'http://www.agcweb.org/{link_to_sermon}')
        soup = bs4.BeautifulSoup(yt_page.text, 'html.parser')
        vid_link = soup.select('iframe')[0]['src']

        pattern = 'd\/.+\?'
        vid_id = re.search(pattern, vid_link).group(0)[2:-1]
        yt_link = 'https://www.youtube.com/watch?v=' + vid_id
    except IndexError:
        yt_link = ""
        print(f'Sermon on {date} have no video')
    except AttributeError:
        yt_link = ""
        print(f'Sermon on {date} have attributeError')

    result = [date, title, yt_link, scripture, scripture_link, speaker]
    data.append(result)

df = pd.DataFrame(data)
df.to_csv('data.csv')
