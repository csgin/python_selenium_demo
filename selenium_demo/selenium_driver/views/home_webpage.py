from  selenium_driver.Page_element.button import Button
from  selenium_driver.Page_element.input_field import InputField
from  selenium_driver.Page_element.multi_select import MultiSelect
from  selenium_driver.Page_element.calendar import Calendar
from  selenium_driver.Page_element.text import Text
from  selenium_driver.Page_element.removeAccents import removeAccents
from  selenium_driver.Page_element.select_element import SelectElement


class Home():
    class Header_Bar():
        def __init__(self):
            self.search_bar_locator = "//div[@class='header-wrapper']"
            self.select_language_locator = 'language_selector_popover'

            self.element = SelectElement(self.search_bar_locator)

            self.select_language = self.element.a_by_aria_controls('language_selector_popover')

        def change_language_to(self, language):
            Button(self.select_language).click()
            language = self.element.span_by_lang(language)
            Button(language).click()

    class Search_Bar():
        def __init__(self):
            self.search_bar_locator = "//div[@data-view='accommodation']"
            self.destination_locator = "Where are you going?"
            self.destination_hints_locator = "search_hl_name"
            self.guests_locator = "xp__input-group xp__guests"
            self.calendar_locator = "xp__dates xp__group"
            self.search_button_locator = "Search"

            self.element = SelectElement(self.search_bar_locator)

            self.search_button = self.element.button_by_text(self.search_button_locator)
            self.destination = self.element.input_by_placeholder(self.destination_locator)
            self.destination_hints = self.element.span_by_class(self.destination_hints_locator)
            self.calendar = self.element.div_by_class(self.calendar_locator)
            self.guests = self.element.div_by_class(self.guests_locator)

        def search_button_should_be_enabled(self):
            Button(self.search_button).should_be_enabled()

        def search_button_should_be_disabled(self):
            Button(self.search_button).should_be_disabled()

        def search_button_should_be_visable(self):
            Button(self.search_button).should_be_visible()

        def click_search_button(self):
            Button(self.search_button).click()

        def fill_in_destination(self, destination):
            InputField(self.destination).send_keys(destination)
            InputField(self.destination).click()

        def get_destinations(self):
            MultiSelect(self.destination_hints).wait_until_visible()
            return MultiSelect(self.destination_hints).get_list_of_elements_inner_HTML()

        def assert_destination(self, destination):
            destinations_from_input_field = self.get_destinations()
            assert removeAccents(destinations_from_input_field[0].split("<br>")[0]) == removeAccents(destination)

        def click_calendar(self):
            MultiSelect(self.calendar).click()

        def click_guests(self):
            MultiSelect(self.guests).click()

        class Calendar():
            def __init__(self):
                Home.Search_Bar.__init__(self)

            def select_dates(self, arrival_date, departure_date):
                """dates should be in str format - like this: 28 February 2020"""
                Calendar(self.element.span_by_aria_label(arrival_date)).click()
                Calendar(self.element.span_by_aria_label(departure_date)).click()

            def get_dates(self):
                check_in = MultiSelect(
                    f"{self.search_bar_locator}//div[@data-placeholder='Check-in']").get_text().split(" ")[1:]
                check_out = MultiSelect(
                    f"{self.search_bar_locator}//div[@data-placeholder='Check-out']").get_text().split(" ")[1:]
                return (check_in, check_out)

            def assert_dates_after_dates_selection(self, arrival_date, departure_date):
                arrival_date = arrival_date.split(" ")[:2]
                departure_date = departure_date.split(" ")[:2]
                arrival_date[1] = arrival_date[1][:3]
                departure_date[1] = departure_date[1][:3]
                dates_from_browser = self.get_dates()
                assert dates_from_browser == (arrival_date, departure_date)

        class Guests():
            def __init__(self):
                Home.Search_Bar.__init__(self)

                self.adult_count = self.element.span_by_id("group_adults_desc")
                self.child_count = self.element.span_by_id("group_children_desc")
                self.room_count = self.element.span_by_id("no_rooms_desc")
                self.add_adult_button = self.element.button_by_aria_label("Increase number of Adults")
                self.add_child_button = self.element.button_by_aria_label("Increase number of Children")
                self.add_room_button = self.element.button_by_aria_label("Increase number of Rooms")
                self.remove_adult_button = self.element.button_by_aria_label("Decrease number of Adults")
                self.remove_child_button = self.element.button_by_aria_label("Decrease number of Children")
                self.remove_room_button = self.element.button_by_aria_label("Decrease number of Rooms")

            def check_child_multiselect_count(self):
                no_of_childs = self.get_child_count()
                for i in range(no_of_childs):
                    MultiSelect(self.element.select_by_aria_label(f"Child {i+1} age")).is_present()

            def check_if_child_multiselect_contains_exacly(self, list):
                no_of_childs = self.get_child_count()
                for i in range(no_of_childs):
                    MultiSelect(self.element.select_by_aria_label(
                        f"Child {i + 1} age") + "//option").should_contain_exacly(list)

            def select_child_age(self, child_index, age):
                MultiSelect(self.element.select_by_aria_label(
                    f"Child {child_index} age")).select_by_text(age)

            def get_selected_age_for_child(self, child_index):
                return MultiSelect(self.element.select_by_aria_label(
                    f"Child {child_index} age")).get_text_from_select()

            def set_adult_count(self, number):
                current = self.get_adult_count()
                counter = number - current
                if counter > 0:
                    for i in range(counter):
                        self._add_adult_guest()
                else:
                    for i in range(abs(counter)):
                        self._remove_adult_guest()

            def set_child_count(self, number):
                current = self.get_child_count()
                counter = number - current
                if counter > 0:
                    for i in range(counter):
                        self._add_child_guest()
                else:
                    for i in range(abs(counter)):
                        self._remove_child_guest()

            def set_room_count(self, number):
                current = self.get_room_count()
                counter = number - current
                if counter > 0:
                    for i in range(counter):
                        self._add_room()
                else:
                    for i in range(abs(counter)):
                        self._remove_room()

            def add_adult_button_should_be_disabled(self):
                Button(self.add_adult_button).should_be_disabled_by_class()

            def add_child_button_should_be_disabled(self):
                Button(self.add_child_button).should_be_disabled_by_class()

            def add_room_button_should_be_disabled(self):
                Button(self.add_room_button).should_be_disabled_by_class()

            def remove_adult_button_should_be_disabled(self):
                Button(self.remove_adult_button).should_be_disabled_by_class()

            def remove_child_button_should_be_disabled(self):
                Button(self.remove_child_button).should_be_disabled_by_class()

            def remove_room_button_should_be_disabled(self):
                Button(self.remove_room_button).should_be_disabled_by_class()

            def add_adult_button_should_be_visible(self):
                Button(self.add_adult_button).should_be_visible()

            def add_child_button_should_be_visible(self):
                Button(self.add_child_button).should_be_visible()

            def add_room_button_should_be_visible(self):
                Button(self.add_room_button).should_be_visible()

            def remove_adult_button_should_be_visible(self):
                Button(self.remove_adult_button).should_be_visible()

            def remove_child_button_should_be_visible(self):
                Button(self.remove_child_button).should_be_visible()

            def remove_room_button_should_be_visible(self):
                Button(self.remove_room_button).should_be_visible()

            def get_adult_count(self):
                return int(Text(self.adult_count).get_attribute('innerHTML').split(" ")[0])

            def get_child_count(self):
                return int(Text(self.child_count).get_attribute('innerHTML').split(" ")[0])

            def get_room_count(self):
                return int(Text(self.room_count).get_attribute('innerHTML').split(" ")[0])

            def _add_adult_guest(self):
                Button(self.add_adult_button).click()

            def _remove_adult_guest(self):
                Button(self.remove_adult_button).click()

            def _add_child_guest(self):
                Button(self.add_child_button).click()

            def _remove_child_guest(self):
                Button(self.remove_child_button).click()

            def _add_room(self):
                Button(self.add_room_button).click()

            def _remove_room(self):
                Button(self.remove_room_button).click()
