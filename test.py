import sqlite3
import requests
from bs4 import BeautifulSoup

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('keyboards.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            url TEXT
        )
    ''')
  
    conn.commit()
    conn.close()

# Insert data into the database
def insert_data(name, price, url):
    conn = sqlite3.connect('keyboards.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO products (name, price, url) VALUES (?, ?, ?)",
                   (name, price, url))
    print(f'INSERT INTO products (name, price, url) VALUES (?, ?, ?), {name, price, url}\n')
    conn.commit()
    conn.close()


def scrape_site_1():
    page_number  = 1
    while True:
        url = f"https://www.sancta-domenica.hr/racunala-i-periferija/tipkovnice-misevi-i-pc-audio/tipkovnice.html?luceed_tipkovnica_tip=26372&p={page_number}"  
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        if soup.find('div', class_= "message info empty") is not None:
            break

        products = soup.select('.item.product.product-item')  

        print(f"scraping page: {page_number}...")
        
        for product in products:
         
            name_text = product.select_one('.product-item-name a').get_text(strip=True)
            name = name_text.split(',')[0]
            price_text = product.select_one('.price').get_text(strip=True)
            price = float(price_text.replace(',', '.').replace('€', '').strip())
            link = product.select_one('.product-item-photo')['href']
                
            #print(f"Product: {name}\nPrice:{price}\nlink:{link}\n\n")
            insert_data(name,price,link)
        page_number += 1

def scrape_site_2():
    while True:
        url = f"https://www.instar-informatika.hr/gaming-tipkovnice/491/?p=8&s=24"  
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        product_items = soup.select('.product-item-box')  # Select product items
    
        for item in product_items:
            # Extract product name
            name_text = item.get('data-product_name', '').strip()
            name = name_text.split(',')[0]
            
            # Extract product price
            price_text = item.get('data-product_price', '').strip()
            price = float(price_text.replace(',', '.')) if price_text else None
            
            # Extract product link
            link_tag = item.select_one('.product-image a')
            link = link_tag['href'] if link_tag else None
            
            # Base URL to form complete link (replace with the actual base URL)
            base_url = "https://www.instar-informatika.hr"
            full_link = base_url + link if link else None
            
            insert_data(name,price,full_link)
        break
# Function to print the contents of the database
def print_database_contents():
    conn = sqlite3.connect('keyboards.db')
    cursor = conn.cursor()
    
    # Correct query using GROUP_CONCAT with ORDER BY
    cursor.execute("""
    SELECT 
        LOWER(name) AS normalized_name, 
        GROUP_CONCAT(DISTINCT price) AS prices,
        GROUP_CONCAT(DISTINCT url) AS urls
    FROM 
        products
    GROUP BY 
        normalized_name;
    """)
    
    # Fetch all results
    rows = cursor.fetchall()
    
    # Check if the table has any data
    if rows:
        for row in rows:
            normalized_name, prices, urls = row
            # Display the output with appropriate formatting
            print(f"Name: {normalized_name.capitalize()}")
            print(f"Prices: {prices}")
            print(f"URLs: {urls}")
            print('-' * 40)
    else:
        print("No data found in the database.")
    
    conn.close()

def drop_table(table_name):
    conn = sqlite3.connect('keyboards.db')
    cursor = conn.cursor()
    
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    print(f"Table {table_name} dropped successfully.")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    drop_table("keyboards.db")
    scrape_site_1()
    scrape_site_2()
    print_database_contents()
