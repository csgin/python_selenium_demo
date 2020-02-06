from selenium_driver.setup.selenium_setup import chrome_handler
from selenium_driver.views.home_webpage import Home


###TEST INPUT DATA
child_count_start = 10
child_count_end = 0
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

@chrome_handler
def test_guests_panel_childs_limits():
    '''Test Author : Tom Johnson
       Contact : tom.johnson@company.com
       REQUREMENTS : REQ77872
       JIRA ID: TA-827'''
    header = Home().Header_Bar()
    header.change_language_to('en-gb')

    search_bar = Home().Search_Bar()
    search_bar.click_guests()
    current_step = search_bar.Guests()
    current_step.set_child_count(child_count_start)
    if child_count_start == 10:
        current_step.add_child_button_should_be_disabled()
    assert current_step.get_child_count() == child_count_start

    current_step.check_child_multiselect_count()

    current_step.check_if_child_multiselect_contains_exacly(multiselect_child_age)

    for age in multiselect_child_age:
        for child_multiselect_id in range(1, child_count_start+1):
            current_step.select_child_age(child_multiselect_id, age)
            assert current_step.get_selected_age_for_child(child_multiselect_id) == age

    current_step.set_child_count(child_count_end)

    assert current_step.get_child_count() == child_count_end
    current_step.remove_child_button_should_be_disabled()