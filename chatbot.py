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
if user_input:
    kysymys = user_input.lower().strip()
    st.session_state.chat_history.append(("user", user_input))

    # Jos botti odottaa vastausta kyllä/ei asiakaspalveluun
    if st.session_state.odottaa_aspa_vastausta:
        if any(word in kysymys for word in ["kyllä", "joo", "yes", "ok"]):
            vastaus = asiakaspalvelu_tiedot
        else:
            vastaus = "Selvä! Voit kysyä minulta lisää, jos tarvitset apua."
        st.session_state.odottaa_aspa_vastausta = False
        st.session_state.chat_history.append(("assistant", vastaus))

    else:
        # Lopetus
        if kysymys == "lopeta":
            vastaus = "Näkemiin! Toivottavasti olin avuksi."

        # Näytä tuotteet, mutta vain selkeissä pyynnöissä
        elif kysymys.startswith("tuotteet") or ("näytä" in kysymys and "tuotteet" in kysymys):
            lista = "\n".join([f"- {t['nimi']} ({t['kategoria']})" for t in tuotteet])
            vastaus = f"Tässä tuotteet:\n{lista}"

        # Avainsanahaku palautus
        elif "palaut" in kysymys:
            vastaus = vastaukset["palautus"]

        # Avainsanahaku toimitus
        elif "toimit" in kysymys or "kuljet" in kysymys or "paket" in kysymys:
            vastaus = vastaukset["toimitus"]

        # Avainsanahaku aukiolo
        elif "auki" in kysymys or "ajat" in kysymys:
            vastaus = vastaukset["aukiolo"]

        else:
            # Epäselvä kysymys → ehdota asiakaspalvelua
            vastaus = (
                "En valitettavasti tiedä vastausta tähän. "
                "Haluatko, että annan asiakaspalvelun yhteystiedot?"
            )
            st.session_state.odottaa_aspa_vastausta = True

        st.session_state.chat_history.append(("assistant", vastaus))


# --- CHATTINÄKYMÄ ---
for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)





