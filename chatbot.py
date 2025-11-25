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
st.write("Hei! Olen verkkokaupan chatbot ja autan sinua mielelläni. Kuinka voin olla avuksi?")

# Tallennetaan keskustelu streamlitissä
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Käyttäjän syöte
user_input = st.text_input("Kirjoita viesti:")

vastaukset = {
    "palautus": "Voit palauttaa tuotteet 30 päivän sisällä ostopäivästä.",
    "toimitus": "Toimitamme tuotteet 2–5 arkipäivässä.",
    "aukiolo": "Asiakaspalvelumme on auki ma–pe klo 9–17."
}

# --- LOGIIKKA ---

if user_input:
    kysymys = user_input.lower()
    st.session_state.chat_history.append(("user", user_input))

    if kysymys == "lopeta":
        vastaus = "Näkemiin! Toivottavasti olin avuksi."
    
    elif kysymys == "tuotteet":
        lista = "\n".join([f"- {t['nimi']} ({t['kategoria']})" for t in tuotteet])
        vastaus = f"Meiltä löytyy seuraavat tuotteet:\n{lista}"

    else:
        vastaus = vastaukset.get(
            kysymys,
            "Valitettavasti en tiedä siitä. Kysy jotain muuta verkkokauppaan liittyvää."
        )

    st.session_state.chat_history.append(("assistant", vastaus))


# --- NÄYTETÄÄN KESKUSTELU CHATILLÄ ---

for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)




