import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import datetime
import time

# CSV file path to store all test results
CSV_FILE_PATH = "test_results.csv"

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is not required
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    yield driver
    driver.quit()

def append_to_csv(results):
    """Append the test results to the CSV file."""
    if not os.path.exists(CSV_FILE_PATH):
        df = pd.DataFrame(results)
        df.to_csv(CSV_FILE_PATH, index=False)  # Write a new file if it doesn't exist
    else:
        df = pd.DataFrame(results)
        df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)  # Append to existing file

def test_homepage(driver):
    start_time = time.time()  # Record the start time

    driver.get("https://www.smoothmaths.co.uk")
    status = "Passed" if "SmoothMaths" in driver.title else "Failed"

    # Record end time and calculate duration
    end_time = time.time()
    duration = end_time - start_time

    # Generate a unique timestamp for screenshot
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create 'screenshots' directory if it doesn't exist
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')

    # Save screenshot with timestamp
    screenshot_path = f"screenshots/homepage_{timestamp}.png"
    driver.save_screenshot(screenshot_path)

    # Prepare results for CSV
    results = {
        "Test Case": ["Test Homepage"],
        "Status": [status],
        "Duration (seconds)": [round(duration, 2)],  # Rounded duration
        "Screenshot": [screenshot_path]
    }
    
    # Append results to the CSV file
    append_to_csv(results)

def test_contact_form(driver):
    start_time = time.time()  # Record the start time

    driver.get("https://www.smoothmaths.co.uk/contact")
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
    status = "Passed" if "Your message has been sent successfully." in success_message.text else "Failed"

    # Record end time and calculate duration
    end_time = time.time()
    duration = end_time - start_time

    # Generate a unique timestamp for screenshot
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Save screenshot with timestamp
    screenshot_path = f"screenshots/contact_form_{timestamp}.png"
    driver.save_screenshot(screenshot_path)

    # Prepare results for CSV
    results = {
        "Test Case": ["Test Contact Form"],
        "Status": [status],
        "Duration (seconds)": [round(duration, 2)],  # Rounded duration
        "Screenshot": [screenshot_path]
    }

    # Append results to the CSV file
    append_to_csv(results)

def test_login(driver):
    start_time = time.time()  # Record the start time

    driver.get("https://www.smoothmaths.co.uk/login")
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
        status = "Passed"
    except Exception as e:
        status = "Failed"

    # Record end time and calculate duration
    end_time = time.time()
    duration = end_time - start_time

    # Generate a unique timestamp for screenshot
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Save screenshot with timestamp
    screenshot_path = f"screenshots/login_{timestamp}.png"
    driver.save_screenshot(screenshot_path)

    # Prepare results for CSV
    results = {
        "Test Case": ["Test Login"],
        "Status": [status],
        "Duration (seconds)": [round(duration, 2)],  # Rounded duration
        "Screenshot": [screenshot_path]
    }

    # Append results to the CSV file
    append_to_csv(results)
