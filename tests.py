import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_homepage(driver):
    driver.get("https://www.smoothmaths.com")
    assert "SmoothMaths" in driver.title
    driver.save_screenshot("homepage.png")

def test_contact_form(driver):
    driver.get("https://www.smoothmaths.com/contact")
    name_field = driver.find_element(By.ID, "name")
    name_field.send_keys("Test User")
    email_field = driver.find_element(By.ID, "email")
    email_field.send_keys("test@example.com")
    message_field = driver.find_element(By.ID, "message")
    message_field.send_keys("This is a test message.")
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()
    wait = WebDriverWait(driver, 10)
    success_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "success-message")))
    assert "Your message has been sent successfully." in success_message.text
    driver.save_screenshot("contact_form.png")

def test_login(driver):
    driver.get("https://www.smoothmaths.com/login")
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys("test_username")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("test_password")
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    wait = WebDriverWait(driver, 10)
    dashboard_link = wait.until(EC.presence_of_element_located((By.ID, "dashboard-link")))
    assert dashboard_link.text == "Dashboard"
    driver.save_screenshot("login.png")

    # Save test results
    results = {
        "Test Case": "Test Homepage, Contact Form, and Login",
        "Status": "Passed",
        "Screenshot": "test_results.csv"
    }
    df = pd.DataFrame(results)
    df.to_csv("test_results.csv", index=False)
