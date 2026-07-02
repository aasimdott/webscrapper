import csv
import time
from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright
searc = input("Enter what you want to search: ")
filename = f"{searc.replace(' ', '_')}_data.csv"
with open(filename, mode="w", newline="", encoding="utf-8") as target:
    excel = csv.writer(target)
    excel.writerow(["Item", "Price", "Link"])
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, executable_path="/usr/bin/chromium")
        page = browser.new_page()
        page.goto("https://ebay.com/")
        sbar = page.locator('[name="_nkw"]')
        sbar.fill(searc)
        page.keyboard.press("Enter")
        try:
            page.wait_for_selector("#srp-river-results", timeout=10000)
        except Exception:
            print("Timeout waiting for search results page.")
        time.sleep(3)
        html = page.content()
        browser.close()
    organise = bs(html, "html.parser")
    main_river = organise.find("div", id="srp-river-results")
    if main_river:
        containers = main_river.find_all("li", class_=lambda c: c and 's-card' in c)
        count = 0
        for container in containers:
            title_element = container.find("span", class_="su-styled-text primary default")
            title = title_element.get_text(strip=True) if title_element else "N/A"
            price_element = container.find("span", class_="su-styled-text primary bold large-1 s-card__price")
            price = price_element.get_text(strip=True) if price_element else "N/A"
            link_element = container.find("a", class_="s-card__link")
            link = link_element.get('href') if link_element else "N/A"
            if title != "N/A" or price != "N/A":
                excel.writerow([title, price, link])
                count += 1
                print(f"{count} Items extracted: {title[:30]}...")
        if count == 0:
            print("Found the container, but couldn't parse individual items. Check layout structure.")
    else:
        print("Could not find the main search results container (#srp-river-results).")
