import requests
from bs4 import BeautifulSoup
import csv

f = open('problem2_csv.csv', 'w', newline='')
wr = csv.writer(f)

URL = 'https://sites.google.com/view/davidchoi/home/members'
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find("div", class_="UtePc RCETm SwuGbc")
nexts = results.find_all("div", class_="hJDwNd-AhqUyc-II5mzb pSzOP-AhqUyc-II5mzb jXK9ad D2fZ2 OjCsFc GNzUNc")
ids = []
for next in nexts:
    id = next["id"]
    ids.append(id)

for id in ids:
    if id !='h.386cb8162e1f23b4_14' and id != 'h.32b6cfb358927619_169':
        results = soup.find(id=id)
        #print(results.prettify())
        job_elements = results.find_all("p", class_="CDt4Ke zfr3Q")

        for job_element in job_elements:
            texts = job_element.text
            name = ' '.join(texts.split("(")[0].split(" ")[:-1])
            texts = ','.join(texts.split(",")[1:])
            texts = texts.replace(' ', '')
            texts = texts.replace(')', '')

            start_year = texts.split("-")[0]
            end_year = "NA"
            if texts.split("-")[-1]:
                end_year = texts.split("-")[-1]


            links = job_element.find_all("a", class_="XqQF9c")
            profile_pic_url = "NA"
            for link in links:
                link_url = link["href"]
                if link_url:
                    profile_pic_url = link_url

        id = id.split("_")[0] + "_" + str(int(id.split("_")[1])+2)
        results = soup.find(id=id)
        job_elements = results.find_all("p", "CDt4Ke zfr3Q")
        research_interest = "NA"
        current_job_role = "NA"
        for job_element in job_elements:
            if job_element.text.startswith('Research'):
                if ' '.join(job_element.text.split(' ')[2:]) != '':
                    research_interest = ' '.join(job_element.text.split(' ')[2:])
            else:
                current_job_role = job_element.text
        wr.writerow([name, start_year, end_year, research_interest, current_job_role, profile_pic_url])

f.close()