from config.settings import BASE_URL


class LoginPage:

    def __init__(self, page):
        self.page = page

        self.username_input = self.page.locator("input[name='username']")
        self.password_input = self.page.locator("input[name='password']")
        self.login_button = self.page.get_by_role("button", name="Login")

    def open(self):
        self.page.goto(BASE_URL)

    def enter_username(self, username):
        self.username_input.fill(username)

    def enter_password(self, password):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()