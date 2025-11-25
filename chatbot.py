import streamlit as st
import os
import json

# Selvitetään tämän Python-tiedoston sijainti
base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "tuotteet.json")

# Ladataan tuotteet JSON-tiedostosta
with open(file_path, "r", encoding="utf-8") as f:
    tuotteet = json.load(f)

st.title("Verkkokaupan Chatbot")
st.write("Hei! Olen verkkokaupan chatbot 🤖 Kuinka voin auttaa?")

# Tallennetaan keskustelu ja chatbotin tila
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "odottaa_aspa_vastausta" not in st.session_state:
    st.session_state.odottaa_aspa_vastausta = False

# Käyttäjän syöte
user_input = st.text_input("Kirjoita viesti:")

# Perusvastaukset
vastaukset = {
    "palautus": "Voit palauttaa tuotteet 30 päivän sisällä ostopäivästä.",
    "toimitus": "Toimitamme tuotteet 2–5 arkipäivässä.",
    "aukiolo": "Asiakaspalvelumme on auki ma–pe klo 9–17."
}

asiakaspalvelu_tiedot = (
    "Tässä asiakaspalvelun yhteystiedot:\n"
    "📞 Puhelin: 010 123 4567\n"
    "📧 Sähköposti: asiakaspalvelu@verkkokauppa.fi\n"
    "🕑 Aukioloajat: ma–pe klo 9–17"
)

# --- LOGIIKKA ---
if use





