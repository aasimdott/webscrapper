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
