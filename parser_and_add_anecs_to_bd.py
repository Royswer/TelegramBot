import requests
from bs4 import BeautifulSoup
import pickle
from db_manager import DB
import pickle


db_manager = DB()

def fetch_aneks(start_page, end_page):
    aneсs = []
    for i in range(start_page, end_page + 1):
        url = f'https://nekdo.ru/page/{i}'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'lxml')
        text_divs = soup.find_all('div', class_='text')
        category_divs = soup.find_all('div', class_='cat')
    
        for anec, cat in zip(text_divs, category_divs):
            cat_list = [a.text for a in cat.find_all('a')]
            text1 = anec.text.strip()
            aneсs.append({
                "text": text1,
                "categories": cat_list
            })
    return aneсs

def main(start_page, end_page):
    # anecs_list = fetch_aneks(start_page, end_page)
    # with open('anecdots.pickle', 'wb') as f:
    #     aneсs = pickle.dump(anecs_list,f)
    # return
    with open('anecdots.pickle', 'rb') as f:
        anecs_list = pickle.load(f)
    
    #Добавить категории в БД    
    
    categories = []
    for dict_ in anecs_list:
        anec = dict_['categories']
        for cat in anec:
            categories.append(cat)
    categories = list(set(categories))
    categories = [{'category': cat}for cat in categories]
    db_manager.add_cats(categories)

    mapping_cat = db_manager.get_id_category_full()
    for anec_dict in anecs_list:
        text = anec_dict['text']
        cat_list = anec_dict['categories']
        anec_id = db_manager.add_anec(text)
        for cat in cat_list:
            cat_id = mapping_cat[cat]
            if cat_id:
                db_manager.add_cats_anecs(cat_id, anec_id)
    #
        

    
import time
start = time.time()
main(1, 50)
end = time.time()
print(end - start)
#1min