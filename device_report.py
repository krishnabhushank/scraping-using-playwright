from playwright.sync_api import sync_playwright
import csv

# Initialize Playwright
with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)  # Set headless=True for headless mode

    # Create a new browser context
    context = browser.new_context()

    # Read the CSV file
    with open('C:/Users/kkoneru/Downloads/samsung_scrape/000_samsung_appliances-consolidated_1.csv', 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            brand = row['brand']
            model = row['model']
            model_without_slash = model.split('/')[0]
            link = "https://device.report/" + brand + "/" + model_without_slash

            print(link)
            # Navigate to the webpage for each category
            page = context.new_page()
            page.goto(link)

            # Extract features from the table with the header "Manufacturer Provided Features"
            table_with_header = page.query_selector(
                'table[style="table-layout: fixed"] th[scope="row"][style="width:40%"]:has-text("Manufacturer Provided Features")')
            if table_with_header:
                print(table_with_header.text_content())
                features = []
                for t_row in table_with_header.query_selector_all('tr'):
                    feature = t_row.query_selector('td').inner_text()
                    features.append(feature)

                print(features)

            # Close the page
            page.close()

    # Close the browser
    context.close()
