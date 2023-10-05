import time

from playwright.sync_api import sync_playwright
import csv


def scrape_product_card(product_card):
    data_modelcode = product_card.get_attribute("data-modelcode")

    try:
        product_name_element = product_card.query_selector("h2.ProductName-title-3949175622")
        description = product_name_element.text_content()
    except AttributeError:
        description = 'NA'
    except KeyError:
        description = 'NA'

    try:
        was_price_element = product_card.query_selector("span.Product-card__price-suggested-pf")
        original_price = was_price_element.text_content().strip().replace(",", "")
    except AttributeError:
        original_price = 'NA'
    except KeyError:
        original_price = 'NA'

    try:
        price_element = product_card.query_selector("span.Product-card__price-current-pf")
        sale_price = price_element.text_content().strip().replace(",", "")
    except AttributeError:
        sale_price = 'NA'
    except KeyError:
        sale_price = 'NA'

    try:
        image_url_element = product_card.query_selector("img.ImageGallery-image-1120567176")
        image_url = image_url_element.get_attribute("src")
    except AttributeError:
        image_url = 'NA'
    except KeyError:
        image_url = 'NA'

    try:
        product_url_element = product_card.query_selector("a.ProductCard-anchorWrapper_img-2277868790")
        product_url = "https://www.samsung.com" + product_url_element.get_attribute("href")
    except AttributeError:
        product_url = 'NA'
    except KeyError:
        product_url = 'NA'

    return {
        'brand': "Samsung",
        'model': data_modelcode,
        'description': description,
        'original_price': original_price,
        'sale_price': sale_price,
        'product_url': product_url,
        'image_url': image_url
    }


def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # Set headless=True for headless mode

        # Create a new browser context
        context = browser.new_context()

        # Read the CSV file
        with open('C:/Users/kkoneru/Downloads/samsung_scrape/samsung_ref_2_sel.csv', 'r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                link = row['Link']
                file_name = row['File_Name']
                csv_file_path = "C:/Users/kkoneru/Downloads/samsung_scrape/" + file_name

                page = browser.new_page()

                print(file_name)
                page.goto(link, timeout=80000)

                try:
                    # Wait for the popup to appear (you might need to adjust the selector)
                    popup = page.wait_for_selector('.bx-creative-1553762')
                    # Click the close button
                    popup.click('a#bx-close-inside-1553762')
                except Exception as e:
                    print(f"Error: {e}")
                    # Handle the case where the popup doesn't appear

                try:
                    # Wait for the popup to appear (you might need to adjust the selector)
                    popup = page.wait_for_selector('.bx-creative-2285566')
                    # Click the close button
                    popup.click('#bx-close-inside-2285566')
                except Exception as e:
                    print(f"Error: {e}")
                    # Handle the case where the popup doesn't appear

                data_list = []  # List to store scraped data

                # Function to click the "View More" button and wait for content to load
                def click_view_more():
                    try:
                        print("Clicking for more")
                        page.click(".FooterControlBar-viewMoreButton-1605513253")
                        page.wait_for_selector('.ProductCard-root-3423567336')
                        return True
                    except:
                        return False

                # Click "View More" until no more button is found
                while click_view_more():
                    time.sleep(5)  # Adjust the delay based on the page loading speed

                # Scroll down to load any remaining content
                previous_page_height = page.evaluate('() => document.body.scrollHeight')
                while True:
                    page.keyboard.press('End')
                    time.sleep(2)  # Adjust the delay based on the page loading speed
                    current_page_height = page.evaluate('() => document.body.scrollHeight')
                    if current_page_height == previous_page_height:
                        break
                    previous_page_height = current_page_height

                # Find all product cards
                product_cards = page.query_selector_all("section.ProductCard-root-3423567336")

                print(f"Number of Products : {len(product_cards)}")

                for card in product_cards:
                    product_data = scrape_product_card(product_card=card)

                    if product_data['brand'] != '':
                        data_list.append(product_data)  # Append the data to the list

                # Close the page
                page.close()

                # Specify the CSV file path
                # csv_file_path = "C:/Users/kkoneru/Downloads/samsung_scrape/mobile_tablets.csv"
                field_names = ["brand", "model", "description", "original_price", "sale_price", "product_url", "image_url"]

                # Open the CSV file in write mode and create a CSV writer
                with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerows(data_list)

        # Close the browser
        context.close()

if __name__ == "__main__":
    main()
