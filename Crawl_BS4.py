from bs4 import BeautifulSoup
import requests

# URL of the blog search page
url = "https://search.naver.com/search.naver?query=%EC%9E%84%EB%9E%91%ED%95%B4%EC%88%98%EC%9A%95%EC%9E%A5&nso=&where=blog&sm=tab_opt"

# Send a request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links with the class 'title_link'
    links = soup.find_all('a', class_='title_link')

    # Extract href attributes from these links
    hrefs = [link['href'] for link in links]

    print(len(hrefs))
    # Print the extracted hrefs
    for href in hrefs:
        print(href)
else:
    print(
        f"Failed to retrieve the webpage. Status code: {response.status_code}")
