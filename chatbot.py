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

# Tallennetaan keskustelu
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Käyttäjän syöte
user_input = st.text_input("Kirjoita viesti:")

# Perusvastaukset
vastaukset = {
    "palautus": "Voit palauttaa tuotteet 30 päivän sisällä ostopäivästä.",
    "toimitus": "Toimitamme tuotteet 2–5 arkipäivässä.",
    "aukiolo": "Asiakaspalvelumme on auki ma–pe klo 9–17."
}

# --- LOGIIKKA ---
if user_input:
    kysymys = user_input.lower()
    st.session_state.chat_history.append(("user", user_input))

    # Lopetus
    if kysymys == "lopeta":
        vastaus = "Näkemiin! Toivottavasti olin avuksi."

    # Tuotelistaus
    elif "tuotte" in kysymys:
        lista = "\n".join([f"- {t['nimi']} ({t['kategoria']})" for t in tuotteet])
        vastaus = f"Tässä tuotteet:\n{lista}"

    # --- AVAINSANAEHTOJA ---
    elif "palaut" in kysymys:
        vastaus = vastaukset["palautus"]

    elif "toimit" in kysymys or "kuljet" in kysymys or "paket" in kysymys:
        vastaus = vastaukset["toimitus"]

    elif "auki" in kysymys or "ajat" in kysymys or "milloin olette auki" in kysymys:
        vastaus = vastaukset["aukiolo"]

    else:
        vastaus = "Valitettavasti en tiedä siitä. Kysy jotain muuta verkkokauppaan liittyvää."

    # Tallennetaan bottiviesti
    st.session_state.chat_history.append(("assistant", vastaus))


# --- CHATTINÄKYMÄ ---
for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)





