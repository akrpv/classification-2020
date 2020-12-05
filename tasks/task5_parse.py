from bs4 import BeautifulSoup
import requests
import pandas as pd

base_url = 'http://notelections.online'

def parse_uik(tik, df):
    soup = BeautifulSoup(requests.get(base_url + tik.get('href')).text, 'html.parser')
    table = soup.find_all('table', bgcolor='#ffffff', cellpadding='2', cellspacing='1')[-1].find_all('nobr')
    uik = len(soup.find_all('table', bgcolor='#ffffff', cellpadding='2', cellspacing='1')[-1].find_all('tr', valign='top')[0].find_all('td'))
    for i in range(uik):
        df.loc[len(df)] = [tik.text, *[table[j].text for j in range(i, i + uik * 14 + 1, uik)]]
    return df


def parse_to_df():
    df = pd.DataFrame({'ТИК':[], 'УИК':[]})
    response = requests.get(base_url + '/region/region/st-petersburg?action=show&root=1&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217417&type=222')
    soup = BeautifulSoup(response.text, 'html.parser')
    tiks = soup.find_all('a', style='text-decoration: none')
    soup_1 = BeautifulSoup(requests.get(base_url + tiks[0].get('href')).text, 'html.parser')
    candidati = soup_1.find_all('table', bgcolor='#ffffff', cellpadding='2', cellspacing='1')[0].find_all('td', style='color:black', align='left', width='50')
    for candidat in candidati:
        df[candidat.text] = 0
    cifr = tiks.pop(-1)
    for tik in tiks:
        df = parse_uik(tik, df)
    bs = BeautifulSoup(requests.get(base_url + cifr.get('href')).text, 'html.parser').find_all('table', bgcolor='#ffffff', cellpadding='2', cellspacing='1')[-1].find_all('b')
    t_b = [bs[i].text for i in range(len(bs))]
    t_b.pop(11)
    df.loc[len(df)] = [cifr.text, cifr.text, *t_b]
    df.to_csv('data/df_5_task.csv', index=False)
    return df

if __name__ == "__main__":
    df = parse_to_df()