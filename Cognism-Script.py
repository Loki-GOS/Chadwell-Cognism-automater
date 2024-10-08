from playwright.sync_api import Playwright, sync_playwright, expect
import time
from playwright_stealth import stealth_sync
import logging

# Logging output to a file called "Cognism.log". This will log the user, start and end pages and the time ran. 
# Helpful when you forget which page you ended at.
logging.basicConfig(filename='./Cognism.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def logs():
    user = input("User: ")
    start_page = int(input('Start Page: '))
    end_page = start_page + 19
    logging.info(f'Script ran as {user}\n Start Page: {start_page}\n End Page: {end_page}')

PARTIAL_LIST_NAME = "test li"
LIST_NAME = "test list"
LIMIT_CONTACTS="1"

    

def run(playwright: Playwright) -> None:

    print('connecting to browser')
    browser = playwright.webkit.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    stealth_sync(page)
    page.goto("https://app.cognism.com/auth/sign-in")
    stealth_sync(page)
    Pause=input("press entr whn logged in and list loaded")

    print('navigating')
    page.get_by_test_id("WJKQejEcDnztCL6YwANS").click()
    page.get_by_label("Select Page25").check()
    page.get_by_role("button").filter(has_text="Save to List").click()
    page.locator("nz-form-control").get_by_role("textbox").click()
    page.locator("nz-form-control").get_by_role("textbox").fill(PARTIAL_LIST_NAME)
    page.get_by_text(LIST_NAME).click()
    expect(page.locator("nz-form-control")).to_contain_text(LIST_NAME)
    
    expect(page.get_by_text("Cancel Save")).to_be_visible()
    expect(page.get_by_role("banner")).to_contain_text("Saving 25 contacts in a List")
    page.get_by_placeholder("Enter the number of contacts").click()
    page.get_by_placeholder("Enter the number of contacts").fill(LIMIT_CONTACTS)
    page.locator("[id^='cdk-overlay']").get_by_role("button", name="Save").click()

    for _ in range(20):
        print(f"Starting Loop {_}")
        page.query_selector('a[data-cognism="paginate-next-a"]').click()
        time.sleep(1.5)
        page.get_by_test_id("WJKQejEcDnztCL6YwANS").click()
        page.get_by_label("Select Page25").check()
        page.get_by_role("button").filter(has_text="Save to List").click()
        page.locator("nz-form-control").get_by_role("textbox").click()
        page.locator("nz-form-control").get_by_role("textbox").fill(PARTIAL_LIST_NAME)
        page.get_by_text(LIST_NAME).click()
        expect(page.locator("nz-form-control")).to_contain_text(LIST_NAME)
    
        expect(page.get_by_text("Cancel Save")).to_be_visible()
        expect(page.get_by_role("banner")).to_contain_text("Saving 25 contacts in a List")
        page.get_by_placeholder("Enter the number of contacts").click()
        page.get_by_placeholder("Enter the number of contacts").fill(LIMIT_CONTACTS)
        page.locator("[id^='cdk-overlay']").get_by_role("button", name="Save").click()
    
        
        
        # ---------------------
    page.click('button[data-cognism="user-menu-button"]')
    page.get_by_text("Log Out").click()
    context.close()

logs()

with sync_playwright() as playwright:
    run(playwright)
