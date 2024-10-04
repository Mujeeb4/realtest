import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import datetime
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    yield driver
    driver.quit()

def test_homepage(driver):
    driver.get("https://www.smoothmaths.com")
    assert "SmoothMaths" in driver.title

    # Generate a unique timestamp for screenshot and CSV
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create 'screenshots' directory if it doesn't exist
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')

    # Save screenshot with timestamp
    screenshot_path = f"screenshots/homepage_{timestamp}.png"
    driver.save_screenshot(screenshot_path)

    # Save test results with timestamp in CSV
    results = {
        "Test Case": ["Test Homepage"],
        "Status": ["Passed" if "SmoothMaths" in driver.title else "Failed"],
        "Screenshot": [screenshot_path]
    }
    df = pd.DataFrame(results)

    # Create a unique CSV file name with timestamp
    csv_file_path = f"test_results_{timestamp}.csv"
    df.to_csv(csv_file_path, index=False)

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

    # Generate a unique timestamp for screenshot and CSV
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create 'screenshots' directory if it doesn't exist
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')

    # Save screenshot with timestamp
    screenshot_path = f"screenshots/contact_form_{timestamp}.png"
    driver.save_screenshot(screenshot_path)

    # Save test results with timestamp in CSV
    results = {
        "Test Case": ["Test Contact Form"],
        "Status": ["Passed" if "Your message has been sent successfully." in success_message.text else "Failed"],
        "Screenshot": [screenshot_path]
    }
    df = pd.DataFrame(results)

    # Create a unique CSV file name with timestamp
    csv_file_path = f"test_results_{timestamp}.csv"
    df.to_csv(csv_file_path, index=False)

def test_login(driver):
    driver.get("https://www.smoothmaths.com/login")
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys("test_username")  # Replace with a valid username (if testing login functionality)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("test_password")  # Replace with a valid password (if testing login functionality)
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    wait = WebDriverWait(driver, 10)

    try:
        # Check for successful login element (adjust selector if needed)
        dashboard_link = wait.until(EC.presence_of_element_located((By.ID, "dashboard-link")))
        assert dashboard_link.text == "Dashboard"

        # Generate a unique timestamp for screenshot and CSV
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create 'screenshots' directory if it doesn't exist
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        # Save screenshot with timestamp
        screenshot_path = f"screenshots/login_{timestamp}.png"
        driver.save_screenshot(screenshot_path)

        # Save test results with timestamp in CSV
        results = {
            "Test Case": ["Test Login"],
            "Status": ["Passed"],
            "Screenshot": [screenshot_path]
        }
    except Exception as e:
        # In case of a failure, capture the failure details
        results = {
            "Test Case": ["Test Login"],
            "Status": ["Failed"],
            "Error": [str(e)]
        }

    df = pd.DataFrame([results])

    # Create a unique CSV file name with timestamp
    csv_file_path = f"test_results_{timestamp}.csv"
    df.to_csv(csv_file_path, index=False)
