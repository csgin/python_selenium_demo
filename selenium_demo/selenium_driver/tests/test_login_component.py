import selenium_driver.setup.selenium_setup as se
from selenium_driver.views.home_webpage import Home
import datetime

multiselect_child_age = ["Age at check-out",
                                                         "0 years old",
                                                         "1 year old",
                                                         "2 years old",
                                                         "3 years old",
                                                         "4 years old",
                                                         "5 years old",
                                                         "6 years old",
                                                         "7 years old",
                                                         "8 years old",
                                                         "9 years old",
                                                         "10 years old",
                                                         "11 years old",
                                                         "12 years old",
                                                         "13 years old",
                                                         "14 years old",
                                                         "15 years old",
                                                         "16 years old",
                                                         "17 years old",]


check_in = datetime.datetime.now()
check_out = check_in + datetime.timedelta(days=7)

current_view = se.return_driver()
current_view = current_view.get("https://www.booking.com/")

header = Home().Header_Bar()
header.change_language_to('en-gb')

search_bar = Home().Search_Bar()
search_bar.search_button_should_be_enabled()
search_bar.search_button_should_be_visable()
search_bar.fill_in_destination("Wrocław")
search_bar.assert_destination("Wrocław")

search_bar.click_calendar()
search_bar.Calendar().select_dates(check_in.strftime("%#d %B %Y"), check_out.strftime("%#d %B %Y"))
search_bar.Calendar().assert_dates_after_dates_selection(check_in.strftime("%#d %B %Y"), check_out.strftime("%#d %B %Y"))

search_bar.click_guests()
current_step = search_bar.Guests()
current_step.set_adult_count(30)
assert current_step.get_adult_count() == 30
current_step.set_child_count(4)
assert  current_step.get_child_count() == 4
current_step.check_child_multiselect_count()

for age in multiselect_child_age:
    current_step.select_child_age(2, age)
    assert current_step.get_selected_age_for_child(2) == age


current_step.check_if_child_multiselect_contains_exacly(multiselect_child_age)
current_step.set_room_count(30)
assert current_step.get_room_count() == 30
current_step.set_child_count(10)

current_step.add_room_button_should_be_disabled()
current_step.add_child_button_should_be_disabled()
current_step.add_adult_button_should_be_disabled()

current_step.set_adult_count(1)
assert current_step.get_adult_count() == 1
current_step.set_child_count(0)
assert  current_step.get_child_count() == 0
current_step.set_room_count(1)
assert current_step.get_room_count() == 1

current_step.remove_room_button_should_be_disabled()
current_step.remove_child_button_should_be_disabled()
current_step.remove_adult_button_should_be_disabled()

search_bar.click_search_button()
