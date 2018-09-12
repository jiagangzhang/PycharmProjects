import logging
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
locators = ['id',
            'name',
            'xpath',
            'link_text',
            'class_name'
            ]
wait_time = 5  # set to configable number later


def locate(driver, by, path):
    return WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((by, path))
        )


def locate_s(driver, by, path):
    """
    :return: list of elements
    """
    return WebDriverWait(driver, wait_time).until(
        EC.presence_of_all_elements_located((by, path))
        )


def setup_logger(logfile_name, logfile_path):
    logger = logging.getLogger(logfile_name)
    formatter = logging.Formatter('%(asctime)s:   %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    filehandler = logging.FileHandler(logfile_path, mode='w')
    filehandler.setFormatter(formatter)
    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(filehandler)
    logger.addHandler(streamhandler)
    return logger


def element_not_exist(driver, by, path):
    return not element_exist(driver, by, path)


def element_exist(driver, by, path):
    # if by.lower() not in locators:
    #     raise ValueError('Please provide legal method name, the method provided is by_%s' % by)
    # locate_method = getattr(driver, 'find_element_by_' + by.lower())
    try:
        locate(driver, by, path)
        return True
    except:
        return False


def open_new_tab(driver, url):
    driver.execute_script('''window.open("%s","_blank");''' % url)
    driver.switch_to_window(driver.window_handles[-1])
    time.sleep(5)


def main():
    """
    unit test function
    """
    from selenium import webdriver
    test_driver = webdriver.Chrome('/Users/jiagangzhang/workspace/chromedriver')
    test_driver.get('https://www.baidu.com')
    assert element_exist(test_driver, 'id', 'kw')
    assert element_not_exist(test_driver, 'id', 'q')
    test_driver.quit()


if __name__ == '__main__':
    main()





