from playwright.sync_api import Page, expect
import random

BASE_URL = "http://127.0.0.1:5000"

#Using browser dialog to confirm earn/expense deletion so must use a function to handle
def handle_dialog(dialog):
	dialog.accept()

def test_earning(page: Page):
	page.goto(BASE_URL)
	page.on("dialog", handle_dialog)

	login_button = page.locator('button[id="index_login"]')
	login_button.click()

	username = page.locator('input[id="username"]')
	username.fill("TestAccount")

	password = page.locator('input[id="password"]')
	password.fill("PASSWORD")

	submit = page.locator('button.button_login')
	submit.click()

	earning = page.locator('button[id="add_earning"]')
	earning.click()

	earn_title = page.locator('input[id="earnTitle"]')
	earn_title.fill("TestEarning")

	random_amount = str(random.randint(0, 10000))

	earn_amount = page.locator('input[id="earnAmount"]')
	earn_amount.fill(random_amount)

	submit_earn = page.locator('button[id="submit_earn"]')
	submit_earn.click()

	example_earning = page.locator('.e_green').filter(has_text=random_amount)
	expect(example_earning).to_be_visible

	edit_earn = page.locator('button.edit_earn')
	edit_earn.click()

	random_amount_2 = str(random.randint(0, 10000))

	earn_amount = page.locator('input[id="earnAmount"]')
	earn_amount.fill(random_amount_2)

	submit_earn = page.locator('button[id="submit_earn"]')
	submit_earn.click()

	example_earning = page.locator('.e_green').filter(has_text=random_amount_2)
	expect(example_earning).to_be_visible

	delete_earn = page.locator('button.delete_earn')
	delete_earn.click()

	expect(example_earning).not_to_be_visible



def test_expense(page: Page):
	page.goto(BASE_URL)
	page.on("dialog", handle_dialog)

	login_button = page.locator('button[id="index_login"]')
	login_button.click()

	username = page.locator('input[id="username"]')
	username.fill("TestAccount")

	password = page.locator('input[id="password"]')
	password.fill("PASSWORD")

	submit = page.locator('button.button_login')
	submit.click()

	expense = page.locator('button[id="add_expense"]')
	expense.click()

	expense_title = page.locator('input[id="expenseTitle"]')
	expense_title.fill("TestExpense")

	random_amount = str(random.randint(0, 10000))

	expense_dedicated_amount = page.locator('input[id="dedicatedAmount"]')
	expense_dedicated_amount.fill(random_amount)

	expense_spend_amount = page.locator('input[id="actualSpendAmount"]')
	expense_spend_amount.fill(random_amount)

	submit_expense = page.locator('button[id="submit_expense"]')
	submit_expense.click()

	example_expense = page.locator('.e_blue').filter(has_text=random_amount)
	expect(example_expense).to_be_visible

	edit_expense = page.locator('button.edit_expense')
	edit_expense.click()

	random_amount_2 = str(random.randint(0, 10000))

	expense_dedicated_amount = page.locator('input[id="dedicatedAmount"]')
	expense_dedicated_amount.fill(random_amount_2)

	submit_expense = page.locator('button[id="submit_expense"]')
	submit_expense.click()

	example_expense = page.locator('.e_blue').filter(has_text=random_amount)
	expect(example_expense).to_be_visible

	delete_earn = page.locator('button.delete_expense')
	delete_earn.click()

	expect(example_expense).not_to_be_visible




