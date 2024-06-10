from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd

def scrape_booking_data(city_name, checkin_date, checkout_date):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # Adjust the path to your local chromedriver
    service = Service('C:/Users/satya/OneDrive/Desktop/scraping/booking_scraper-master/chromedriver.exe')  
    driver = webdriver.Chrome(service=service, options=chrome_options)

    page_url = (f'https://www.booking.com/searchresults.en-us.html?checkin={checkin_date}'
                f'&checkout={checkout_date}&selected_currency=USD&ss={city_name}&ssne={city_name}'
                f'&ssne_untouched={city_name}&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_type=city'
                f'&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure')

    driver.get(page_url)
    
    # Wait for the hotel cards to be present
    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="property-card"]')))

    hotels_list = []
    hotel_cards = driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
    print(f'There are: {len(hotel_cards)} hotels in {city_name}.')

    for i in range(len(hotel_cards)):
        hotel_dict = {}
        try:
            hotel_cards = driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
            hotel = hotel_cards[i]

            # Use explicit waits to ensure elements are present before accessing them
            hotel_dict['hotel'] = WebDriverWait(hotel, 10).until(
                EC.presence_of_element_located((By.XPATH, './/div[@data-testid="title"]'))
            ).text
            hotel_dict['price'] = hotel.find_element(By.XPATH, './/span[@data-testid="price-and-discounted-price"]').text
            hotel_dict['score'] = hotel.find_element(By.XPATH, './/div[@data-testid="review-score"]/div[1]').text
            hotel_dict['avg review'] = hotel.find_element(By.XPATH, './/div[@data-testid="review-score"]/div[2]/div[1]').text
            hotel_dict['reviews count'] = hotel.find_element(By.XPATH, './/div[@data-testid="review-score"]/div[2]/div[2]').text.split()[0]

            # Concatenate hotel details into a single description with additional text
            hotel_dict['description'] = ('This hotel has a price of ' + hotel_dict['price'] + ', score is ' + 
                                          hotel_dict['score'] + ', average review is ' + 
                                          hotel_dict['avg review'] + ', and reviews count is ' + 
                                          hotel_dict['reviews count'])
        except IndexError as ie:
            print(f"Index error occurred for a hotel: {ie}")
            continue
        except Exception as e:
            print(f"Error occurred for a hotel: {e}")
            continue

        hotels_list.append(hotel_dict)

    df = pd.DataFrame(hotels_list, columns=['hotel', 'description'])
    df.to_csv(f'{city_name}_hot_list.csv', index=False) 

    driver.quit()

if __name__ == '__main__':
    city_name = 'Goa'  # Change this to the desired city name
    checkin_date = '2024-07-01'  # Change this to the desired check-in date
    checkout_date = '2024-07-08'  # Change this to the desired check-out date
    scrape_booking_data(city_name, checkin_date, checkout_date)



