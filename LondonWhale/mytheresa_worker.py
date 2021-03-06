# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import json
import time
import logging
import common_util as cu
from common_util import locate, locate_s


url='http://click.linksynergy.com/link?id=ynYrPp*y8jg&offerid=572016.13317151633&type=15&murl=https%3A%2F%2Fmytheresa.commander1.com%2Fc3%2F%3Ftcs%3D3504%26chn%3Daff1%26src%3Dlinkshare%26cmp%3Daff_linksh_au%26tarea%3Dhk%26ptyp%3Dfeed%26pub_id%3D%5BSITE.CODE%5D%26pub_name%3D%5BSITE.CODE%5D%26pub_type%3D%5BSITE.CODE%5D%26feed_num%3DP00294590%26feed_des%3DGucci%26feed_mwg%3Dshoes%26url%3Dhttps%253A%252F%252Fwww.mytheresa.com%252Fen-hk%252Fgucci-leather-sandals-945342.html%253Futm_source%253Daffiliate%2526utm_medium%253Daffiliate.linkshare.au'
sizes_in_stock = []


def json_finder(input_text):
    pattern = r'{.+}'
    script = re.findall(pattern, input_text)[0]
    return json.loads(script)


def get_available_sizes(driver):
    global sizes_in_stock
    js_script = locate_s(driver, By.XPATH, './/div[@id="mythccconsole"]/following-sibling::script')[0]\
        .get_attribute('innerHTML')
    js_json = json_finder(js_script)
    product_id = js_json['product']['id']
    sizes_on_stock = js_json['product']['sizesOnStock'].split('|')


def myth_add_to_cart(sku_list, driver):
    for i in range(len(sku_list)):
        sku = sku_list[i]
        if i == 0:
            driver.get(sku['url'])
        else:
            cu.open_new_tab(driver, sku['url'])

        # check style is not sold out
        if locate(driver, By.ID, 'product-addtocart-button').text == 'SOLD OUT':
            raise Exception('sku %s is sold out' % sku['name'])

        # check ordered sku is not sold out
        if cu.element_exist(driver, By.CLASS_NAME, 'size-trigger'):
            locate(driver, By.CLASS_NAME, 'size-trigger').click()
            if cu.element_not_exist(driver, By.CLASS_NAME, 'addtocart-trigger'):
                raise Exception('All sizes sold out for sku %s' % sku['name'])
            available_sizes = locate_s(driver, By.CLASS_NAME, 'addtocart-trigger')
            size_list = [size.text for size in available_sizes]
            order_size = [s for s in size_list if sku['size'] in s]
            if len(order_size) == 0:
                raise Exception('The ordered size is not available for sku %s' % sku['name'])
            # todo: 现在使用第一个匹配sku.size的尺码放入购物车，当size=5、S/M/L/XL 或S/M（网站上text为S-M）时会下单错误
            index = size_list.index(order_size[0])
            available_sizes[index].click()
        else:
            logging.INFO('no size selection, will go with the default size')
        # add to cart
        locate(driver, By.ID, 'product-addtocart-button').click()
    # time.sleep(5)
    # press View Bag button
    locate_s(driver, By.XPATH, ".//div[@class='buttons-set']/a")[0].click()


def myth_verify_cart_total(sku_list, driver):
    cart_names = [n.text for n in locate_s(driver, By.CLASS_NAME, 'product-name')]
    remove_buttons = locate_s(driver, By.CLASS_NAME, 'product-cart-remove-item')
    if len(cart_names) < len(sku_list):
        raise Exception('Cart quantity too little')
    elif len(cart_names) > len(sku_list):
        sku_names = [sku['name'] for sku in sku_list]
        for i in range(len(cart_names)):
            if cart_names[i] not in sku_names:
                remove_buttons[i].click()
                break
        return False
    else:
        return True


def verify_cart_total_wrapper(sku_list, driver):
    for i in range(5):
        if myth_verify_cart_total(sku_list, driver):
            break
        time.sleep(5)  # 等待购物车页面重载
    # 如果5次删减仍过多，直接取消下单
    cart_names = [n.text for n in locate_s(driver, By.CLASS_NAME, 'product-name')]
    if len(cart_names) > len(sku_list):
        raise Exception('Too many items in cart')


def myth_verify_cart_item(sku_list, driver):
    cart_names = [n.text for n in locate_s(driver, By.CLASS_NAME, 'product-name')]
    cart_sizes = [s.text for s in locate_s(driver, By.CLASS_NAME, 'product-size')]
    cart_qtys = [s.get_attribute("value") for s in locate_s(driver, By.XPATH, ".//div[@class='cart-qty-wrapper']/input")]

    if cu.element_exist(driver, By.CLASS_NAME, 'error-msg'):
        # 库存不够
        raise Exception('Not enough stock for ')
        pass
    pass


def check_out(sku_list, driver):
    pass


def pay_paypal():
    pass


def place_mytheresa_order(order_obj):
    # call api记录开始下单
    # log 记录 order_obj
    try:
        driver = webdriver.Chrome('/Users/jiagangzhang/workspace/chromedriver')
        myth_add_to_cart(order_obj['sku_list'], driver)
        verify_cart_total_wrapper(order_obj['sku_list'], driver)

        # api记录confirm
    except Exception as e:
        logging.exception(e)
        driver.save_screenshot(order_obj['order_key'] + '.png')
        # 调api记录下单异常，需人工介入
    finally:
        driver.quit()


if __name__ == '__main__':
    test_order_obj = {

        }
    place_mytheresa_order(test_order_obj)
