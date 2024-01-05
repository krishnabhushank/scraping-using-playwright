from playwright.sync_api import sync_playwright
import csv


def scrape_product_card(product_card):
    link = "https://www.walmart.com" + product_card.query_selector(
        '.sans-serif.mid-gray.relative.flex.flex-column.w-100.hide-child-opacity a').get_attribute('href')

    try:
        product_name = product_card.query_selector('.w_iUH7').inner_text()
    except AttributeError:
        product_name = 'NA'
    except KeyError:
        product_name = 'NA'

    try:
        product_price = product_card.query_selector('.flex.flex-wrap.justify-start.items-center.lh-title.mb1').query_selector('.w_iUH7').inner_text()
    except AttributeError:
        product_price = 'NA'
    except KeyError:
        product_price = 'NA'

    return {
        'brand_name': 'koolatron',
        'product_name': product_name,
        'price': product_price,
        'link': link
    }


def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # Set headless=True for headless mode
        page = browser.new_page()

        page.goto(
            "https://www.walmart.com/search?q=koolatron&affinityOverride=default&facet=brand%3AKoolatron")

        # Wait for a specific amount of time before clicking "Apply"
        page.wait_for_timeout(2000)  # Wait for 2 seconds (adjust as needed)

        data_list = []  # List to store scraped data

        page_number = 1
        while True:
            page.wait_for_timeout(5000)  # Wait for 5 seconds (adjust as needed)

            print(f"Page {page_number}")
            product_cards = page.query_selector_all(".mb0.ph1.pa0-xl.bb.b--near-white.w-25")
            print(f"Number of Products : {len(product_cards)}")

            for card in product_cards:
                product_data = scrape_product_card(product_card=card)

                data_list.append(product_data)  # Append the data to the list

            # Check if the "Next" button is disabled
            next_page_button = page.query_selector('a[data-testid="NextPage"]')
            if next_page_button:
                # Click on the next page button
                next_page_button.click()
                page_number += 1
            else:
                break

            page.wait_for_selector(".mb0.ph1.pa0-xl.bb.b--near-white.w-25")
            print("Next Page")

        browser.close()

        # Specify the CSV file path
        csv_file_path = "C:/Users/kkoneru/Downloads/amazon_scrape/koolatron_walmart_prds.csv"
        field_names = ["brand_name", "product_name", "price", "link"]

        # Open the CSV file in write mode and create a CSV writer
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data_list)


if __name__ == "__main__":
    main()
