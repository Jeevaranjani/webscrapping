#install libraries
#pip install selenium
#pip install pandas


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Set up Chrome WebDriver
chrome_driver_path = r'C:\Users\djeev\scrape\chromedriver.exe.exe'
options = Options()
options.add_argument("--start-maximized")
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Open the main project list page
url = "https://rera.odisha.gov.in/projects/project-list"
driver.get(url)
time.sleep(5)

# Scroll to load content (ensure JS loads the project cards)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# Get first 6 "View Details" buttons
view_buttons = driver.find_elements(By.XPATH, "//a[contains(text(),'View Details')]")[:6]

# Initialize result list
project_data = []

for i in range(6):
    print(f"Processing project {i + 1}...")

    # Re-locate buttons due to DOM refresh after back()
    view_buttons = driver.find_elements(By.XPATH, "//a[contains(text(),'View Details')]")
    driver.execute_script("arguments[0].click();", view_buttons[i])
    time.sleep(4)

    # ---------------- Project Details ----------------
    try:
        rera_no = driver.find_element(By.XPATH, "//label[contains(text(),'RERA Regd')]/following-sibling::strong").text.strip()
    except:
        rera_no = None

    try:
        project_name = driver.find_element(By.XPATH, "//label[contains(text(),'Project Name')]/following-sibling::strong").text.strip()
    except:
        project_name = None

    # ---------------- Promoter Details Tab ----------------
    try:
        promoter_tab = driver.find_element(By.XPATH, "//a[contains(text(),'Promoter Details')]")
        promoter_tab.click()
        time.sleep(3)
    except:
        print("Couldn't open Promoter Details tab")
        pass

    # Extract promoter fields
    # Extract promoter name (Company Name or Proprietory Name)
    try:
        promoter_name = driver.find_element(By.XPATH, "//div[label[contains(text(),'Company Name') or contains(text(),'Proprietory Name')]]/strong").text.strip()
    except:
        promoter_name = None


    try:
        promoter_address = driver.find_element(By.XPATH, "//div[label[contains(text(),'Registered Office Address') or contains(text(),'Current Residence Address')]]/strong").text.strip()
    except:
        promoter_address = None


    try:
        gst_no = driver.find_element(By.XPATH, "//div[label[contains(text(),'GST No')]]/strong").text.strip()
    except:
        gst_no = None

    # Save result
    project_data.append({
        "RERA Regd. No": rera_no,
        "Project Name": project_name,
        "Promoter Name": promoter_name,
        "Promoter Address": promoter_address,
        "GST No": gst_no
    })

    # Go back to main page
    driver.back()
    time.sleep(4)

# Create DataFrame
df = pd.DataFrame(project_data)
print(df)

# Save to CSV
df.to_csv("odisha_rera_projects.csv", index=False)

# Quit driver
driver.quit()


