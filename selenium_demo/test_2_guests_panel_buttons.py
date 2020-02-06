from selenium_driver.setup.selenium_setup import chrome_handler
from selenium_driver.views.home_webpage import Home


@chrome_handler
def test_guests_panel_buttons():
    '''Test Author : Tom Johnson
           Contact : tom.johnson@company.com
           REQUREMENTS : REQ77872
           JIRA ID: TA-827'''
    header = Home().Header_Bar()
    header.change_language_to('en-gb')

    search_bar = Home().Search_Bar()
    search_bar.click_guests()
    current_step = search_bar.Guests()

    current_step.add_adult_button_should_be_visible()
    current_step.add_child_button_should_be_visible()
    current_step.add_room_button_should_be_visible()
    current_step.remove_adult_button_should_be_visible()
    current_step.remove_child_button_should_be_visible()
    current_step.remove_room_button_should_be_visible()
