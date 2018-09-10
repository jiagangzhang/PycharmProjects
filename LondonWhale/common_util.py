locators = ['id',
            'name',
            'xpath',
            'link_text',
            'class_name'
            ]


def element_not_exist(driver, by, element):
    return not element_exist(driver, by, element)


def element_exist(driver, by, element):
    if by.lower() not in locators:
        raise ValueError('Please provide legal method name, the method provided is by_%s' % by)
    locate_method = getattr(driver, 'find_element_by_' + by.lower())
    try:
        locate_method(element)
        return True
    except:
        return False


def test():
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
    test()





