from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = 'driver/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)


def click_and_wait(web_element, class_name):
    web_element.click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name)))


driver.get('https://www.sparklease.com/')
find_car_button = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/button[1]")
click_and_wait(find_car_button, "card")
auto_cards = driver.find_elements_by_class_name("card")
for card in auto_cards:
    card.click()
    driver.switch_to.window(driver.window_handles[1])
    random_var = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]").text
    down_pay_amount = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]").text
    driver.close()
driver.quit()


