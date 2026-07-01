import csv
import time
from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright
site = input("Enter Shop site url: ")
searc = input("Enter for searching: ")
filename = f"{searc.replace(" ","_")}_.csv"
with open(filename, mode="w", newline="", encoding="utf-8") as target:
    excel = csv.writer(target)
    excel.writerow(["Item","Price"])
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, executable_path="/usr/bin/chromium")
        page = browser.new_page()
        page.goto(site)
        sbar = page.locator('[name=field-keywords]')
        sbar.fill(searc)
        page.keyboard.press("Enter")
        page.wait_for_selector('div[data-component-type="s-search-result"]')
        time.sleep(2)
        contents = page.content()
        browser.close()
    soup = bs(contents,"html.parser")
    titles = soup.find_all("div", {"data-component-type": "s-search-result"})
    count = 0
    for title in titles:
        try:
            title_element = title.find("h2")
            item = title_element.get_text(strip=True) if title_element else "N/A"
            price_element = title.find("span", class_="a-whole-price")
            price = price_element.get_text(strip=True)if price_element else "N/A"
            excel.writerow([item, price])
            count += 1
        except Exception:
            continue
print(f"{count} Items wrote into {filename}")
