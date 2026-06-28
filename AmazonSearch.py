import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
#take input
searc = input("Enter what you want to search for on Amazon: ")
with sync_playwright() as p:
    # 1. Open the browser
    browser = p.chromium.launch(headless=False, executable_path="/usr/bin/chromium")
    page = browser.new_page()

    # 2. Go to DuckDuckGo
    print("Opening Amazon...")
    page.goto("https://amazon.com")

    # 3. Type your search and hit Enter
    search_bar = page.locator('[name="field-keywords"]')
    search_bar.fill(searc)
    page.keyboard.press("Enter")

    # 4. CRITICAL STEP: Wait for the network to become quiet and results to fully load
    print("Waiting for dynamic search results to load...")
    page.wait_for_selector('div[data-component-type="s-search-result"]', timeout=15000)
    time.sleep(2) # Extra buffer safety pause

    # 5. THE MAGIC BRIDGE: Grab the fully loaded dynamic HTML text from the browser
    fully_loaded_html = page.content()

    # 6. Shut down the browser since we have the data in memory now
    browser.close()

# --- THE CODE DROPS BACK TO REGULAR BEAUTIFULSOUP WORK ---
print("\n--- Processing HTML with BeautifulSoup ---")
soup = BeautifulSoup(fully_loaded_html, "html.parser")

# On DuckDuckGo, search result links have an HTML tag 'a' with a class 'kY2C461wS_HA67wAdwZg'
# (Note: Search engine tags change often, but this layout shows you the logic)
search_titles = soup.find_all("div", {"data-component-type": "s-search-result"})

print(f"Found {len(search_titles)} search results on the page:\n")

# Loop through and print the text of each search result heading
for  titel in search_titles:
    try:
        title_element = titel.find("h2")
        title = title_element.get_text(strip=True) if title_element else "No Title"
        price_element = titel.find("span", class_="a-price-whole")
        price = price_element.get_text(strip=True) if price_element else "N/A"
        print(f"Item: {title}")
        print(f"Price: {price}")
        print("-"*60)
    except Exception:
        continue
