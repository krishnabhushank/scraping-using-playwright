from playwright.sync_api import sync_playwright
import csv


def scrape_product_card(product_card):
    try:
        # Extract ASIN from the product detail link
        product_detail_link = product_card.query_selector(".ProductGridItem__itemInfo__wl2YN a")
        product_detail_href = product_detail_link.get_attribute("href")
        asin_start = product_detail_href.find("/dp/") + 4
        asin_end = product_detail_href.find("?")
        asin = product_detail_href[asin_start:asin_end]
    except AttributeError:
        asin = 'NA'
    except KeyError:
        asin = 'NA'

    try:
        product_name = product_card.query_selector(".Title__title__z5HRm").inner_text()
    except AttributeError:
        product_name = 'NA'
    except KeyError:
        product_name = 'NA'

    try:
        product_price = product_card.query_selector(".Price__price__LKpWT").get_attribute('aria-label')
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
            "https://www.amazon.com/stores/page/01F94996-F48C-403F-9FCE-B9DEBC804751?ingress=0&visitId=6cf09a3a-fa47-4bd1-b189-cca7463ffda9&lp_slot=auto-sparkle-hsa-tetris&store_ref=SB_A101631922AB4QMF2WZR8&ref_=sbx_be_s_sparkle_mcd_bkgd")

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

        page.wait_for_selector(".ProductGridItem__itemOuter__KUtvv.ProductGridItem__fixed__DQzmO")

        while True:
            # Check if the "Show more" button exists
            try:
                show_more_div = page.query_selector(".ShowMoreButton__gridMoreButton__U7_gf")
                show_more_button = show_more_div.query_selector(".Button__button__b_aG7")
                # Click the "Show more" button
                show_more_button.click()
                print("Show More Clicked")
                page.wait_for_timeout(20000)
            except AttributeError:
                break  # No more items to load, exit the loop
            except KeyError:
                break  # No more items to load, exit the loop

        data_list = []  # List to store scraped data

        page.wait_for_timeout(5000)  # Wait for 5 seconds (adjust as needed)

        page.wait_for_selector(".ProductGridItem__itemOuter__KUtvv.ProductGridItem__fixed__DQzmO")

        product_cards = page.query_selector_all(".ProductGridItem__itemOuter__KUtvv.ProductGridItem__fixed__DQzmO")
        print(f"Number of Products : {len(product_cards)}")

        for card in product_cards:
            product_data = scrape_product_card(product_card=card)

            if product_data['asin'] != '':
                data_list.append(product_data)  # Append the data to the list

        browser.close()

        # Specify the CSV file path
        csv_file_path = "C:/Users/kkoneru/Downloads/amazon_scrape/kenmore_sel_prds_on_amazon.csv"
        field_names = ["asin", "product_name", "price"]

        # Open the CSV file in write mode and create a CSV writer
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data_list)


if __name__ == "__main__":
    main()
