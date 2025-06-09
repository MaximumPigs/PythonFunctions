from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Instanciate driver

def webdriver_detached_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    
    return webdriver.Chrome(options=chrome_options)

# Basic functions

def webdriver_open_page(driver, url):
    driver.get(url)


def driver_close_tab(driver):
    driver.close()


def driver_quit(driver):
    driver.quit()


# Find elements

def driver_get_element(driver, by, value):

    def class_(driver, class_):
        return driver.find_element(By.CLASS_NAME, value=class_)

    def name(driver, name):
        return driver.find_element(By.NAME, value=name)

    def tag(driver, tag):
        return driver.find_element(By.TAG_NAME, value=tag)

    def id(driver, id):
        return driver.find_element(By.ID, value=id)

    def css_selector(driver, selector):
        return driver.find_element(By.CSS_SELECTOR, value=selector)

    def link_text(driver, link):
        return driver.find_element(By.LINK_TEXT, value=link)
    
    return by(driver, value)
    
def driver_get_element_by_xpath(driver, tag, attribute, value):
    return driver.find_element(By.XPATH, value=f"//{ tag }[{ attribute }='{ value }']")

# Interact with elements

def element_get_tag_name(element):
    return element.tag_name

def element_get_attribute(element, attribute):
    return element.get_attribute(attribute)

def element_get_size(element):
    return element.size

def element_click(element):
    element.click()

def element_send_keys(element, keys):
    element.send_keys(keys)

def element_send_enter(element):
    element.send_keys(Keys.ENTER)
    