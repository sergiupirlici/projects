from bs4 import BeautifulSoup
import urllib.request

req = urllib.request.urlopen('https://www.stiri.md')
html = req.read()

soup = BeautifulSoup(html, 'html.parser')
news = soup.find_all('article', class_='at61ir-0 jaRJMg')

results = []

for item in news:
    title = item.find('div', class_='at61ir-3 gTgSK').get_text(strip=True)
    href = 'https://stiri.md' + (item.a.get('href'))
    img_link = item.find('img', class_='at61ir-5 fgMKSO').get('src')
    time_posted = item.find(
        'div', class_='sc-15kvkpo-2 jsaLuK').get_text(strip=True)
    results.append({
        'title': title,
        'href': href,
        'img_link': img_link,
        'time_posted': time_posted,
    })


f = open('news.txt', 'w', encoding='utf-8')
i = 1
for item in results:
    f.write(
        f'{i} Titlul: {item["title"]}\nLink spre articol: {item["href"]}\nLink spre imagine: {item["img_link"]}\nOra postării: {item ["time_posted"]}\n\n')
    i += 1
f.close()
