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
                return { "message": "Out of stock!", "url": full_url, "logo": "https://img.perfume.com/images/perfume_logo.svg?v=2"}
            else:
                price_span = redirected_soup.find('span', class_='sale-price-val')

                if price_span:
                    price = price_span.get_text(strip=True)
                    return { "message": "$"+price, "url": full_url, "logo": "https://img.perfume.com/images/perfume_logo.svg?v=2" }
                else:
                    return { "message": "Out of stock", "url": full_url, "logo": "https://img.perfume.com/images/perfume_logo.svg?v=2" }
        else:
            return { "message": "N/A", "url": "", "logo": "https://img.perfume.com/images/perfume_logo.svg?v=2" }
    else:
        return { "message": "N/A", "url": "", "logo": "https://img.perfume.com/images/perfume_logo.svg?v=2" }

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
                return { "message": "$"+price, "url": full_url, "logo": "https://cloud.shopback.com/c_fit,h_750,w_750/store-service-tw/assets/22694/d8b08f90-1360-11eb-b53a-f7f3a95c0c22.png"}
            else:
                return { "message": "Out of stock!", "url": full_url, "logo": "https://cloud.shopback.com/c_fit,h_750,w_750/store-service-tw/assets/22694/d8b08f90-1360-11eb-b53a-f7f3a95c0c22.png"}
        else:
            return {"message": "N/A", "url": url, "logo": "https://cloud.shopback.com/c_fit,h_750,w_750/store-service-tw/assets/22694/d8b08f90-1360-11eb-b53a-f7f3a95c0c22.png"}

    else:
        return {"message": "N/A", "url": url, "logo": "https://cloud.shopback.com/c_fit,h_750,w_750/store-service-tw/assets/22694/d8b08f90-1360-11eb-b53a-f7f3a95c0c22.png"}


def fragranceOutlet(productName):
    encoded_name = urlencode({'q': productName})
    url = f"https://www.fragranceoutlet.com/pages/search-results-page?{encoded_name}"
    base_url = 'https://www.fragranceoutlet.com/'

    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    unavailable = soup.find('div', class_='no-result')
    if unavailable:
        return {"message": "N/A", "url": url, "logo": "https://cdn-files.eu.placewise.com/f/CJEIEKIDGgpzdG9yZV9sb2dvIgcxMDA3MjM2OOyQvjq6cfGMIzE48Ko2XeE_1J6-"}

    
    products = soup.find('ul', class_="cm-varient-list")
    # print(response.status_code)
    li_items = products.find_all('li')

    last_li = li_items[-1]

    # Extract the data-price attribute
    price = last_li['data-price']
    return {"message": "$"+price, "url": url, "logo": "https://cdn-files.eu.placewise.com/f/CJEIEKIDGgpzdG9yZV9sb2dvIgcxMDA3MjM2OOyQvjq6cfGMIzE48Ko2XeE_1J6-" }
    
def notino(productName):
    encoded_name = productName.replace(' ', '%20')
    url = f"https://www.notino.co.uk/search.asp?exps={encoded_name}"
    base_url = 'https://www.notino.co.uk/'
    # print(url)
    scraper = cloudscraper.create_scraper()
    # response = scraper.get(url)
    response = scraper.get(base_url)

    soup = BeautifulSoup(response.text, 'html.parser')
    
    product_div = soup.find('data-testid', 'product-container')
    # print(response.status_code)
    if product_div:
        print("onok")
        # first_link = product_div.find('a')
        # if first_link and first_link.get('href'):
        #     href = first_link['href']
        #     full_url = urljoin(base_url, href)
        #     print(f"Redirecting to: {full_url}")

        #     redirected_response = scraper.get(full_url)

        #     redirected_soup = BeautifulSoup(redirected_response.text, 'html.parser')

        #     price_span = redirected_soup.find('span', class_='price-item price-item--sale price-item--last')

        #     if price_span:
        #         price = price_span.get_text(strip=True)
        #         return {"message": price, "url": full_url, "logo": "https://cdn-files.eu.placewise.com/f/CJEIEKIDGgpzdG9yZV9sb2dvIgcxMDA3MjM2OOyQvjq6cfGMIzE48Ko2XeE_1J6-" }
        #     else:
        #         return {"message": "out of stock", "url": full_url, "logo": "https://cdn-files.eu.placewise.com/f/CJEIEKIDGgpzdG9yZV9sb2dvIgcxMDA3MjM2OOyQvjq6cfGMIzE48Ko2XeE_1J6-" }
        # else:
        #     return None
    else:
        return None
    
def lookfantastic(productName):
    encoded_name = urlencode({'q': productName})
    # encoded_name = productName.replace(' ', '%20')
    url = f"https://www.lookfantastic.com/search/?{encoded_name}"
    base_url = 'https://www.lookfantastic.com/'
    
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    price_section = soup.find('p', class_='text-sm mt-1 price override-price-style')
    print(price_section)
    if price_section == None:
        return {"message": "N/A", "url": url, "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAFFXEcz7OuqNNGsU2xmFOiX2aFsAz3OfWLQ&s"}

    spans = price_section.find_all('span')

    # Get the last span
    current_price = spans[-1].text.strip()
    # print(current_price[1:])
    
    return {"message": current_price[1:], "url": url, "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAFFXEcz7OuqNNGsU2xmFOiX2aFsAz3OfWLQ&s"}


def getPrice(productName):
    print("Fetching prices for:", productName)

    perfume = getPerfume(productName)
    fragrancex = getFragrancex(productName)
    fragranceotlet = fragranceOutlet(productName)
    lookfantas = lookfantastic(productName)

    print(perfume)
    print(fragrancex)
    print(fragranceotlet)
    print(lookfantas)

    return {
        "perfume.com": perfume,
        "fragrancex.com": fragrancex,
        "fragranceoutlet.com": fragranceotlet,
        "lookfantastic.com": lookfantas
    }