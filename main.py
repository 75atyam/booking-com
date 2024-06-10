import pandas as pd
import booking_scraper as bk  # Assuming booking_scraper.py is in the same directory

# Specify the parameters for scraping
city_name = 'Goa'
checkin_date = '2024-07-01'
checkout_date = '2024-07-08'

# Run the scraping function
bk.scrape_booking_data(city_name, checkin_date, checkout_date)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('Goa_hot_list.csv')

# Display the DataFrame
print(df)
