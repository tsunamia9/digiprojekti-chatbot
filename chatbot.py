import streamlit as st
import os
import json
import random
import re

# --- CSS: poistetaan punainen reunavalo tekstikentästä ---
st.markdown("""
    <style>
    input:focus {
        outline: none !important;
        border: 1px solid #ccc !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Ladataan tuotteet JSON-tiedostosta ---
base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "tuotteet.json")

with open(file_path, "r", encoding="utf-8") as f:
    tuotteet = json.load(f)

st.title("Verkkokaupan Chatbot 🤖")
st.write("Hei! Olen verkkokaupan chatbot. Kuinka voin auttaa?")

# --- Tallennetaan keskustelu ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Funktio vastauksen hakemiseen ---
def get_vastaus(kysymys: str) -> str:
    kysymys = kysymys.lower()

    # Ystävälliset vastaukset
    tervehdykset = ["hei", "moi", "terve", "hello", "päivää"]
    kiitokset = ["kiitos", "thx", "thanks", "kiitti"]
    kehumiset = ["hyvä", "kiva", "mahtava", "paras", "super"]

    vastaukset = {
        "palautus": "Voit palauttaa tuotteet 30 päivän sisällä ostopäivästä.",
        "toimitus": "Toimitamme tuotteet 2–5 arkipäivässä.",
        "aukiolo": "Asiakaspalvelumme on auki ma–pe klo 9–17.",
        "maksutavat": "Hyväksymme Visa, Mastercard, PayPal ja Klarna-maksut.",
        "alennukset": "Tarjoamme satunnaisia kampanjoita ja uutiskirjeen tilaajille alennuksia.",
        "tilausseuranta": "Voit seurata tilaustasi sisäänkirjautumalla omalle tilillesi.",
        "vaihto": "Voit vaihtaa tuotteita 30 päivän sisällä, kunhan ne ovat käyttämättömiä.",
        "lahjakortti": "Tarjoamme lahjakortteja, jotka ovat voimassa 12 kuukautta ostopäivästä.",
        "tuki": "Voit ottaa yhteyttä asiakaspalveluumme sähköpostitse support@verkkokauppa.fi."
    }

    # 1) Tervehdys
    if any(sana in kysymys for sana in tervehdykset):
        return random.choice([
            "Hei! 😊 Miten voin auttaa sinua tänään?",
            "Moi! Miten voin olla avuksi?",
            "Terve! 😊 Mitä haluaisit tietää?"
        ])

    # 2) Kiitos
    if any(sana in kysymys for sana in kiitokset):
        return random.choice([
            "Ole hyvä! 💙 Kiva että pystyin auttamaan.",
            "Ei kestä! 😊",
            "Aina ilo auttaa!"
        ])

    # 3) Kehuminen
    if any(sana in kysymys for sana in kehumiset):
        return "Aww kiitos! 😄 Teen parhaani auttaakseni."

    # 4) Lopetus
    if kysymys == "lopeta":
        return "Näkemiin! Toivottavasti olin avuksi 😊"

    # 5) Tuotelistaus
    if kysymys.strip() == "tuotteet" or "näytä tuotte" in kysymys:
        lista = "\n".join(
            [f"- {t['nimi']} ({t['kategoria']}) – {t.get('hinta', 'Hinta ei saatavilla')}€" for t in tuotteet]
        )
        return f"Tässä meidän tuotteet:\n{lista}"

    # --- Avainsanat ---
    if re.search(r"\bpalaut(us)?\b", kysymys):
        return vastaukset["palautus"]
    if re.search(r"\b(toimitus|kuljetus|paket)\b", kysymys):
        return vastaukset["toimitus"]
    if re.search(r"\b(auki|ajat)\b", kysymys):
        return vastaukset["aukiolo"]
    if re.search(r"\b(maksu|kortti|paypal|klarna)\b", kysymys):
        return vastaukset["maksutavat"]
    if re.search(r"\b(alennus|kampanja)\b", kysymys):
        return vastaukset["alennukset"]
    if re.search(r"\b(tilausseuranta|seuranta)\b", kysymys):
        return vastaukset["tilausseuranta"]
    if re.search(r"\b(vaihto|vaihda)\b", kysymys):
        return vastaukset["vaihto"]
    if re.search(r"\b(lahjakortti|lahja)\b", kysymys):
        return vastaukset["lahjakortti"]
    if re.search(r"\b(tuki|yhteys)\b", kysymys):
        return vastaukset["tuki"]

    # --- Fallback, jos ei ymmärrä ---
    return (
        "Hmm… en ole varma mitä tarkoitit 🤔\n"
        "Ehkä haluat tietoa jostakin seuraavista:\n"
        "- Palautus- ja vaihto-ohjeet\n"
        "- Toimitusaika\n"
        "- Maksutavat\n"
        "- Alennukset ja kampanjat\n"
        "- Tilausseuranta\n"
        "- Aukioloajat\n"
        "- Lahjakortit\n"
        "- Asiakastuki"
    )

# --- Käyttäjän syöte ---
user_input = st.text_input("Kirjoita viesti:", value="", key="input")

# --- Tyhjennä keskustelu -nappi ---
if st.button("Tyhjennä keskustelu"):
    st.session_state.chat_history = []

# --- Logiikka vastauksen hakemiseen ---
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    vastaus = get_vastaus(user_input)
    st.session_state.chat_history.append(("assistant", vastaus))

# --- Chat-historia ---
for sender, msg in st.session_state.chat_history[-50:]:  # Näytetään max 50 viestiä
    st.chat_message(sender).write(msg)








