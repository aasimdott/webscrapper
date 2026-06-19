import requests
from bs4 import BeautifulSoup
url = input("Enter the URL of Books site: ")
fakeId = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:151.0) Gecko/20100101 Firefox/151.0"}
response = requests.get(url,fakeId)
print(f"*Response code: {response.status_code}")
organized = BeautifulSoup(response.text, "html.parser")
parentcontainer = organized.find_all("article", class_="product_pod")
print(f"---Found {len(parentcontainer)} Books---")
for container in parentcontainer:
    title = container.h3.a["title"]
    price = container.find("p",class_="price_color").text
    print(f"Book: {title}")
    print(f"Price: {price}")
    print("-"*60)
