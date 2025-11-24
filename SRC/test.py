import string
import requests

def get_all_villes():
    url = "https://www.paruvendu.fr/communfo/defaultcommunfo/defaultcommunfo/autocompleteLocalisation"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.paruvendu.fr/",
    }

    all_villes = {}

    for letter in string.ascii_lowercase:
        params = {
            "avecCodePostal": 1,
            "term": letter
        }

        print(f"🔎 Requête pour lettre : {letter}")

        r = requests.get(url, headers=headers, params=params)

        # Vérifier si la réponse est bien du JSON
        try:
            data = r.json()
        except Exception as e:
            print("❌ Réponse NON JSON :", r.text[:200])
            continue

        # Stocker les villes
        for item in data:
            key = item.get("value")
            if key:
                all_villes[key] = item

    return all_villes


villes = get_all_villes()
print("📌 Nombre total de villes trouvées :", len(villes))
print("🔽 Quelques villes :", list(villes.keys())[:20])