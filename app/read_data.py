import pandas as pd
import streamlit as st
import re

# Fonction pour charger les données
@st.cache_data
def load_data(path):
    try:
        df = pd.read_csv(path,low_memory=False)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier {path} est introuvable. Veuillez vérifier son emplacement.")
    except Exception as e:
        raise RuntimeError(f"Une erreur est survenue lors du chargement des données: {str(e)}")
    

def count_unique_words(text):
    words = re.findall(r'\b\w+\b', str(text).lower())
    return len(set(words))

