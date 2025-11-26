from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# ------------------------------

# CONFIGURATION

# ------------------------------

VILLE = "marseille"
PAGE = 1
URL = f"[https://www.paruvendu.fr/immobilier/vente/{VILLE}/?p={PAGE}&allp=1](https://www.paruvendu.fr/immobilier/vente/{VILLE}/?p={PAGE}&allp=1)"

# Chemin vers le chromedriver (à adapter selon ton installation)

CHROMEDRIVER_PATH = "C:/chromedriver/chromedriver.exe"  # Modifier si nécessaire

# ------------------------------

# LANCER SELENIUM

# ------------------------------

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.get(URL)

# Laisser le temps à la page de charger le JS

time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

# ------------------------------

# EXTRACTION DES ANNONCES

# ------------------------------

annonces = soup.find_all("div", class_="blocAnnonce")

if not annonces:
    print("Aucune annonce trouvée sur cette page.")
else:
    for idx, a in enumerate(annonces, 1):

# Titre
        titre_tag = a.find("h2")
        titre = titre_tag.text.strip() if titre_tag else "N/A"

# Prix
prix_tag = a.find("span", class_="prix")
prix = prix_tag.text.strip() if prix_tag else "N/A"
    
    # Lien
lien_tag = a.find("a", href=True)
lien = "https://www.paruvendu.fr" + lien_tag['href'] if lien_tag else "N/A"
    
print(f"Annonce {idx}:")
print(f"  Titre : {titre}")
print(f"  Prix  : {prix}")
print(f"  Lien  : {lien}\n")


# ------------------------------

# FERMER LE NAVIGATEUR

# ------------------------------

driver.quit()
