from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


# Initialize the WebDriver with the configured options
driver = webdriver.Chrome(options=chrome_options)


files = {
    'email': (None, 'pkalkie@gmail.com'),
    'wachtwoord': (None, 'F11442P1552'),
    'inloggen': (None, 'Inloggen')
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Open login page
driver.get('https://www.gppoule.nl/inloggen/')

driver.find_element(By.NAME, 'email').send_keys('pkalkie@gmail.com')
driver.find_element(By.NAME, 'wachtwoord').send_keys('F11442P1552')
driver.find_element(By.NAME, 'inloggen').click()

# Navigate to the protected page
driver.get('https://www.gppoule.nl/poule-info/9830/')

# Extract data
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Find the table by div class (adjust the class names based on your HTML)
table_rows = soup.find_all('div', class_='row table-race p-0')

# Initialize a list to store the data
data = []

# Loop through the rows and extract data
for row in table_rows:
    columns = row.find_all('div', recursive=False)
    place = columns[0].get_text(strip=True)
    name = columns[1].get_text(strip=True)
    points = columns[2].get_text(strip=True)

    # Append the data to the list as a dictionary
    data.append({
        'place': place,
        'name': name,
        'points': points
    })

# Convert the list to JSON
json_data = json.dumps(data, indent=4)

# Write the JSON data to a file
with open('data.json', 'w') as file:
    file.write(json_data)

print("Data saved to data.json")

# Close the browser
driver.quit()
