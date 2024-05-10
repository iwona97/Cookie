from selenium import webdriver
from selenium.webdriver.common.by import By
import time
END_GAME = 5 * 60
STEP_TIME = 10

# Optional - Keep th browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Get cookie to click on
cookie = driver.find_element(By.ID, value="cookie")

# Get store items ids
store_items = driver.find_elements(By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in store_items]

buy_item = time.time() + 10
end_game = time.time() + 60 * 5

while True:
    # 1. click the cookie
    cookie.click()

    # afet 5 seconds check adn buy the most expensive item
    if time.time() >= buy_item:

        # Get available items prices (Elder Pledge is available after certain amount of money)
        # Get all upgrade <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        item_prices = []

        # Convert <b> text into an integer cost
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Create dictionary of store items ids and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # Get current cookie count
        money = driver.find_element(By.ID, value="money").text
        if "," in money:
            money = money.replace(",", "")
        cookie_count = int(money)

        # Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count >= cost:
                affordable_upgrades[cost] = id

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID, value=to_purchase_id).click()

        # Add another 5 seconds until the next check
        buy_item = time.time() + STEP_TIME

        # After 5 minutes stop the bot and check the cookies per second count.
        if time.time() >= end_game:
            cookies_per_second = driver.find_element(By.ID, value="cps").text
            print(cookies_per_second)
            break




























































