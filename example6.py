import os

import pytest
from playwright.sync_api import sync_playwright, expect

# Katumbas ng -Dheadless=true. Default: headless (para gumana sa CI)
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"


@pytest.fixture(scope="module")
def page():
    """Katumbas ng setUp(): gumagawa ng browser at page para sa buong file."""
    with sync_playwright() as p:
        # Ibang browsers: p.firefox.launch(...), p.webkit.launch(...)
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        page.set_default_timeout(50000)
        expect.set_options(timeout=7000)  # default assertion timeout
        page.goto("https://www.saucedemo.com/")
        yield page
        browser.close()


def test_login(page):
    """Access and Login to the Swag labs website"""
    print(page.title())
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_label("Password").fill("secret_sauce")
    page.locator("#login-button").click()


def test_inventory(page):
    """Verify if able to access the Inventory Page"""
    print(page.title())
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
