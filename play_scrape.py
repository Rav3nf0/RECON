import requests
import csv
from bs4 import BeautifulSoup

def parse_install_count(install_text):
    install_text = install_text.strip().replace(',', '')

    if 'M' in install_text:
        num_installs = install_text.replace('M+', '')
        if num_installs:
            return int(num_installs) * 1000000
    elif 'B' in install_text:
        num_installs = install_text.replace('B+', '')
        if num_installs:
            return int(num_installs) * 1000000000
    elif install_text.isdigit():
        return int(install_text)

    return 0  # Return 0 for invalid or empty install counts

# Provide a list of search terms
search_terms = ['chat', 'games', 'social', 'music', 'education', 'shopping', 'Entertainment', 'lifestyle', 'books', 'food', 'tools', 'sports', 'references']

with open('app_data_combined.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Search Term', 'App Name', 'App URL', 'Number of Installs']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for search_term in search_terms:
        URL = f"https://play.google.com/store/search?q={search_term}&c=apps&hl=en&gl=in"

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        app_links = []
        app_name = []
        app_installs = []

        # Find all the app names and links using the specific classes
        name_elements = soup.find_all('span', class_='DdYX5')
        for element in name_elements:
            app_name.append(element.text)

        link_elements = soup.find_all('a', class_='Si6A0c Gy4nib', href=True)
        for link_element in link_elements:
            app_links.append(link_element['href'])

        # Visit each app's URL, scrape and filter by installs, then store in CSV
        for app_link, app_name in zip(app_links, app_name):
            full_app_link = "https://play.google.com" + app_link
            app_page = requests.get(full_app_link)
            app_soup = BeautifulSoup(app_page.content, 'html.parser')

            # Find the second div element with class ClM7O
            div_elements = app_soup.find_all('div', class_='ClM7O')

            if len(div_elements) >= 2:
                div_element = div_elements[1]  # Selecting the second div element

                # Extract the number of installs from the div content
                install_text = div_element.get_text()
                num_installs = parse_install_count(install_text)

                if num_installs >= 100000000:  # Filter apps with installs <= 100 million
                    writer.writerow({'Search Term': search_term, 'App Name': app_name, 'App URL': full_app_link, 'Number of Installs': num_installs})

print("Data has been saved to app_data_NEW_combined.csv")
