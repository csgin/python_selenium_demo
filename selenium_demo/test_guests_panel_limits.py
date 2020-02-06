from selenium_driver.setup.selenium_setup import chrome_handler
from selenium_driver.views.home_webpage import Home


@chrome_handler
def test_guests_panel_limits():
    '''Test Author : Tom Johnson
           Contact : tom.johnson@company.com
           REQUREMENTS : REQ77872
           JIRA ID: TA-827'''
    header = Home().Header_Bar()
    header.change_language_to('en-gb')

    search_bar = Home().Search_Bar()
    search_bar.click_guests()
    current_step = search_bar.Guests()

    assert current_step.get_adult_count() == 2
    assert current_step.get_child_count() == 0
    assert current_step.get_room_count() == 1

    current_step.set_adult_count(30)
    current_step.set_child_count(10)
    current_step.set_room_count(30)

    assert current_step.get_adult_count() == 30
    assert current_step.get_child_count() == 10
    assert current_step.get_room_count() == 30

    current_step.add_room_button_should_be_disabled()
    current_step.add_child_button_should_be_disabled()
    current_step.add_adult_button_should_be_disabled()

    current_step.set_adult_count(15)
    current_step.set_child_count(5)
    current_step.set_room_count(15)

    assert current_step.get_adult_count() == 15
    assert current_step.get_child_count() == 5
    assert current_step.get_room_count() == 15

    current_step.set_adult_count(1)
    current_step.set_child_count(0)
    current_step.set_room_count(1)

    assert current_step.get_adult_count() == 1
    assert current_step.get_child_count() == 0
    assert current_step.get_room_count() == 1

    current_step.remove_room_button_should_be_disabled()
    current_step.remove_child_button_should_be_disabled()
    current_step.remove_adult_button_should_be_disabled()
