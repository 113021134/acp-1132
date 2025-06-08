import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode

def getPerfume(productName):
    encoded_name = urlencode({'stext': productName})
    url = f"https://www.perfume.com/search/search_results?{encoded_name}"
    base_url = 'https://www.perfume.com/'

    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    product_div = soup.find('div', class_='top-products__item')
    
    if product_div:
        first_link = product_div.find('a')
        if first_link and first_link.get('href'):
            href = first_link['href']
            full_url = urljoin(base_url, href)
            print(f"Redirecting to: {full_url}")

            redirected_response = scraper.get(full_url)

            redirected_soup = BeautifulSoup(redirected_response.text, 'html.parser')

            out_of_stock = redirected_soup.find('div', class_='notify-all-out-of-stock')
            if out_of_stock:
                return "Out of stock!"
            else:
                price_span = redirected_soup.find('span', class_='sale-price-val')

                if price_span:
                    # print("Sale Price:", price_span.get_text(strip=True))
                    return price_span.get_text(strip=True)
                else:
                    return None
                    # print("No sale price span found.")
        else:
            # print("No <a> tag with href found inside the div.")
            return None
    else:
        return None
        # print("No matching div found.")

def getFragrancex(productName):
    encoded_name = productName.replace(' ', '+')
    url = f"https://www.fragrancex.com/search/search_results?stext={encoded_name}"
    base_url = 'https://www.fragrancex.com/'

    retry_count = 0
    max_retries = 10

    product_div = None

    while retry_count < max_retries:
        try:
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            product_div = soup.find('div', class_='product-img')

            if product_div != None:
                # print("found")
                break
            else:
                print(f"Retrying... ({retry_count + 1}/{max_retries})")
                retry_count += 1
        except Exception as e:
            print(f"Error occurred: {e}. Retrying... ({retry_count + 1}/{max_retries})")
            retry_count += 1

    
    if product_div:
        first_link = product_div.find('a')
        if first_link and first_link.get('href'):
            href = first_link['href']
            full_url = urljoin(base_url, href)
            print(f"Redirecting to: {full_url}")

            redirected_response = scraper.get(full_url)

            redirected_soup = BeautifulSoup(redirected_response.text, 'html.parser')

            price_meta = redirected_soup.find('meta', attrs={'itemprop': 'price'})
            if price_meta and price_meta.get('content'):
                price = price_meta['content']
                return price
            else:
                return "Out of stock!"
        else:
            return None
    else:
        return None


def getPrice(productName):
    print("Fetching prices for:", productName)
    perfume = getPerfume(productName)
    fragrancex = getFragrancex(productName)

    return {
        "perfume.com": perfume,
        "fragrancex.com": fragrancex,
    }