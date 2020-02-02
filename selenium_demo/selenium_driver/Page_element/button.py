from selenium_driver.Page_element.page_element import PageElement

class Button(PageElement):
    def __init__(self, base_xpath):
        self.xpath = base_xpath
        print(self.xpath)
        PageElement.__init__(self, self.xpath)

