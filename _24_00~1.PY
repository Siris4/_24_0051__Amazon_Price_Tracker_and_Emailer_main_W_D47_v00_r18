
from bs4 import BeautifulSoup
import lxml
import requests
import smtplib, os

max_price_to_pay_for_product = 1470

url = "https://www.amazon.com.mx/King-6-8Kg-Chocolate-Ronnie-Coleman/dp/B010V80O6U/ref=sr_1_1?__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3HU8WC4XGEE1P&dib=eyJ2IjoiMSJ9.8zJrbK9-7ryYD1sv6SuB-9kebI1sRsdJjXV1x4TjWurcsuheh1yedYrLZ97__19cY0TZVYDAZT4f6CyDRZFnQm6maMvUhjmJgQc-exONqiJoNdo5s-z8eGnG_oW117HfODYQBkkwA6x7XienYSH-VQRoe5eRAjGv1dBo18eOWoZJKVU8a-mf3o3oDWMUfkud6w2Kb11BHRVnVwfBPp7VL_lqMic8wPUNShVbJqOqY1_IMCLxw_vXsjwIwYmr742mKfK4jHzQQ4BhDdEbQ43-viDFcNJUJ3VgjKp7WaFJCs4.6r3RdcQgrL_awo17kcdqz-ZP9eP4W6equPef6J1Dmlo&dib_tag=se&keywords=king+mass&qid=1709600277&sprefix=king+mass+%2Caps%2C131&sr=8-1&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47"
price_element = "<span class='a-price-whole'>1,469<span class='a-price-decimal'>.</span></span>"


# define your headers as a dictionary
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',   # removed: 'My App/1.0',
    'Accept-Language': 'en-US,en;q=0.9'
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',   # removed: 'application/json',
    # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
}

# you can now use response.text or response.json() to access the data returned by the server
response = requests.get(url, headers=headers)
# print(response.text)

#######################

soup = BeautifulSoup(response.content, "lxml")
print(soup.prettify())

import re

# using regular expression to extract digits from the price_element
price_digits = re.findall(r'\d+', price_element)

# joining the digits to form the complete price, then removing any commas
price_whole = ''.join(price_digits).replace(',', '')

# converting the joined string to an integer
price_number = float(price_whole)
price = (f"{price_number:.2f}")

print(f"The extracted price number is: {price}")


########################## Getting the Product Description from URL ####################

from urllib.parse import urlparse, unquote

parsed_url = urlparse(url)
path_segments = parsed_url.path.split('/')

product_title_segment = path_segments[1] if len(path_segments) > 1 else ''

# decodes the URL to convert chars back to text:
product_title = unquote(product_title_segment)

print(f"The title of this product is: {product_title}")



def send_email_to_myself():
    my_from_email1 = os.environ.get("MY_FROM_EMAIL1")
    password = os.environ.get("PASSWORD")

    their_email2 = os.environ.get("THEIR_EMAIL2")


    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:  # allows us to connect to our email provider's SMTP email server, and create an Object from the .SMTP(Class), location of the server (gmail = smtp.gmail.com)
        connection.starttls()  # tls = Transport Layer Security, a way of securing our connection to our email server. (encrypted and secure)) (indent block starts here)
        connection.login(user=my_from_email1, password=password)
        connection.sendmail(from_addr=my_from_email1,
                            to_addrs=their_email2,
                            msg=f"Subject:Amazon Price Drop Alert for {product_title}! \n\nYour product: {product_title} just reached a price of ${price}, which is lower than your desired price of ${max_price_to_pay_for_product}.\nHave a great day! -siris.Developer"  # (indent block ends here.)
                            )  # Subject field goes inside the msg=parameter: + \n\n

if price_number <= max_price_to_pay_for_product:
    send_email_to_myself()
    print("\nEmail sent!")


# print(f"The split price element is: {price_element.split()}")

# span_price_whole = soup.find("span", class_="a-price-whole").get_text()
# print(f"span price whole is: {span_price_whole}")
#
#
# price_whole = soup.find(class_="a-price-whole").text
# print(f"price whole is: {price_whole}")
#
# price_whole = soup.find(class_="a-price-whole").text()
# print(f"price whole is: {price_whole}")
#
# span_price_decimal = soup.find("span", class_="a-price-decimal").get_text
# print(f"span price decimal is: {span_price_decimal}")
#
# price_decimal = soup.find(class_="a-price-decimal").getText()
# print(f"price decimal is: {price_decimal}")
#
# price_decimal = soup.find(class_="a-price-decimal").get_text()
# print(f"price decimal is: {price_decimal}")

# stories = soup.find_all('tr', class_='athing')