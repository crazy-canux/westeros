from super_devops.selenium.link import WebLink
from super_devops.selenium.textbox import WebTextbox
from super_devops.selenium.button import WebButton
from super_devops.selenium.label import WebLabel

class Dashboard(object):

    """"Dashboard page on westeros web-gui."""

    def __init__(self):
        # Login page
        self.username_textbox = WebTextbox(
            xpath='//*[@id="id"]'
        )
        self.password_textbox = WebTextbox(
            xpath='//*[@id="id"]'
        )
        self.login_button = WebButton(
            xpath='//*[@id="id"]'
        )

        # Logout page
        self.logout_button = WebButton(
            xpath='//*[@id="id"]'
        )
