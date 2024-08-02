import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url = 'https://pureportal.coventry.ac.uk/en/organisations/eec-school-of-computing-mathematics-and-data-sciences-cmds/publications/'

response = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
    })

soup = BeautifulSoup(response.content, 'html.parser')
publications = soup.find_all('div', class_='result-container')


data = [ ]
for result in  publications:
    pub_link = result.select_one('h3.title a')['href']
    if pub_link:
        pub_response =  requests.get(pub_link, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'})
        pub_soup = BeautifulSoup(pub_response.content, 'html.parser')
        title = pub_soup.select_one('div.introduction h1 span' ).get_text(strip=True)
        author_with_link = pub_soup.select('p.relations.persons a')
        authors = []
        for author in author_with_link:
            author_name = author.get_text(strip = True)
            author_link = author['href']
            authors.append({'name' : author_name, 'link':author_link})

        author_without_link = pub_soup.select_one('p.relations.persons ' )
        for content in author_without_link.contents:
            if isinstance(content, str):
                for name in content.split(','):
                    if name.strip(' '):
                        authors.append({'name' :name.strip()})
                    
        dates = pub_soup.select('tr.status span.date')
        pub_date = ' '
        for date in dates:
            pub_date = date.get_text(strip = True)
            # authors.append({'Date':pub_date})
        

        data.append({'Title' :title, 'Publication link':pub_link , 'Author' :authors , 'publication Date':pub_date} )
        
        # print(authors)
        # time.sleep(5)

        df = pd.DataFrame(data)
        # print(df)

# # Convert DataFrame to CSV
# df.to_csv('pub.csv', index=False)
    
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import time
# import urllib.robotparser

# # Define the base URL and headers
# base_url = 'https://pureportal.coventry.ac.uk'
# url = f'{base_url}/en/organisations/eec-school-of-computing-mathematics-and-data-sciences-cmds/publications/'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
# }

# # Parse the robots.txt file
# robots_url = f'{base_url}/robots.txt'
# rp = urllib.robotparser.RobotFileParser()
# rp.set_url(robots_url)
# rp.read()

# # Check if the main publications page is allowed to be scraped
# if rp.can_fetch(headers['User-Agent'], url):
#     # Request the main publications page
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Find all publication containers
#     publications = soup.find_all('div', class_='result-container')
#     data = []

#     # Iterate over each publication
#     for result in publications:
#         pub_link = result.select_one('h3.title a')['href']
#         full_pub_link = base_url + pub_link
        
#         # Check if the publication link is allowed to be scraped
#         if rp.can_fetch(headers['User-Agent'], full_pub_link):
#             # Request the publication page
#             pub_response = requests.get(full_pub_link, headers=headers)
#             pub_soup = BeautifulSoup(pub_response.content, 'html.parser')
            
#             # Extract the title
#             title = pub_soup.select_one('div.introduction h1 span').get_text(strip=True)
            
#             # Extract the authors
#             author_with_link = pub_soup.select('p.relations.persons a')
#             authors = []
#             for author in author_with_link:
#                 author_name = author.get_text(strip=True)
#                 author_link = base_url + author['href']
#                 authors.append({'name': author_name, 'link': author_link})

#             author_without_link = pub_soup.select_one('p.relations.persons')
#             if author_without_link:
#                 for content in author_without_link.contents:
#                     if isinstance(content, str):
#                         for name in content.split(','):
#                             if name.strip():
#                                 authors.append({'name': name.strip()})

#             # Extract the publication date
#             dates = pub_soup.select('tr.status span.date')
#             pub_date = ' '
#             for date in dates:
#                 pub_date = date.get_text(strip=True)
            
#             # Append the extracted data
#             data.append({'Title': title, 'Publication link': full_pub_link, 'Author': authors, 'Publication Date': pub_date})

#             # Print the authors (for debugging purposes)
#             print(authors)

#             # Respectful crawling: add a delay between requests
#             time.sleep(1)
#         else:
#             print(f"Fetching {full_pub_link} is disallowed by robots.txt")

#     # Create a DataFrame from the data
#     df = pd.DataFrame(data)

#     # Convert the DataFrame to a CSV file
#     df.to_csv('pub.csv', index=False)

#     print('Data has been saved to pub.csv')
# else:
#     print(f"Fetching {url} is disallowed by robots.txt")
