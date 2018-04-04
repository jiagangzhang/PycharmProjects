from appium import webdriver
import time

desired_caps = {
    "automationName": "Appium",
    "platformName": "iOS",
    "platformVersion": "10.2",
    "deviceName": "iPhone 7",
    "app": "/Users/jiagangzhang/storefront-ios.app"
    }

print('started')
wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
print('start complete')
try:

    el0 = wd.find_element_by_accessibility_id('skip button')
    print(type(el0))
    # print(len(el0))
    el0.click()
except:
    print('not first login')

time.sleep(5)
try:
    wd.driver.switch_to_alert().accept()
    time.sleep(5)
except:
    print('no alert popup')

el1 = wd.find_element_by_xpath("//XCUIElementTypeButton[@name=\"登录\"]")
el1.click()
el3 = wd.find_element_by_xpath("//XCUIElementTypeTextField[@name=\"LoginMM-UITB_CA_ACCOUNT\"]")
el3.send_keys("perm-mm")
time.sleep(5)
el4 = wd.find_element_by_xpath("//XCUIElementTypeSecureTextField[@name=\"LoginMM-UITB_CA_PASSWORD\"]")
el4.send_keys("Bart")
time.sleep(5)
el5 = wd.find_element_by_xpath("//XCUIElementTypeButton[@name=\"LoginMM-UIBT_LOGIN\"]")
el5.click()
print('key sent')
time.sleep(20)
wd.quit()
print('close')
