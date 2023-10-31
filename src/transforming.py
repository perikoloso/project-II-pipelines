
#TRANSFORMING

import deepl
from bs4 import BeautifulSoup
import requests
import time
import pandas as dp


def translate (text):
    auth_key = "84c8e09d-8b3c-646f-78a2-f03d894c2701:fx"  # Replace with your key
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang='ES')
    return result

def exe_translation(df):
    l_ins_esp=[]                  
    for i in df.index:
        l_ins_esp.append(translate(df["method"][i]))
    df["method_esp"] = l_ins_esp
    return df

def translated_df(df):
    l_serve = []
    l_garnish = []
    l_items = []
    l_nutrition = []
    l_dict = {}
    df_trans = df[df['diffords_url'] != 'Unknown']
    return df_trans

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("à", "a"),
        ("è", "e"),
        ("ì", "i"),
        ("ò", "o"),
        ("ù", "u"),
        ("cocktail",""),
        ("ç","c")
        
    )
    for a, b in replacements:
        s = s.replace(a, b)
    return s

def scrap_df_base (df): # Get main link from cocktails website to jump into details
    out_names = []
    out_href = []
    for x in df.index:
        n_cocktail = normalize(df["name"][x].strip())
        url = f"https://www.diffordsguide.com/cocktails/search?keyword%5B%5D={n_cocktail}&gentle_to_boozy%5B%5D=0&gentle_to_boozy%5B%5D=10&sweet_to_sour%5B%5D=0&sweet_to_sour%5B%5D=10&calories%5B%5D=0&calories%5B%5D=9"
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "html.parser")
        get_name = soup.find_all("h3",{"class":"box__title"})
        get_link = soup.find_all("a",{"class":"cell small-6 medium-3 large-2 box"})
        
        all_href = [i.get("href") for i in get_link]
        #all_names= [re.sub(r'\([^)]*\)', '', normalize(i.getText())).strip() for i in get_name]

        all_names= [i.getText().strip()[:len(n_cocktail)] for i in get_name]

        try:
            index = all_names.index(n_cocktail)
            out_names.append(all_names[index])
            out_href.append(all_href[index])
        except:
            out_names.append("Unknown")
            out_href.append("Unknown")
        time.sleep(1)
    df["diffords"] = out_names
    df["diffords_url"] = out_href
    return df

def scrap_details(df):
    l_serve = []
    l_garnish = []
    l_nutrition = []
    l_dict = {}

    for x in df.index:
        url_detail = "https://www.diffordsguide.com/"+df["diffords_url"][x]
        title = df["name"][x]
        res_detail = requests.get(url_detail)
        soup_detail = BeautifulSoup(res_detail.content, "html.parser")
        get_details = soup_detail.find_all("h3",{"class":""})
        l_dict['Glass']= ''
        l_dict['Garnish']= ''
        l_dict['Nutrition']= ''
        for i in get_details:
            if 'Serve in' in i.text:
                l_dict['Glass']=i.find_next('a').text.strip()
            if 'Garnish' in i.text:
                l_dict['Garnish']=i.find_next('p').text.strip()
            if 'Nutrition' in i.text:
                l_dict['Nutrition']=i.find_next('strong').text.replace("calories",'').strip()

        l_serve.append(l_dict['Glass'])
        l_garnish.append(l_dict['Garnish'])
        l_nutrition.append(l_dict['Nutrition'])

    df.loc[df["diffords_url"] != 'Unknown', "diff_glass"] = l_serve
    df.loc[df["diffords_url"] != 'Unknown', "diff_garnish"] = l_garnish
    df.loc[df["diffords_url"] != 'Unknown', "diff_nutrition"] = l_nutrition

    return df

def ingredients_dict(df):
    for i in df.index:
        try:
            elements = df["ingredients"][i].split(',')
            dict_ingr = {}
            for element in elements:
                if 'ml' in element:
                    quantity, ingredient = [i.strip() for i in element.split(' ml')]
                if 'pcs' in element:
                    quantity, ingredient = [i.strip() for i in element.split(' pc')]
                
                dict_ingr[ingredient] = quantity
                df["ingredients"][i] = dict_ingr
                return "Done!"
        except:
            print("Error: Dicts were already created.")
