import streamlit as st
import os
import json

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


# Selvitetään tämän Python-tiedoston sijainti
base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "tuotteet.json")

# Ladataan tuotteet JSON-tiedostosta
with open(file_path, "r", encoding="utf-8") as f:
    tuotteet = json.load(f)

st.title("Verkkokaupan Chatbot 🤖")
st.write("Hei! Olen verkkokaupan chatbot. Kuinka voin auttaa?")

# Tallennetaan keskustelu
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Käyttäjän syöte (lisätty key)
user_input = st.text_input("Kirjoita viesti:", key="input")

# Perusvastaukset
vastaukset = {
    "palautus": "Voit palauttaa tuotteet 30 päivän sisällä ostopäivästä.",
    "toimitus": "Toimitamme tuotteet 2–5 arkipäivässä.",
    "aukiolo": "Asiakaspalvelumme on auki ma–pe klo 9–17."
}

# Ystävälliset vastausmallit
tervehdykset = ["hei", "moi", "terve", "hello", "päivää"]
kiitokset = ["kiitos", "thx", "thanks", "kiitti"]
kehumiset = ["hyvä", "kiva", "mahtava", "paras", "super"]

# --- LOGIIKKA ---
if user_input:
    kysymys = user_input.lower()
    st.session_state.chat_history.append(("user", user_input))

    # Tyhjennetään syöttökenttä heti kun viesti on lähetetty
    st.session_state.input = ""

    # 1) Tervehdys
    if any(sana in kysymys for sana in tervehdykset):
        vastaus = "Hei! 😊 Miten voin auttaa sinua tänään?"

    # 2) Kiitos
    elif any(sana in kysymys for sana in kiitokset):
        vastaus = "Ole hyvä! 💙 Kiva että pystyin auttamaan."

    # 3) Kehuminen
    elif any(sana in kysymys for sana in kehumiset):
        vastaus = "Aww kiitos! 😄 Teen parhaani auttaakseni."

    # 4) Lopetus
    elif kysymys == "lopeta":
        vastaus = "Näkemiin! Toivottavasti olin avuksi 😊"

    # 5) Tuotelistaus (korjattu ettei reagoi palautus-lauseisiin)
    elif kysymys.strip() == "tuotteet" or "näytä tuotte" in kysymys:
        lista = "\n".join([f"- {t['nimi']} ({t['kategoria']})" for t in tuotteet])
        vastaus = f"Tässä meidän tuotteet:\n{lista}"

    # --- AVAINSANAEHTOJA ---
    elif "palaut" in kysymys:
        vastaus = vastaukset["palautus"]

    elif ("toimit" in kysymys or 
          "kuljet" in kysymys or 
          "paket" in kysymys):
        vastaus = vastaukset["toimitus"]

    elif "auki" in kysymys or "ajat" in kysymys:
        vastaus = vastaukset["aukiolo"]

    else:
        vastaus = (
            "Hmm… en ole varma miten vastata tähän 🤔\n"
            "Haluatko että annan asiakaspalvelun yhteystiedot?"
        )
        st.session_state.waiting_for_yes = True

    # Tallennetaan bottiviesti
    st.session_state.chat_history.append(("assistant", vastaus))


# --- CHATTINÄKYMÄ ---
for sender, msg in st.session_state.chat_history:
    st.chat_message(sender).write(msg)





