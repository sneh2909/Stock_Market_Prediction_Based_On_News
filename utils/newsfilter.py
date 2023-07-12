import requests
import pandas as pd




def get_api_key() -> str:
    with open('newsfilter_key.txt', 'r') as file:
        key = file.readline()
        return key
    

def query_api(company_symbol:str, start_date:str, end_date:str, startPoint:int, size:int):
    API_KEY = get_api_key()
    API_ENDPOINT = f"https://api.newsfilter.io/search?token={API_KEY}"

    queryString = f"symbols:{company_symbol} AND publishedAt:[{start_date} TO {end_date}]"    

    payload = {
        "queryString": queryString,
        "from": startPoint,
        "size": size
    }

    response = requests.post(API_ENDPOINT, json=payload)

    return response.json()


def append_details(articles:dict, df:dict) -> dict:

    for article in articles['articles']:
        df['title'].append(article['title'])
        df['description'].append(article['description'])
        df['sectors'].append(article['sectors'])
        df['industries'].append(article['industries'])
        df['source'].append(article['source']['name'])
        df['publishedAt'].append(article['publishedAt'])
    
    return df


def get_data(company_symbol:str, start_date:str, end_date:str) -> pd.DataFrame:
    df = {
        "title": [],
        "description": [],
        "sectors": [],
        "industries": [],
        "source": [],
        "publishedAt": []
    }

    startPoint = 0
    size  = -1
    while True:
        articles = query_api(company_symbol, start_date, end_date, startPoint, size)
        df = append_details(articles, df)
        print(f"Received {startPoint} to {startPoint + len(articles['articles']) - 1}")

        if len(articles['articles']) < 50:
            break

        startPoint += 50

    df = pd.DataFrame(df)
    return df