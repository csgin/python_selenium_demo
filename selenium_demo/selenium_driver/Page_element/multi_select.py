from selenium_driver.Page_element.page_element import PageElement
from selenium.webdriver.common.by import By

class MultiSelect(PageElement):
    def __init__(self, base_xpath):
        self.xpath = base_xpath
        print(self.xpath)
        PageElement.__init__(self, self.xpath)

    def should_contain_exacly(self, list):
        list_of_web_elements = self.driver.find_elements(By.XPATH, self.xpath)
        assert len(list_of_web_elements) == len(list)
        assert list == [i.text.strip() for i in list_of_web_elements]

    def get_text_from_select(self):
        element = self.driver.find_element(By.XPATH, self.xpath)
        value = element.get_attribute("value")
        return self.driver.find_element(By.XPATH, self.xpath + f"//option[@value='{value}']").text.strip()