from selenium_driver.setup.selenium_setup import chrome_handler
from selenium_driver.views.home_webpage import Home
import datetime


check_in = datetime.datetime.now()
check_out = check_in + datetime.timedelta(days=14)

destination = "Wrocław"

@chrome_handler
def test_choice_dates():
    '''Test Author : Tom Johnson
           Contact : tom.johnson@company.com
           REQUREMENTS : REQ77872
           JIRA ID: TA-827'''
    header = Home().Header_Bar()
    header.change_language_to('en-gb')

    search_bar = Home().Search_Bar()
    search_bar.search_button_should_be_enabled()
    search_bar.search_button_should_be_visable()
    search_bar.fill_in_destination(destination)
    search_bar.assert_destination(destination)

    search_bar.click_calendar()
    search_bar.Calendar().select_dates(
        check_in.strftime("%#d %B %Y"), check_out.strftime("%#d %B %Y"))
    search_bar.Calendar().assert_dates_after_dates_selection(
        check_in.strftime("%#d %B %Y"), check_out.strftime("%#d %B %Y"))
    search_bar.click_search_button()

