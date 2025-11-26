import pandas as pd
import re

# Chargement du CSV
df = pd.read_csv("paruvendu_villes_5pages.csv")

# Nettoyage Détails
df["Détails"] = df["Détails"].astype(str).str.replace("\n"," ").str.replace("\xa0"," ")

# Fonction simple
def parse_details(details_str):
    details_str = str(details_str)

    out = {
        "Pieces": None,
        "Chambres": None,
        "Garage": None,
        "Balcon": None,
        "Ascenseur": None,
        "Terrain_m2": None,
        "DPE": None,
        "Autre": None
    }

    # Pièces
    pieces_match = re.search(r"(\d+)(?:/(\d+))?\s*pi[eè]ce", details_str, re.I)
    if pieces_match:
        out["Pieces"] = pieces_match.group(0)

    # Chambres
    chambres_match = re.search(r"(\d+)\s*chambre", details_str, re.I)
    if chambres_match:
        out["Chambres"] = chambres_match.group(1)

    # Garage / Balcon / Ascenseur
    for col in ["Garage", "Balcon", "Ascenseur"]:
        if col.lower() in details_str.lower():
            out[col] = "Oui"

    # Terrain
    terrain_match = re.search(r"terrain\s*(\d+)", details_str, re.I)
    if terrain_match:
        out["Terrain_m2"] = terrain_match.group(1)

    # DPE
    dpe_match = re.search(r"DPE\s*:\s*([A-G])", details_str, re.I)
    if dpe_match:
        out["DPE"] = dpe_match.group(1)

    # Autre
    parts = [p.strip() for p in details_str.split(",")]
    known = ["pièce", "chambre", "garage", "balcon", "ascenseur", "terrain", "DPE"]
    other = [p for p in parts if not any(k in p.lower() for k in known)]

    if other:
        out["Autre"] = "; ".join(other)

    return out

# Parsing
details_df = df["Détails"].apply(parse_details).apply(pd.Series)

# Surface depuis le titre
def extract_surface(title):
    if pd.isna(title): 
        return None
    match = re.search(r"(\d+)\s*m²", title.replace("\xa0",""))
    return int(match.group(1)) if match else None

df["Surface_m2"] = df["Titre"].apply(extract_surface)

# CONCAT sans créer de doublons
df_final = pd.concat([df.drop(columns=["Détails"], errors="ignore"), details_df], axis=1)

df_final.to_csv("paruvendu_villes_detail.csv", index=False, encoding="utf-8")
print("OK : paruvendu_villes_detail.csv généré")
