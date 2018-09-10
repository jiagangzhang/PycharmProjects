from selenium import webdriver
import time
import logging
import common_util as cu


url='http://click.linksynergy.com/link?id=ynYrPp*y8jg&offerid=572016.13317151633&type=15&murl=https%3A%2F%2Fmytheresa.commander1.com%2Fc3%2F%3Ftcs%3D3504%26chn%3Daff1%26src%3Dlinkshare%26cmp%3Daff_linksh_au%26tarea%3Dhk%26ptyp%3Dfeed%26pub_id%3D%5BSITE.CODE%5D%26pub_name%3D%5BSITE.CODE%5D%26pub_type%3D%5BSITE.CODE%5D%26feed_num%3DP00294590%26feed_des%3DGucci%26feed_mwg%3Dshoes%26url%3Dhttps%253A%252F%252Fwww.mytheresa.com%252Fen-hk%252Fgucci-leather-sandals-945342.html%253Futm_source%253Daffiliate%2526utm_medium%253Daffiliate.linkshare.au'


def mytheresa_add_to_cart(sku, driver):
    driver.get(sku.url)
    # check style is not sold out
    if driver.find_element_by_id('product-addtocart-button').text == 'SOLD OUT':
        logging.INFO('sku %s is sold out' % sku.name)
        raise Exception('sku %s is sold out' % sku.name)

    # check ordered sku is not sold out


def pay_paypal():
    pass


def place_mytheresa_order(order_obj):
    """
    don't forget size and color
    """
    try:
        driver = webdriver.Chrome('/Users/jiagangzhang/workspace/chromedriver')
        for sku in order_obj.sku_list:
            mytheresa_add_to_cart(sku, driver)

        # driver.get(url)
        # todo : if SOLD OUT present,
        if order_obj.size:
            size_trigger = driver.find_element_by_class_name('size-trigger')
            # todo: add check, whether the size is in stock (no 'add to wishlist' shown)
            size_trigger.click()
        if order_obj.color:
            # choose color
            pass

        # time.sleep(20)
    except Exception as e:
        logging.exception(e)
    finally:
        driver.quit()