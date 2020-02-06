from time import sleep

from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, TimeoutException, \
    WebDriverException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import selenium_driver.setup.selenium_setup as se



class PageElement:
    def __init__(self, xpath):
        """
        Constructs a PageElement object which represents a DOM element.
        Every class supposed to represent a DOM element should inherit from this base class.
        :param xpath: DOM element locator. Only xpaths are used.
        """
        self.xpath = xpath
        self.driver = se.browser()

    def is_present(self):
        """
        Checks if page contains the element. The check is immediate.
        :return: True if page contains the element, otherwise False is returned.
        """
        try:
            self.driver.find_element(By.XPATH, self.xpath)
            return True
        except NoSuchElementException:
            return False

    def should_be_present(self, timeout=10.0):
        """
        Checks if page contains the element and raises NoSuchElementException if it is not found after the set timeout.
        This method should be used when the test is supposed to fail in case of the missing element.
        :param timeout: Timeout value in seconds.
        :return: None.
        """
        if not self.wait_until_present(timeout):
            raise NoSuchElementException(f'Page did not contain element after {timeout} seconds: {self.xpath}')

    def wait_until_present(self, timeout=10.0):
        """
        Checks if page contains the element and returns False if it is not found after the set timeout.
        :param timeout: Timeout value in seconds.
        :return: True if the element was found before the set timeout was reached, otherwise False.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                expected_conditions.presence_of_element_located((By.XPATH, self.xpath))
            )
            return True
        except TimeoutException:
            return False

    def should_not_be_present(self, timeout=10.0):
        """
        Checks if page does not contain the element and raises WebDriverException if it is still present after the set timeout.
        This method should be used when the test is supposed to fail in case the page still contains the element.
        :param timeout: Timeout value in seconds.
        :return: None.
        """
        if not self.wait_until_not_present(timeout):
            raise WebDriverException(f'Page still contained element after {timeout} seconds: {self.xpath}')

    def wait_until_not_present(self, timeout=10.0):
        """
        Checks if page does not contain the element and returns False if it is still present after the set timeout.
        :param timeout: Timeout value in seconds.
        :return: True if the element disappeared before the set timeout was reached, otherwise False.
        """
        try:
            WebDriverWait(self.driver, timeout).until_not(
                expected_conditions.presence_of_element_located((By.XPATH, self.xpath))
            )
            return True
        except TimeoutException:
            return False

    def get_count(self):
        """
        Get the number of DOM elements matched by the element's xpath.
        :return: Integer equal to the matched DOM elements.
        """
        return len(self.driver.find_elements(By.XPATH, self.xpath))

    def get_list_of_elements(self):
        """
        Get DOM elements matched by the element's xpath.
        :return: list of element.text() found in DOM by xpath.
        """
        elements = self.driver.find_elements(By.XPATH, self.xpath)
        list_of_elements = []
        for element in elements:
            list_of_elements.append(element.text)
        return list_of_elements

    def get_list_of_elements_inner_HTML(self):
        """
        Get DOM elements matched by the element's xpath.
        :return: list of element.text() found in DOM by xpath.
        """
        elements = self.driver.find_elements(By.XPATH, self.xpath)
        list_of_elements = []
        for element in elements:
            list_of_elements.append(element.get_attribute('innerHTML'))
        return list_of_elements

    def should_match_x_times(self, number):
        """
        Checks if there are exactly 'number' of DOM elements matched by the element's xpath and raises Exception
        if that's not true. This method should be used when the test is supposed to fail in case the number of elements
        is different than expected.
        :return: None.
        """
        xpath_count = len(self.driver.find_elements(By.XPATH, self.xpath))
        if xpath_count != number:
            raise Exception(
                f'Page was supposed to contain {number}, but contains {xpath_count} element(s): {self.xpath}')

    def is_visible(self):
        """
        Checks if the element is visible. The check is immediate.
        :return: True if the element is visible, otherwise False is returned.
        """
        try:
            self.driver.find_element(By.XPATH, self.xpath).is_displayed()
            return True
        except NoSuchElementException or ElementNotVisibleException:
            return False

    def should_be_visible(self, timeout=10.0):
        """
        Checks if the element is visible and raises ElementNotVisibleException if it is not after the set timeout.
        This method should be used when the test is supposed to fail in case the element is not visible.
        :param timeout: Timeout value in seconds.
        :return: None.
        """
        if not self.wait_until_visible(timeout):
            raise ElementNotVisibleException(
                f'Element was supposed to be visible in {timeout} seconds but was not: {self.xpath}')

    def wait_until_visible(self, timeout=10.0):
        """
        Checks if the element is visible and returns False if it is not after the set timeout.
        :param timeout: Timeout value in seconds.
        :return: True if the element became visible before the set timeout was reached, otherwise False.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                expected_conditions.visibility_of_element_located((By.XPATH, self.xpath))
            )
            return True
        except TimeoutException:
            return False

    def should_not_be_visible(self, timeout=10.0):
        """
        Checks if the element is not visible and raises WebDriverException if it is still visible after the set timeout.
        This method should be used when the test is supposed to fail in case the element is visible.
        :param timeout: Timeout value in seconds.
        :return: None.
        """
        if not self.wait_until_not_visible(timeout):
            raise WebDriverException(f'Element was still visible after {timeout} seconds: {self.xpath}')

    def wait_until_not_visible(self, timeout=10.0):
        """
        Checks if the element is not visible and returns False if it is still visible after the set timeout.
        :param timeout: Timeout value in seconds.
        :return: True if the element became invisible before the set timeout was reached, otherwise False.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                expected_conditions.invisibility_of_element_located((By.XPATH, self.xpath))
            )
            return True
        except TimeoutException:
            return False

    def scroll_to(self):
        """
        Scrolls to the center of the element. If the element does not exist, NoSuchElementException is raised.
        :return: None.
        """
        try:
            element = self.driver.find_element(By.XPATH, self.xpath)
            ActionChains(self.driver).move_to_element(element).perform()
            ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
        except NoSuchElementException:
            raise NoSuchElementException(f'Cannot scroll to element: {self.xpath}')

    def scroll_to_js(self):
        try:
            element = self.driver.find_element(By.XPATH, self.xpath)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        except NoSuchElementException:
            raise NoSuchElementException(f'Cannot scroll to element: {self.xpath}')

    def scroll_to_with_offset(self, x_offset, y_offset):
        """
        Scrolls to the part of the element specified by x_offset and y_offset. Offsets are relative to the top-left
        corner of the element. If the element does not exist, NoSuchElementException is raised.
        :param x_offset: Horizontal offset in pixels.
        :param y_offset: Vertical offset in pixels.
        :return: None.
        """
        try:
            element = self.driver.find_element(By.XPATH, self.xpath)
            ActionChains(self.driver).move_to_element_with_offset(element, x_offset, y_offset).perform()
        except NoSuchElementException:
            raise NoSuchElementException(f'Cannot scroll to element: {self.xpath}')

    def scroll_to_in_vs_repeat_container(self, container, load_timeout=0.1, iterations_limit=30):
        """
        Searches for the element in the given vs-repeat container (PageElement) in iterations. Each iteration
        loads another part of vs-repeat content, until:
        - the element is found. In this case the element is scrolled to.
        - the element is not found and there is no more vs-repeat content to be loaded. In this case WebDriverException
          is raised.
        - the element is not found and iteration_limit is reached. In this case WebDriverException is raised.
        :param container: PageElement corresponding to the vs-repeat container.
        :param load_timeout: Maximum expected time it takes new vs-repeat content to load each iteration.
        :param iterations_limit: Maximum number of iterations. This is to avoid searching through very large containers.
        :return: None.
        """
        before_content_tr = PageElement(
            f'{container.xpath}//tr[contains(@class, "vs-repeat-before-content")]')
        after_content_tr = PageElement(
            f'{container.xpath}//tr[contains(@class, "vs-repeat-after-content")]')
        after_content_tr_empty = PageElement(
            f'{container.xpath}//tr[contains(@class, "vs-repeat-after-content") and contains(@style, "height: 0px")]')
        before_content_tr.scroll_to_with_offset(0, 0)
        for _ in range(iterations_limit):
            if self.wait_until_present(load_timeout):
                self.scroll_to()
                return
            elif after_content_tr_empty.wait_until_present(load_timeout):
                raise WebDriverException(f'Element {self.xpath} not found in vs-repeat container: {container.xpath}')
            else:
                after_content_tr.scroll_to_with_offset(0, 0)
        raise WebDriverException(
            f'Element {self.xpath} not found in vs-repeat container in {iterations_limit} iterations: {container.xpath}'
        )

    def mouse_over(self):
        """
        Waits until the element is visible and then performs a mouse over action over it.
        :return: None.
        """
        if self.wait_until_visible():
            element = self.driver.find_element(By.XPATH, self.xpath)
            ActionChains(self.driver).move_to_element(element).perform()
        else:
            raise TimeoutException(f'Element cannot be moused over: {self.xpath}')

    def mouse_over_and_click_another_element(self, another_element):
        """
        Waits until the element is visible and then performs a mouse over action over it. After that it clicks
        another_element that is supposed to become visible when the element is moused over.
        :param another_element: PageElement object representing the element that's supposed to be clicked.
        :return: None.
        """
        if self.wait_until_visible():
            actions = ActionChains(self.driver)
            actions.move_to_element(self.driver.find_element(By.XPATH, self.xpath))
            actions.click(self.driver.find_element(By.XPATH, another_element.xpath))
            actions.perform()
        else:
            raise TimeoutException(f'Cannot click {another_element.xpath} after mousing over: {self.xpath}')

    def click(self):
        """
        Waits until the element is visible and then clicks on it. Raises ElementNotVisibleException if the element
        is not visible or WebDriverException in case of a different failure reason.
        :return: None.
        """
        try:
            if self.wait_until_visible():
                self.driver.find_element(By.XPATH, self.xpath).click()
            else:
                raise ElementNotVisibleException(f'Element cannot be clicked, because it was not visible: {self.xpath}')
        except WebDriverException:
            raise WebDriverException(f'Element cannot be clicked: {self.xpath}')

    def double_click(self):
        """
        Waits until the element is visible and then double clicks on it. Raises ElementNotVisibleException if the element
        is not visible or WebDriverException in case of a different failure reason.
        :return: None.
        """
        try:
            if self.wait_until_visible():
                ActionChains(self.driver).double_click(self.driver.find_element(By.XPATH, self.xpath)).perform()
            else:
                raise ElementNotVisibleException(
                    f'Element cannot be double clicked, because it was not visible: {self.xpath}')
        except WebDriverException:
            raise WebDriverException(f'Element cannot be double clicked: {self.xpath}')

    def click_with_offset(self, x_offset, y_offset):
        """
        Waits until the element is visible and then clicks it with the given offsets. Raises ElementNotVisibleException
        if the element is not visible or WebDriverException in case of a different failure reason.
        :param x_offset: Horizontal offset in pixels.
        :param y_offset: Vertical offset in pixels.
        :return: None.
        """
        try:
            if self.wait_until_visible():
                actions = ActionChains(self.driver)
                actions.move_to_element_with_offset(self.driver.find_element(By.XPATH, self.xpath), x_offset, y_offset)
                actions.click()
                actions.perform()
            else:
                raise ElementNotVisibleException(f'Element cannot be clicked, because it was not visible: {self.xpath}')
        except WebDriverException:
            raise WebDriverException(f'Element cannot be clicked: {self.xpath}')

    def long_press(self):
        """
        Waits until the element is visible and then press on it. Raises ElementNotVisibleException if the element
        is not visible or WebDriverException in case of a different failure reason.
        W3 webdriver has touch/longclick action but currently our driver doesn't support, so use flick instead.
        :return: None.
        """
        try:
            if self.wait_until_visible():
                action = TouchActions(self.driver)
                action.flick_element(self.driver.find_element(By.XPATH, self.xpath), 0, 10, 5).perform()
            else:
                raise ElementNotVisibleException(
                    f'Element cannot be pressed, because it was not visible: {self.xpath}')
        except WebDriverException:
            raise WebDriverException(f'Element cannot be pressed: {self.xpath}')

    def get_text(self):
        """
        Waits until the element is present and then retrieves its text.
        :return: String equal to the element's text.
        """
        if self.wait_until_present():
            return self.driver.find_element(By.XPATH, self.xpath).text
        else:
            raise TimeoutException(f'Cannot get element text: {self.xpath}')

    def get_attribute(self, attribute):
        """
        Waits until the element is present and then retrieves its specified attribute.
        Example usage:
            self.get_attribute('value') will retrieve value of the 'value' attribute
        :param attribute: Attribute to be retrieved (string).
        :return: String equal to the element's attribute's value.
        """
        for _ in range(0, 4):
            if self.wait_until_present():
                try:
                    return self.driver.find_element(By.XPATH, self.xpath).get_attribute(attribute)
                except StaleElementReferenceException:
                    sleep(0.25)
                    pass
        raise TimeoutException(f'Cannot get element attribute {attribute}: {self.xpath}')

    def tag_name(self):
        """
        Waits until the element is present and then retrieves its specified HTML tag.
        Example usage:
            self.tag_name('value') will retrieve value of the 'value' attribute
        :return: String equal to the element's HTML tag name.
        """
        if self.wait_until_present():
            return self.driver.find_element(By.XPATH, self.xpath).tag_name
        else:
            raise TimeoutException(f'Cannot get element HTML tag name: {self.xpath}')

    def send_keys(self, data):
        """
        Waits until the element is visible and then sends keys from data to it.
        :param data: String to be sent to the element.
        :return: None.
        """
        if self.wait_until_visible():
            self.driver.find_element(By.XPATH, self.xpath).send_keys(data)
        else:
            raise TimeoutException(f'Cannot send keys to element: {self.xpath}')

    def clear(self):
        """
        Waits until the element is visible and then clears it.
        :return: None.
        """
        if self.wait_until_visible():
            self.driver.find_element(By.XPATH, self.xpath).clear()
        else:
            raise TimeoutException(f'Cannot clear element: {self.xpath}')

    def should_be_enabled(self):
        """
        Waits until the element is visible and checks if it is enabled.
        :return: None.
        """
        PageElement(f'{self.xpath}[not(@disabled)]').should_be_visible()

    def should_be_disabled(self):
        """
        Waits until the element is visible and checks if it is disabled.
        :return: None.
        """
        PageElement(f'{self.xpath}[@disabled]').should_be_visible()

    def should_be_disabled_by_class(self):
        """
        Waits until the element is visible and checks if its class contains 'disabled' text
        :return: None.
        """
        PageElement(f'{self.xpath}[contains(@class,"disabled")]').should_be_visible()

    def get_css_property(self, property):
        """
        Waits until the element is present and then retrieves its css property.
        Example usage:
            self.get_css_property('value') will retrieve value of the 'value' css property
        :param attribute: CSS property to be retrieved (string).
        :return: String equal to the element's css property's value.
        """
        if self.wait_until_present():
            return self.driver.find_element(By.XPATH, self.xpath).value_of_css_property(property)
        else:
            raise TimeoutException(f'Cannot get element CSS property {property}: {self.xpath}')

    def select_by_text(self, visible_text):
        try:
            Select(self.driver.find_element(By.XPATH, self.xpath)).select_by_visible_text(visible_text)
            return True
        except ElementNotVisibleException:
            return False
