class SelectElement():
    def __init__(self, xpath):
        self.xpath = xpath

    def button_by_text(self, button_text):
        return self.xpath + f'//button[normalize-space() = "{button_text}"]'

    def button_by_aria_label(self, button_aria_label):
        return self.xpath + f"//button[@aria-label='{button_aria_label}']"

    def input_by_placeholder(self, placeholder):
        return self.xpath + f"//input[@placeholder='{placeholder}']"

    def div_by_class(self, class_name):
        return self.xpath + f"//div[@class='{class_name}']"

    def span_by_aria_label(self, aria_label):
        return self.xpath + f"//span[@aria-label='{aria_label}']"

    def span_by_id(self, id):
        return self.xpath + f"//span[@id='{id}']"

    def span_by_lang(self, lang):
        return self.xpath + f"//span[@lang='{lang}']"

    def span_by_class(self, class_name):
        return self.xpath + f"//span[@class='{class_name}']"

    def select_by_aria_label(self, aria_label):
        return self.xpath + f"//select[@aria-label='{aria_label}']"

    def a_by_aria_controls(self, aria_controls):
        return self.xpath + f"//a[@aria-controls='{aria_controls}']"
