from playwright.sync_api import sync_playwright
import csv


def scrape_product_card(product_card):
    asin = product_card.get_attribute('data-asin')

    try:
        product_name = product_card.query_selector("h2.a-size-mini").inner_text()
    except AttributeError:
        product_name = 'NA'
    except KeyError:
        product_name = 'NA'

    try:
        product_price = product_card.query_selector("span.a-offscreen").inner_text()
    except AttributeError:
        product_price = 'NA'
    except KeyError:
        product_price = 'NA'

    return {
        'asin': asin,
        'product_name': product_name,
        'price': product_price
    }


def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # Set headless=True for headless mode
        page = browser.new_page()

        page.goto(
            "https://www.amazon.com/s?k=kenmore&i=garden&rh=n%3A1055398%2Cp_89%3AKenmore&dc&crid=1VG300M71WFCO&qid=1692369138&refresh=1&rnid=2528832011&sprefix=kenmore%2Caps%2C552&ref=sr_pg_1")

        # Click to open the popup
        deliver_to_link = page.query_selector(
            '#nav-global-location-popover-link')  # Replace with the actual selector for the link
        deliver_to_link.click()

        # Wait for the popup to open
        page.wait_for_selector('#GLUXZipUpdateInput')  # Replace with the actual selector for the input field

        # Enter the zip code
        zip_code_input = page.query_selector(
            '#GLUXZipUpdateInput')  # Replace with the actual selector for the input field
        zip_code_input.fill('60169')

        # Wait for a specific amount of time before clicking "Apply"
        page.wait_for_timeout(2000)  # Wait for 2 seconds (adjust as needed)

        # Apply the zip code
        apply_button = page.query_selector('#GLUXZipUpdate')  # Replace with the actual selector for the Apply button
        apply_button.click()

        # Wait for the popup to open
        page.wait_for_selector('#GLUXHiddenSuccessDialog')  # Replace with the actual selector for the success dialog

        try:
            # Extract the zip code
            zip_code = page.query_selector(
                '#GLUXHiddenSuccessSelectedAddressPlaceholder').inner_text()  # Replace with the actual selector for the zip code element
        except AttributeError:
            zip_code = 'NA'
        except KeyError:
            zip_code = 'NA'

        print(f"zip_code: {zip_code}")

        # Wait for a specific amount of time before clicking "Continue"
        page.wait_for_timeout(2000)  # Wait for 2 seconds (adjust as needed)

        footer = page.wait_for_selector('.a-popover-footer')

        # Click the "Continue" button
        continue_button = footer.wait_for_selector("span[data-action='GLUXConfirmAction']")
        continue_button.click()

        print("Continue Clicked")

        # Wait for the pop-up content to disappear
        page.wait_for_selector("#a-popover-content-3", state="hidden")

        print("Popup Closed??")

        data_list = []  # List to store scraped data

        while True:
            page.wait_for_timeout(5000)  # Wait for 5 seconds (adjust as needed)

            product_cards = page.query_selector_all(".s-result-item")
            print(f"Number of Products : {len(product_cards)}")

            for card in product_cards:
                product_data = scrape_product_card(product_card=card)

                if product_data['asin'] != '':
                    data_list.append(product_data)  # Append the data to the list

            # Check if the "Next" button is disabled
            next_button = page.query_selector('.s-pagination-next')
            if next_button and next_button.get_attribute('aria-disabled') == 'true':
                print("No More Next")
                break  # Exit the loop if there's no "Next" button

            next_button.click()
            page.wait_for_selector(".s-result-item")
            print("Next Page")

        browser.close()

        # Specify the CSV file path
        csv_file_path = "C:/Users/kkoneru/Downloads/amazon_scrape/kenmore_amazon_prds.csv"
        field_names = ["asin", "product_name", "price"]

        # Open the CSV file in write mode and create a CSV writer
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data_list)


if __name__ == "__main__":
    main()
