from selenium import webdriver
import time
import logging
import common_util as cu


url='http://click.linksynergy.com/link?id=ynYrPp*y8jg&offerid=572016.13317151633&type=15&murl=https%3A%2F%2Fmytheresa.commander1.com%2Fc3%2F%3Ftcs%3D3504%26chn%3Daff1%26src%3Dlinkshare%26cmp%3Daff_linksh_au%26tarea%3Dhk%26ptyp%3Dfeed%26pub_id%3D%5BSITE.CODE%5D%26pub_name%3D%5BSITE.CODE%5D%26pub_type%3D%5BSITE.CODE%5D%26feed_num%3DP00294590%26feed_des%3DGucci%26feed_mwg%3Dshoes%26url%3Dhttps%253A%252F%252Fwww.mytheresa.com%252Fen-hk%252Fgucci-leather-sandals-945342.html%253Futm_source%253Daffiliate%2526utm_medium%253Daffiliate.linkshare.au'


def mytheresa_add_to_cart(sku_list, driver):
    for i in range(len(sku_list)):
        sku = sku_list[i]
        if i == 0:
            driver.get(sku.url)
        else:
            # driver.execute_script('''window.open("%s","_blank");''' % sku.url)
            cu.open_new_tab(driver, sku.url)
        # check style is not sold out
        if driver.find_element_by_id('product-addtocart-button').text == 'SOLD OUT':
            logging.INFO('sku %s is sold out' % sku.name)
            raise Exception('sku %s is sold out' % sku.name)

        # check ordered sku is not sold out
        if cu.element_exist(driver, 'class_name', 'size-trigger'):
            driver.find_element_by_class_name('size-trigger').click()
            if cu.element_not_exist(driver, 'class_name', 'addtocart-trigger'):
                logging.WARN('All sizes sold out for sku %s' % sku.name)
                # take screen shot
                raise Exception('All sizes sold out for sku %s' % sku.name)
            available_sizes = driver.find_elements_by_class_name('addtocart-trigger')
            size_list = [size.text for size in available_sizes]
            order_size = [s for s in size_list if sku.size in s]
            if len(order_size) == 0:
                logging.WARN('The ordered size is not available for sku %s' % sku.name)
                # take screen shot
                raise Exception('The ordered size is not available for sku %s' % sku.name)
            # todo: 现在使用第一个匹配sku.size的尺码放入购物车，当size=5、S/M/L/XL 或S/M（网站上text为S-M）时会下单错误
            index = size_list.index(order_size[0])
            available_sizes[index].click()
        else:
            logging.INFO('no size selection, will go with the default size')

        # choose color, not implemented
        # add to cart
        pass


def pay_paypal():
    pass


def place_mytheresa_order(order_obj):
    """
    don't forget size and color
    """
    try:
        driver = webdriver.Chrome('/Users/jiagangzhang/workspace/chromedriver')
        # for sku in order_obj.sku_list:
        mytheresa_add_to_cart(order_obj.sku_list, driver)

        # # driver.get(url)
        # if order_obj.size:
        #     size_trigger = driver.find_element_by_class_name('size-trigger')
        #     # todo: add check, whether the size is in stock (no 'add to wishlist' shown)
        #     size_trigger.click()
        # if order_obj.color:
        #     # choose color
        #     pass

        # time.sleep(20)
    except Exception as e:
        logging.exception(e)
    finally:
        driver.save_screenshot(order_obj.order_key+'.png')
        driver.quit()


if __name__ == '__main__':
    test_order_obj = {

        }
    place_mytheresa_order(test_order_obj)
