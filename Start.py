from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from parse import parse
from datetime import date
import pymongo

DRIVER_PATH = 'driver/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
scrapping_done = False

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["sparklease"]
collection = db["data"]


def click_and_wait(web_element, class_name):
    web_element.click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, class_name)))


def click_and_wait_id(web_element, id_name):
    web_element.click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, id_name)))


def toggle_lease_cash():
    lease_box = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div[1]/label[1]/div")
    click_and_wait(lease_box, "card")


def toggle_private_dealer():
    private_box = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div[1]/label[3]/div")
    click_and_wait(private_box, "card")


def next_page():
    next_page_button = driver.find_element_by_xpath("//*[@id='auto-list-wrapper']/div[2]/div[2]/div/span[7]")
    click_and_wait(next_page_button, "card")


def is_last_page():
    pagination_text = driver.find_element_by_xpath("//*[@id='auto-list-wrapper']/div[2]/div[1]/span").text
    last_num, total_num = parse("Showing {} - {} of {}", pagination_text)[1], \
                          parse("Showing {} - {} of {}", pagination_text)[2]
    return True if last_num == total_num else False


def is_car_eligible(car):
    bubble_list = car.find_elements(By.CSS_SELECTOR, "div.bubble-container span")
    if len(bubble_list) == 2:
        if bubble_list[1].text == "已售" or bubble_list[0].text == "转FINANCE":
            return False
    elif bubble_list[0].text == "转FINANCE":
        return False
    return True


def expand_config_list():
    try:
        more_button = driver.find_element(By.ID, "carConfigShowMore")
        click_and_wait_id(more_button, "carConfigShowLess")
    except NoSuchElementException:
        pass


def get_car_info():
    car_id = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div/div[2]/div/div[2]").text
    car_model = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div/div[1]/div[1]").text
    car_type = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div/div[1]/div[2]").text
    original_downpay = driver.find_element_by_xpath(
        "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div").text
    pay_or_get = driver.find_element_by_xpath(
        "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]").text
    down_pay_amount = driver.find_element_by_xpath(
        "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]").text
    monthly_payment = driver.find_element_by_xpath(
        "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]").text
    start_date = driver.find_element_by_xpath(
        "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[1]/span[1]").text
    end_date = driver.find_element_by_xpath(
        "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[2]/span[1]").text
    remaining_month = driver.find_element_by_xpath(
        "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[3]/span[1]").text
    current_km = driver.find_element_by_xpath(
        "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[2]/td[1]/span[1]").text
    remaining_km = driver.find_element_by_xpath(
        "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[2]/td[2]/span[1]").text
    residual = driver.find_element_by_xpath(
        "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/table/tbody/tr[2]/td[3]/span[1]").text
    car_info_box0 = driver.find_element_by_xpath(
        "/html/body/div[3]/div[2]/div/div[3]/div[1]/div[2]/div[1]") \
        .find_elements(By.CLASS_NAME, "info-content")
    car_info_box1 = driver.find_element_by_xpath(
        "/html/body/div[3]/div[2]/div/div[3]/div[1]/div[2]/div[2]") \
        .find_elements(By.CLASS_NAME, "info-content")

    transaction_fee = car_info_box0[0].text
    security_deposit = car_info_box0[1].text
    fees_per_km_over_limit = car_info_box0[2].text
    car_return_insurance = car_info_box0[3].text
    wheel_insurance = car_info_box0[4].text
    interest_rate = car_info_box0[5].text
    accident = car_info_box1[0].text
    scratch = car_info_box1[1].text
    car_check = car_info_box1[2].text
    color = car_info_box1[3].text
    automatic_manual = car_info_box1[4].text
    drive_mode = car_info_box1[5].text

    expand_config_list()
    config_list = [x.text for x in driver.find_elements(By.CLASS_NAME, "info-car-confi-item")[: -1]]

    try:
        info_car_extra = driver.find_element(By.CLASS_NAME, "info-car-extra").text
    except NoSuchElementException:
        info_car_extra = ""

    today = date.today()

    dict0 = {"_id": car_id,
             "car_model": car_model,
             "car_type": car_type,
             "original_downpay": original_downpay,
             "pay_or_get": pay_or_get,
             "down_pay_amount": down_pay_amount,
             "monthly_payment": monthly_payment,
             "start_date": start_date,
             "end_date": end_date,
             "remaining_month": remaining_month,
             "current_km": current_km,
             "remaining_km": remaining_km,
             "residual": residual,
             "transaction_fee": transaction_fee,
             "security_deposit": security_deposit,
             "fees_per_km_over_limit": fees_per_km_over_limit,
             "car_return_insurance": car_return_insurance,
             "wheel_insurance": wheel_insurance,
             "interest_rate": interest_rate,
             "accident": accident,
             "scratch": scratch,
             "car_check": car_check,
             "color": color,
             "automatic_manual": automatic_manual,
             "drive_mode": drive_mode,
             "config_list": config_list,
             "info_car_extra": info_car_extra,
             "date_added": today.strftime("%B %d, %Y")
             }
    if collection.count_documents({"_id": car_id}) == 0:
        collection.insert_one(dict0)


driver.get('https://www.sparklease.com/')
find_car_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/button[1]")
click_and_wait(find_car_button, "card")
toggle_lease_cash()
toggle_private_dealer()
while not scrapping_done:
    auto_cards = driver.find_elements_by_class_name("card")
    for card in auto_cards:
        if is_car_eligible(card):
            card.click()
            driver.switch_to.window(driver.window_handles[1])
            get_car_info()
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    if is_last_page():
        scrapping_done = True
    else:
        next_page()
driver.quit()
