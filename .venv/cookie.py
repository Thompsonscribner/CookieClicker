from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Estabilish connection
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")


# Initiate cookie
cookie = driver.find_element(By.ID, value="cookie")

def update_prices():
    store = driver.find_elements(By.CSS_SELECTOR, value="#store div")
    store_prices = {}

    n=0
    for x in store:

        try:
            pair = x.find_element(By.CSS_SELECTOR, value="b").text.split(" - ")
            item = pair[0]
            price = int(pair[1].replace(",", ""))
            store_prices[n] = {
                "item": item,
                "price": price
            }
            n+=1
        except:
            pass

    return dict(reversed(store_prices.items()))

def update_cash():
    # cash = int(driver.find_element(By.ID, value="money").text.replace(",", ""))
    # print(cash)
    return int(driver.find_element(By.ID, value="money").text.replace(",", ""))

def buy(item):
    buy_id = "buy"+item
    item = driver.find_element(By.ID, value=buy_id)
    try:item.click()
    except: print("buying error")



timeout = time.time() + 5
five_min = time.time() + 60*5  # 5 minutes

# Main loop
is_on = True
while is_on:
    cookie.click()

    if time.time() > timeout:
        store_prices = update_prices()
        cash = update_cash()
        for key in store_prices:
            values = store_prices[key]
            if cash >= values["price"]:
                buy(values["item"])
                break
            else:
                continue

        timeout = time.time() + 5

    #score after 5 minutes
    if time.time() > five_min:
        cookie_per_s = driver.find_element(by=By.ID, value="cps").text
        print(cookie_per_s)
        driver.quit()
        is_on = False


