"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Veronika Svitakova
email: svitakovaveronika16@gmail.com
discord: veronikasvitakova_67296
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys
import re

Base_URL = "https://www.volby.cz/pls/ps2017nss/"


def fetch_url(url):
    """Stáhne obsah URL a vrátí BeautifulSoup objekt."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException:
        return None


def get_municipal_links(district_url):
    """Získá odkazy na obce z URL okresu."""
    soup = fetch_url(district_url)
    if not soup:
        return []

    municipality_links = []
    for row in soup.find_all('tr')[2:]:
        cells = row.find_all('td')
        if len(cells) > 2:
            code = cells[0].text.strip()
            name = cells[1].text.strip()
            link = cells[0].find('a')
            if link:
                full_link = Base_URL + link['href']
                municipality_links.append((code, name, full_link))

    return municipality_links


def parse_summary_table(soup):
    """Získá souhrnné údaje o voličích a hlasech."""
    summary_table = soup.find('table', {'id': 'ps311_t1'})
    if not summary_table:
        return ["", "", ""]

    data_cells = summary_table.find_all('td', {'data-rel': 'L1'})
    if len(data_cells) < 3:
        return ["", "", ""]

    return [
        data_cells[0].text.replace('\xa0', '').strip(),
        data_cells[1].text.replace('\xa0', '').strip(),
        data_cells[3].text.replace('\xa0', '').strip()
    ]


def parse_party_results(soup):
    """Získá výsledky voleb jednotlivých stran."""
    party_tables = soup.find_all('table', {'class': 'table'})
    party_names = []
    votes_results = []

    for table in party_tables[1:]:  # První tabulka obsahuje obecné informace
        for row in table.find_all('tr')[2:]:
            cells = row.find_all('td')
            if len(cells) > 2:
                try:
                    party_names.append(cells[1].text.strip())
                    votes_results.append(cells[2].text.replace('\xa0', '').strip())
                except IndexError:
                    pass

    return party_names, votes_results


def get_municipality_results(municipality_url):
    """Získá výsledky voleb pro obec."""
    soup = fetch_url(municipality_url)
    if not soup:
        return [], [], []

    summary_results = parse_summary_table(soup)
    party_names, votes_results = parse_party_results(soup)

    return summary_results, party_names, votes_results


def write_results_to_csv(output_file, municipalities, party_names):
    """Zapíše výsledky do CSV souboru."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"] + party_names
        writer.writerow(header)

        for code, name, link in municipalities:
            results, _, votes_results = get_municipality_results(link)
            writer.writerow([code, name] + results + votes_results)


def validate_input_args():
    """Validuje vstupní argumenty skriptu."""
    if len(sys.argv) != 3:
        print("Použití: python scraper.py <URL> <výstupní_soubor.csv>")
        sys.exit(1)

    district_url = sys.argv[1]
    output_file = sys.argv[2]

    if not re.match(r"^https://www\.volby\.cz/pls/ps2017nss/ps3[0-9]+\?", district_url):
        print("Chybný formát URL. Zkontrolujte zadaný odkaz.")
        sys.exit(1)

    return district_url, output_file


def main():
    """Hlavní funkce skriptu."""
    district_url, output_file = validate_input_args()

    municipalities = get_municipal_links(district_url)
    if not municipalities:
        print("Nepodařilo se najít žádné obce. Zkontrolujte URL.")
        sys.exit(1)

    first_municipality = municipalities[0][2]
    _, party_names, _ = get_municipality_results(first_municipality)

    write_results_to_csv(output_file, municipalities, party_names)
    print(f"Výsledky uloženy do {output_file}")


if __name__ == "__main__":
    main()
