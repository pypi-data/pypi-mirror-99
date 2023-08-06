from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
class BasePageElement(object):
    """Base page class that is initialized on every page object class."""
    is_clear_text=True
    delay=100
    is_find_hide=False
    is_click_on=False
    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        try:
            if self.is_find_hide:
                WebDriverWait(driver, self.delay).until(
                    EC.presence_of_element_located(self.locator))
            else:
                WebDriverWait(driver, self.delay).until(
                    EC.visibility_of_element_located(self.locator))
            element = driver.find_element(*self.locator)
            if self.is_clear_text:
                element.clear()
            if self.is_click_on:
                element.click()
                element = driver.find_element(*self.locator)
            element.send_keys(value)
        except Exception as e:
            print("Error BasePageELement",str(e))
            traceback.print_exc()
            pass
    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver,  self.delay).until(EC.visibility_of_element_located(self.locator))
        element = driver.find_element(*self.locator)
        return element.get_attribute("href")
