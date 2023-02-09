import json
import re
import requests
from bs4 import BeautifulSoup


def get_url(url, save_path):
    count = 0
    result=[]
    response = requests.get(url)
    print((response.status_code))
    soup = BeautifulSoup(response.text, 'lxml')
    page_count = 4


    for i in range(1, page_count + 1, 1):
        response2 = requests.get(f'{url}?page={i}')
        soup2 = BeautifulSoup(response2.text, 'lxml')
        links = soup2.find_all('div', class_='product__item-narrow')
        for link in links:
            try:
                result.append({'links': 'https://www.sulpak.kz' + link.find('a').get('href')})
                count += 1
            except:
                print("error")

            print(f"Salem Sagan Kalamkas: {count}")



    with open(f'{save_path}/main_links.json', 'w') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def get_data(path):
    data = json.load(open((path)))
    main_characteristics = []
    count = 0

    for item in data:
        characteristic = []
        response = requests.get(item. get('links'))
        soup = BeautifulSoup(response.text, 'lxml')

        title = soup.find('h1', class_='title__large product__header-js').text.strip()

        product_code = re.sub(r'\bКод товара: \b', '', soup.find('div', class_='title__block-info').text.strip(), flags = re.IGNORECASE)

        product__characteristics = soup.find_all('div', class_='product__characteristics-items')


        for i in product__characteristics:
            characteristic_title = i.find('div', class_='product__characteristics-item-title').text.strip()

            value = i.find('div', class_='product__characteristics-item-val').text.strip()

            characteristic.append({f'{characteristic_title}': f'{value}'})

        try:
            main_characteristics.append({
                'title': title,
                'product_code': product_code,
                'characteristics': characteristic
            })
            count += 1
            print(f'data parsed: {count}')
        except:
            print("error")



    with open(f'/Users/nurmukhanbet/Desktop/kolesa/main_ch2.json', 'w') as file:
        json.dump(main_characteristics, file, indent=4, ensure_ascii=False)


def main():
    save_path = r'/Users/nurmukhanbet/Desktop/kolesa'
    get_url("https://www.sulpak.kz/f/noutbuki/astana", save_path)
    get_data(f'{save_path}/main_links.json')




if __name__ == '__main__':
    main()

