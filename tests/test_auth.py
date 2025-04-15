from playwright.sync_api import Page, expect
import random

BASE_URL = "http://127.0.0.1:5000"

def test_landing_page(page: Page):
   page.goto(BASE_URL)
   expect(page).to_have_title("Paige's Finance Tracker")

def test_user_creation(page: Page):
   page.goto(BASE_URL)
   register_button = page.get_by_role("link", name="Register")
   register_button.click()

   username = page.locator('input[id="username"]')
   expect(username).to_be_visible()
   username.fill(f"TestUser{random.randint(0, 10000)}")

   password = page.locator('input[id="password"]')
   expect(password).to_be_visible()
   password.fill("PASSWORD")

   confirm_password = page.locator('input[id="confirm_password"]')
   expect(confirm_password).to_be_visible()
   confirm_password.fill("PASSWORD")

   security_question = page.locator('input[id="security_question_one"]')
   expect(security_question).to_be_visible()
   security_question.fill("THIS IS A TEST QUESTION")

   security_answer = page.locator('input[id="security_answer_one"]')
   expect(security_answer).to_be_visible()
   security_answer.fill("THIS IS A TEST ANSWER")

   submit = page.locator('button[type="submit"]')
   submit.click()

   flash_success = page.locator('div.alert-success')
   expect(flash_success).to_be_visible()


def test_user_creation_wrong(page: Page):
   page.goto(BASE_URL)
   register_button = page.locator('button[id="index_register"]')
   register_button.click()

   expect(page).to_have_url(f"{BASE_URL}/register")

   username = page.locator('input[id="username"]')
   expect(username).to_be_visible()
   username.fill(f"TestUser{random.randint(0, 10000)}")

   password = page.locator('input[id="password"]')
   expect(password).to_be_visible()
   password.fill("PASSWORD")

   confirm_password = page.get_by_label("Confirm Password:")
   expect(confirm_password).to_be_visible()
   confirm_password.fill("WRONGPASSWORD")

   security_question = page.locator('input[id="security_question_one"]')
   expect(security_question).to_be_visible()
   security_question.fill("THIS IS A TEST QUESTION")

   security_answer = page.locator('input[id="security_answer_one"]')
   expect(security_answer).to_be_visible()
   security_answer.fill("THIS IS A TEST ANSWER")

   submit = page.locator('button[type="submit"]')
   submit.click()

   flash_danger = page.locator('div.alert-danger')
   expect(flash_danger).to_be_visible()


def test_login_success(page: Page):
   page.goto(BASE_URL)
   login_button = page.locator('button[id="index_login"]')
   login_button.click()

   username = page.locator('input[id="username"]')
   username.fill("TestAccount")

   password = page.locator('input[id="password"]')
   password.fill("PASSWORD")

   submit = page.locator('button.button_login')
   submit.click()

   tracksheet = page.locator('div.tracksheet_content')
   expect(tracksheet).to_be_visible()


def test_login_incorrect(page: Page):
   page.goto(BASE_URL)
   login_button = page.locator('button[id="index_login"]')
   login_button.click()

   username = page.locator('input[id="username"]')
   username.fill("TestAccount")

   password = page.locator('input[id="password"]')
   password.fill("WRONGPASSWORD")

   submit = page.locator('button.button_login')
   submit.click()

   flash_danger = page.locator('div.alert-danger')
   expect(flash_danger).to_be_visible()