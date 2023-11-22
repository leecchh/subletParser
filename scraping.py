import csv
from bs4 import BeautifulSoup
from datetime import datetime

# Path to your HTML file
file_path = 'test.html'  # Replace with your file path

# Read the HTML content from the file
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# List to store listings
listings = []

# Function to parse the date string
def parse_dates(date_str):
    if '-' in date_str:
        start_str, end_str = date_str.split(' - ')
        start_date = datetime.strptime(start_str.strip(), '%B %d, %Y')
        end_date = datetime.strptime(end_str.strip(), '%B %d, %Y')
    else:
        start_date = datetime.strptime(date_str.strip(), '%B %d, %Y')
        end_date = start_date  # or use None if no end date is provided
    return start_date, end_date

# Set to store unique listings
unique_listings = set()

# Iterate through each div tag
for div in soup.find_all('div'):
    price = div.find(class_="text-white text-smish font-semibold bg-teal-light py-1 px-2")
    location = div.find(class_="text-grey-dark font-semibold text-smish")
    description = div.find(class_="text-teal-light hover:text-teal no-underline")
    time = div.find(class_="text-white text-smish bg-teal-light py-1 px-2")
    img_tag = div.find('img')
    url_tag = div.find('a', class_="font-bold text-teal-light hover:text-teal no-underline")

    if price and location and description and time and img_tag and url_tag:
        start_time, end_time = parse_dates(time.text.strip())
        img_src = img_tag.get('src', '').strip()
        url = "https://www.listingsproject.com" + url_tag.get('href', '').strip()
        listing_tuple = (start_time, end_time, price.text.strip(), location.text.strip(), description.text.strip(), img_src, url)
        
        # Check for duplicates
        if listing_tuple not in unique_listings:
            unique_listings.add(listing_tuple)
            listings.append(listing_tuple)

# Sort listings by startTime
listings.sort(key=lambda x: x[0])

# CSV file path
csv_file_path = 'listings.csv'

# Writing to CSV
with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Start Time', 'End Time', 'Price', 'Location', 'Description', 'Image URL', 'URL'])  # Updated header

    for listing in listings:
        writer.writerow([
            listing[0].strftime('%Y-%m-%d'), 
            listing[1].strftime('%Y-%m-%d'), 
            listing[2], 
            listing[3].replace('|', '-'), 
            listing[4], 
            listing[5],
            listing[6]
        ])

print(f"Data exported to {csv_file_path}")