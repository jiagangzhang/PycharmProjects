import time
import traceback
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# url='http://click.linksynergy.com/link?id=ynYrPp*y8jg&offerid=572016.13317151633&type=15&murl=https%3A%2F%2Fmytheresa.commander1.com%2Fc3%2F%3Ftcs%3D3504%26chn%3Daff1%26src%3Dlinkshare%26cmp%3Daff_linksh_au%26tarea%3Dhk%26ptyp%3Dfeed%26pub_id%3D%5BSITE.CODE%5D%26pub_name%3D%5BSITE.CODE%5D%26pub_type%3D%5BSITE.CODE%5D%26feed_num%3DP00294590%26feed_des%3DGucci%26feed_mwg%3Dshoes%26url%3Dhttps%253A%252F%252Fwww.mytheresa.com%252Fen-hk%252Fgucci-leather-sandals-945342.html%253Futm_source%253Daffiliate%2526utm_medium%253Daffiliate.linkshare.au'
# url='http://click.linksynergy.com/link?id=ynYrPp*y8jg&offerid=572016.12456801024&type=15&murl=https%3A%2F%2Fmytheresa.commander1.com%2Fc3%2F%3Ftcs%3D3504%26chn%3Daff1%26src%3Dlinkshare%26cmp%3Daff_linksh_au%26tarea%3Dhk%26ptyp%3Dfeed%26pub_id%3D%5BSITE.CODE%5D%26pub_name%3D%5BSITE.CODE%5D%26pub_type%3D%5BSITE.CODE%5D%26feed_num%3DP00311822%26feed_des%3DSimone%2BRocha%26feed_mwg%3Daccessoires%26url%3Dhttps%253A%252F%252Fwww.mytheresa.com%252Fen-hk%252Fsimone-rocha-crystal-and-faux-pearl-earrings-927522.html%253Futm_source%253Daffiliate%2526utm_medium%253Daffiliate.linkshare.au'
url = 'http://click.linksynergy.com/link?id=ynYrPp*y8jg&offerid=572016.12456774922&type=15&murl=https%3A%2F%2Fmytheresa.commander1.com%2Fc3%2F%3Ftcs%3D3504%26chn%3Daff1%26src%3Dlinkshare%26cmp%3Daff_linksh_au%26tarea%3Dhk%26ptyp%3Dfeed%26pub_id%3D%5BSITE.CODE%5D%26pub_name%3D%5BSITE.CODE%5D%26pub_type%3D%5BSITE.CODE%5D%26feed_num%3DP00300920%26feed_des%3DGucci%26feed_mwg%3Daccessoires%26url%3Dhttps%253A%252F%252Fwww.mytheresa.com%252Fen-hk%252Fgucci-butterfly-striped-belt-971965.html%253Futm_source%253Daffiliate%2526utm_medium%253Daffiliate.linkshare.au'
url2 = 'http://click.linksynergy.com/link?id=ynYrPp*y8jg&offerid=572016.12456774934&type=15&murl=https%3A%2F%2Fmytheresa.commander1.com%2Fc3%2F%3Ftcs%3D3504%26chn%3Daff1%26src%3Dlinkshare%26cmp%3Daff_linksh_au%26tarea%3Dhk%26ptyp%3Dfeed%26pub_id%3D%5BSITE.CODE%5D%26pub_name%3D%5BSITE.CODE%5D%26pub_type%3D%5BSITE.CODE%5D%26feed_num%3DP00300923%26feed_des%3DGucci%26feed_mwg%3Daccessoires%26url%3Dhttps%253A%252F%252Fwww.mytheresa.com%252Fen-hk%252Fgucci-crystal-embellished-leather-belt-967679.html%253Futm_source%253Daffiliate%2526utm_medium%253Daffiliate.linkshare.au'


# def open_new_tab(driver, url):
#     driver.execute_script('''window.open("%s","_blank");''' % url)

def open_new_tab(driver, url):
    driver.execute_script('''window.open("%s","_blank");''' % url)
    driver.switch_to_window(driver.window_handles[-1])
    time.sleep(5)


def locate(driver, by, path):
    return WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((by, path))
        )


def locate_s(driver, by, path):
    """
    :return: list of elements
    """
    return WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((by, path))
        )


def re_finder(input_text):
    pattern = r'{.+}'
    js = re.findall(pattern, input_text)[0]
    return json.loads(js)


driver = webdriver.Chrome(
    '/Users/jiagangzhang/workspace/chromedriver')  # Optional argument, if not specified will search path.

driver.get(url)

try:
    # text=driver.find_element_by_id('product-addtocart-button').text
    text = driver.find_element(By.ID, 'product-addtocart-button').text
    size_trigger = driver.find_element_by_class_name('size-trigger')
    size_trigger.click()

    s = locate_s(driver, By.XPATH, './/div[@id="mythccconsole"]/following-sibling::script')[0]
    js_code = s.get_attribute('innerHTML')
    code = re_finder(js_code)
    print(code['product']['id'])
    raise Exception('end')

    available_sizes = locate_s(driver, By.CLASS_NAME, 'addtocart-trigger')
    available_sizes[0].click()
    driver.find_element_by_id('product-addtocart-button').click()
    # time.sleep(5)
    locate_s(driver, By.XPATH, ".//div[@class='buttons-set']/a")[0].click()

    time.sleep(5)
    qtys = locate_s(driver, By.XPATH, ".//div[@class='cart-qty-wrapper']/input")
    # qtys = driver.find_elements_by_xpath(".//div[@class='cart-qty-wrapper']/input")
    for i in qtys:
        value = i.get_attribute("value")
        print(value)
        print(type(value))

# try:
# 	for i in range(3):
# 		size_trigger = driver.find_element_by_class_name('size-trigger')
# 		size_trigger.click()
# 		sizes = driver.find_elements_by_xpath(".//ul[@class='sizes']/li")
# 		sizes[2].click()
# 		driver.find_element_by_id('product-addtocart-button').click()
# 		time.sleep(5)
# 		open_new_tab(driver, url2)
# except Exception as e:
# 	print(e)
# 	driver.save_screenshot('blablabla.png')

# mytheresa = driver.window_handles[0]
# try:
# 	purchase_button = driver.find_element_by_name('braintree-paypal-button')
# 	print('Found')
# 	purchase_button.click()

except Exception as e:
    exstr = traceback.format_exc()
    print(exstr)
time.sleep(20)

# paypal_window = driver.window_handles[1]
# driver.switch_to_window(paypal_window)
# card_number = driver.find_element_by_name('cardNumber')
# card_number.send_keys('1234567890')
# print ('found')
# time.sleep(10)
driver.quit()
