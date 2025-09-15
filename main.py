from fastapi import FastAPI
import spacy

# Message pour indiquer que le chargement commence (utile pour le démarrage sur Render)
print("Chargement du modèle SpaCy fr_dep_news_trf...")

# Charger le modèle SpaCy (plus lourd, mais plus précis)
# Ce chargement se fait une seule fois au démarrage de l'application.
nlp = spacy.load("fr_dep_news_trf")

print("Modèle chargé avec succès.")

# Créer l'application FastAPI
app = FastAPI()

# Définir le point d'entrée (endpoint) pour la lemmatisation
@app.post("/lemmatize")
def lemmatize_word(data: dict):
    word = data.get("word")
    if not word:
        return {"error": "Le champ 'word' est manquant."}

    # Traiter le mot avec SpaCy
    doc = nlp(word)
    
    # Extraire le lemme du premier token (mot)
    # On s'assure qu'il y a bien un token à analyser
    if len(doc) > 0:
        lemme = doc[0].lemma_
        return {"lemme": lemme}
    else:
        return {"lemme": word} # Retourne le mot original si l'analyse échoue

# Un point d'entrée simple pour vérifier que le service est en ligne
@app.get("/")
def read_root():
    return {"status": "API de lemmatisation SpaCy est en ligne"}
