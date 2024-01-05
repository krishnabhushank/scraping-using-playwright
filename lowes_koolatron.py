from playwright.sync_api import sync_playwright
import csv


def scrape_product_card(product_card):
    link = "https://www.lowes.com" + product_card.query_selector('.ImageHolderStyle-sc-4v6c0e-1 a').get_attribute('href')

    try:
        brand_name = product_card.query_selector('.js-save-to-list').get_attribute('data-brand')
    except AttributeError:
        brand_name = 'NA'
    except KeyError:
        brand_name = 'NA'

    try:
        product_name = product_card.query_selector('.js-save-to-list').get_attribute('data-description')
    except AttributeError:
        product_name = 'NA'
    except KeyError:
        product_name = 'NA'

    try:
        price_element = product_card.query_selector('.slpl-price-info')
        product_price = ""
        if price_element:
            price_elements = price_element.query_selector_all('sup')
            product_price = ''.join(element.inner_text() for element in price_elements)

    except AttributeError:
        product_price = 'NA'
    except KeyError:
        product_price = 'NA'

    try:
        model_number = product_card.query_selector('.tooltip-custom').inner_text()
        model_number = model_number.replace("Model #", "")
    except AttributeError:
        model_number = 'NA'
    except KeyError:
        model_number = 'NA'

    return {
        'model_number': model_number,
        'brand_name': brand_name,
        'product_name': product_name,
        'price': product_price,
        'link': link
    }


def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # Set headless=True for headless mode
        page = browser.new_page()

        page.goto(
            "https://www.lowes.com/search?searchTerm=koolatron")

        # Wait for a specific amount of time before clicking "Apply"
        page.wait_for_timeout(2000)  # Wait for 2 seconds (adjust as needed)

        data_list = []  # List to store scraped data

        while True:
            page.wait_for_timeout(5000)  # Wait for 5 seconds (adjust as needed)

            product_cards = page.query_selector_all(".sc-o9wle2-4")
            print(f"Number of Products : {len(product_cards)}")

            for card in product_cards:
                product_data = scrape_product_card(product_card=card)

                data_list.append(product_data)  # Append the data to the list

            # Check if the "Next" button is disabled
            next_button = page.query_selector('a.hd-pagination__link[aria-label="Next"]')
            if next_button and "Nao=" not in next_button.get_attribute('href'):
                print("No More Next")
                break  # Exit the loop if there's no "Next" button

            next_button.click()
            page.wait_for_selector(".browse-search__pod")
            print("Next Page")

        browser.close()

        # Specify the CSV file path
        csv_file_path = "C:/Users/kkoneru/Downloads/amazon_scrape/koolatron_homedepot_prds.csv"
        field_names = ["model_number", "brand_name", "product_name", "price", "link"]

        # Open the CSV file in write mode and create a CSV writer
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data_list)


if __name__ == "__main__":
    main()
