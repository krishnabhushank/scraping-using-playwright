from playwright.sync_api import sync_playwright
import csv


def scrape_product_card(product_card):
    try:
        brand = product_card.query_selector('.product-title a span').text_content()
    except AttributeError:
        brand = 'NA'
    except KeyError:
        brand = 'NA'

    try:
        model = product_card.query_selector('.product-title a span.man-no').text_content().strip()
    except AttributeError:
        model = 'NA'
    except KeyError:
        model = 'NA'

    try:
        product_url = product_card.query_selector('.product-title a').get_attribute('href')
        product_url = 'https://www.abcwarehouse.com' + product_url
    except AttributeError:
        product_url = 'NA'
    except KeyError:
        product_url = 'NA'

    try:
        image_url = product_card.query_selector('img').get_attribute('src')
    except AttributeError:
        image_url = 'NA'
    except KeyError:
        image_url = 'NA'

    try:
        description = product_card.query_selector('.product-box-description').text_content()
    except AttributeError:
        description = 'NA'
    except KeyError:
        description = 'NA'

    try:
        original_price = product_card.query_selector('.price.old-price').text_content().strip(
            "Reg. Price").strip().replace(",", "")
    except AttributeError:
        original_price = 'NA'
    except KeyError:
        original_price = 'NA'

    try:
        sale_price = product_card.query_selector('.price.actual-price').text_content().replace(",", "")
    except AttributeError:
        sale_price = 'NA'
    except KeyError:
        sale_price = 'NA'

    return {
        'brand': brand,
        'model': model,
        'description': description,
        'original_price': original_price,
        'sale_price': sale_price,
        'product_url': product_url,
        'image_url': image_url
    }


def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # Set headless=True for headless mode
        page = browser.new_page()

        page.goto(
            "https://www.abcwarehouse.com/floorcare-accessories-2", timeout=50000)

        # Wait for the popup to open
        popup_loaded = page.wait_for_selector('.ltkpopup-close', timeout=50000)

        data_list = []  # List to store scraped data

        if popup_loaded:
            print("Popup is loaded")

            # Close the popup
            popup_loaded.click()

            current_page = 1
            while True:
                page.wait_for_timeout(5000)  # Wait for 5 seconds (adjust as needed)

                product_cards = page.query_selector_all(".product-item")

                print(f"Number of Products : {len(product_cards)}")

                for card in product_cards:
                    product_data = scrape_product_card(product_card=card)

                    if product_data['brand'] != '':
                        data_list.append(product_data)  # Append the data to the list

                # Check if the "Next" button is disabled
                next_button = page.query_selector('.next-page a')
                if not next_button:
                    print("No More Next")
                    break  # Exit the loop if there's no "Next" button

                current_page += 1
                print(f"Going to Page {current_page}")
                next_button.click()

                page.wait_for_selector('.current-page', state="attached").wait_for_element_state("visible")
                print("Next Page")

        browser.close()

        # Specify the CSV file path
        csv_file_path = "C:/Users/kkoneru/Downloads/abcwarehouse_scrape/abcwh_vacuums-floorcare-accessories-2.csv"
        field_names = ["brand", "model", "description", "original_price", "sale_price", "product_url", "image_url"]

        # Open the CSV file in write mode and create a CSV writer
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data_list)


if __name__ == "__main__":
    main()
