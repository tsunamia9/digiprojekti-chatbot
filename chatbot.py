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

if user_input:
    kysymys = user_input.lower()
    
    if kysymys == "lopeta":
        vastaus = "Botti: Näkemiin! Toivottavasti olin avuksi."
        st.session_state.chat_history.append(("Sinä", user_input))
        st.session_state.chat_history.append(("Botti", vastaus))
        
    elif kysymys == "tuotteet":
        lista = "\n".join([f"- {t['nimi']} ({t['kategoria']})" for t in tuotteet])
        vastaus = f"Botti: Meiltä löytyy seuraavat tuotteet:\n{lista}"
        st.session_state.chat_history.append(("Sinä", user_input))
        st.session_state.chat_history.append(("Botti", vastaus))
        
    else:
        vastaus = vastaukset.get(kysymys, "Botti: Valitettavasti en tiedä siitä. Kysy jotain muuta verkkokauppaan liittyvää.")
        st.session_state.chat_history.append(("Sinä", user_input))
        st.session_state.chat_history.append(("Botti", vastaus))

# Näytetään keskusteluhistoria
for sender, msg in st.session_state.chat_history:
    st.write(f"**{sender}:** {msg}")
