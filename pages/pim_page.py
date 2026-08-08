import time
from playwright.sync_api import expect


class PIMPage:

    def __init__(self, page):
        self.page = page

        self.pim_menu = self.page.get_by_role("link", name="PIM")
        self.add_button = self.page.get_by_role("button", name="Add")

        self.first_name_input = self.page.locator("input[name='firstName']")
        self.middle_name_input = self.page.locator("input[name='middleName']")
        self.last_name_input = self.page.locator("input[name='lastName']")

        self.employee_id_input = (
            self.page
            .locator(".oxd-input-group")
            .filter(has_text="Employee Id")
            .locator("input")
        )

        self.save_button = self.page.get_by_role("button", name="Save")


    def open_pim(self):
        self.pim_menu.click()


    def click_add_employee(self):
        self.add_button.click()


    def enter_first_name(self, first_name):
        self.first_name_input.fill(first_name)


    def enter_middle_name(self, middle_name):
        self.middle_name_input.fill(middle_name)


    def enter_last_name(self, last_name):
        self.last_name_input.fill(last_name)


    def enter_employee_name(self, first_name, middle_name, last_name):
        self.enter_first_name(first_name)
        self.enter_middle_name(middle_name)
        self.enter_last_name(last_name)

    def enter_employee_id(self, employee_id):
        self.employee_id_input.fill(employee_id)


    def click_save(self):
        self.save_button.click()


    def get_employee_id(self):
        expect(self.employee_id_input).not_to_have_value("")
        return self.employee_id_input.input_value()


    def create_employee(self, first_name, middle_name, last_name):
        self.enter_employee_name(first_name, middle_name, last_name)

        employee_id = str(int(time.time() * 1000))[-9:]

        self.enter_employee_id(employee_id)

        self.click_save()

        self.page.wait_for_url("**/pim/viewPersonalDetails/empNumber/**")

        return employee_id


    def validate_employee_id(self, expected_employee_id):
        actual_employee_id = self.get_employee_id()

        if actual_employee_id == expected_employee_id:
            return True

        return False