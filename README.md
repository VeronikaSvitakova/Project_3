# Project_3
Web Scraper Výsledků Voleb 2017
Tento skript v Pythonu slouží k extrakci výsledků voleb z roku 2017 z webu volby.cz. Umožňuje uživateli vybrat libovolný územní celek z odkazu (https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) a uložit výsledky do souboru CSV.

Použití
Výběr územního celku: Na stránce https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ vyberte požadovaný územní celek kliknutím na odkaz ve sloupci "Výběr obce".
Získání URL: Zkopírujte URL adresu vybraného územního celku.
Spuštění skriptu: Spusťte skript s dvěma argumenty: URL adresou územního celku a požadovaným názvem výstupního souboru s příponou .csv.
Kroky ke spuštění
Vytvoření virtuálního prostředí například ve windows:

python -m venv venv

Instalace závislostí: Nainstalujte potřebné knihovny ze souboru requirements.txt:

pip install -r requirements.txt
Spuštění skriptu: Spusťte skript Project_3.py s dvěma argumenty: URL adresou a názvem výstupního souboru. Například:

python Project_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4203" vysledky_litomerice.csv
Ukázkový výstup
V repozitáři je přiložen ukázkový výstupní soubor vysledky_litomerice.csv.

Požadavky
Python 3.6+
Knihovny uvedené v souboru requirements.txt (nainstalujete pomocí pip install -r requirements.txt).
Soubory v repozitáři
Project_3.py: Hlavní skript pro scraping dat.
requirements.txt: Soubor se seznamem závislostí.
vysledky_litomerice.csv: Ukázkový výstupní soubor.
