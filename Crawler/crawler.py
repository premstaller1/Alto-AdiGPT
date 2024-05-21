import requests
from bs4 import BeautifulSoup
import csv


# Function to extract links from a single page
def extract_links_from_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        drei_spalten_elements = soup.find_all(class_='dreiSpalten')
        links = []
        for element in drei_spalten_elements:
            a_tag = element.find('a')
            if a_tag and 'href' in a_tag.attrs:
                link = a_tag['href']
                full_url = "https://www.almenrausch.at" + link
                links.append(full_url)
        print(links)
        return links
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []
    
#Function to extract information from a subpage
def extract_info_from_subpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Processing subpage: {url}")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the section containing the tour name
        tour_name_section = soup.find('div', id='detail-top')
        # Extract tour name
        tour_name = tour_name_section.find('h1').text.strip()
        
        # Find the main row element containing tour information
        row_element = soup.find(class_='singel-infowrap')
        
        # Extract description from the main row element
        description_paragraphs = row_element.find_all('p')
        description_paragraphs
        description = "\n".join([p.text.strip() for p in description_paragraphs if p.text.strip() != ""])

        charakter_element = soup.find(class_='charakter')
        character = charakter_element.text.strip()

        # Find the tripInfoWide section
        trip_info_wide = soup.find(class_='tripInfoWide')

        # Extract information from tripInfoWide
        tour_info = {}
        for tr in trip_info_wide.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) == 2:
                key = tds[0].text.strip().rstrip(':')
                value = tds[1].text.strip()
                tour_info[key] = value

        # Find the tripHousing section
        trip_housing = soup.find(class_='tripHousing')

        # Initialize housing_recommendations list
        housing_recommendations = []

        # Check if tripHousing section exists
        if trip_housing:
            # Find all overviewBox elements
            overview_boxes = trip_housing.find_all(class_='overviewBox')
            
            # If overviewBox elements exist, extract information
            if overview_boxes:
                for box in overview_boxes:
                    housing_info = {}
                    housing_info['Title'] = box.find('span', itemprop='headline').text.strip()
                    housing_info['Description'] = box.find('div', itemprop='description').text.strip()
                    housing_info['Link'] = "https://www.almenrausch.at" + box.find('a')['href']
                    housing_recommendations.append(housing_info)
            else:
                print("No housing recommendations found.")

        return tour_name, description, character, tour_info, housing_recommendations

        return tour_name, description, character, tour_info, housing_recommendations
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None, None, None, {}, []
    
# Function to save tour information to a CSV file
def save_to_csv(all_tour_info):
    with open('tour_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Tour Name', 'Description', 'Character', 'Tour Info', 'Housing Recommendations']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for tour_info in all_tour_info:
            writer.writerow({
                'Tour Name': tour_info[0],
                'Description': tour_info[1],
                'Character': tour_info[2],
                'Tour Info': tour_info[3],
                'Housing Recommendations': tour_info[4]
            })
    
# Main function to process multiple pages
def main():
    base_url = "https://www.almenrausch.at/touren/suchergebnisse/"
    total_pages = 107
    all_tour_info = []

    for page_num in range(1, total_pages + 1):
        page_url = base_url + str(page_num) + "/"
        print(f"Processing page: {page_num}")
        links = extract_links_from_page(page_url)
        for link in links:
            tour_info = extract_info_from_subpage(link)
            if tour_info:
                all_tour_info.append(tour_info)

    # Save the extracted information into a CSV file
    save_to_csv(all_tour_info)


if __name__ == "__main__":
    main()