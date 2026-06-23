import time
import csv
import random
from bs4 import BeautifulSoup
from curl_cffi import requests
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
    "device-memory": "8",
    "downlink": "10",
    "ect": "4g",
    "rtt": "50",
    "sec-ch-device-memory": "8",
    "sec-ch-ua": '"Not A(Company;Broken x";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}
with open("sheet.csv", mode="w", newline="", encoding="UTF-8") as target:
    excel = csv.writer(target)
    excel.writerow(["Title", "Price"])
    for page in range(1, 3):
        print(f"--- Fetching Data from Page {page} ---")
        url = f"https://www.amazon.com/s?i=fashion-mens-intl-ship&bbn=16225019011&rh=n%3A7141123011%2Cn%3A16225019011%2Cn%3A679255011&page={page}"
        response = requests.get(url, headers=headers, impersonate="chrome")
        if "To discuss automated access" in response.text or response.status_code == 503:
            print("Blocked by Amazon Bot Detection! We need a proxy.")
            break
        organize = BeautifulSoup(response.text, "html.parser")
        boxes = organize.find_all("div", {"data-component-type": "s-search-result"})
        if not boxes:
            print("No products found. Checking if page structure changed or if captcha triggered.")
        for box in boxes:
            try:
                title_element = box.find("h2")
                title = title_element.get_text(strip=True) if title_element else "No Title"
                price_element = box.find("span", class_="a-price-whole")
                price = price_element.get_text(strip=True) if price_element else "N/A"
                excel.writerow([title, price])
            except Exception:
                continue
        time.sleep(random.uniform(2, 5))
print("Closed")
