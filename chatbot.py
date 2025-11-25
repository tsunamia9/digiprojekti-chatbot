import streamlit as st
import os
import json
import random

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

# --- Tallennetaan keskustelu ja viimeinen aihe ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_topic" not in st.session_state:
    st.session_state.last_topic = None
if "awaiting_confirmation" not in st.session_state:
    st.session_state.awaiting_confirmation = False  # odottaa käyttäjän vastausta "Auttoiko tämä?"

# --- Vastauslogiikka ---
positive_replies = ["joo", "kyllä", "ok", "selvä", "go", "jatka", "kyllä kiitos"]
negative_replies = ["ei", "en", "en oikein", "en halua"]

def get_vastaus(kysymys: str) -> str:
    kysymys = kysymys.lower()
    
    # --- Odotetaan vahvistusta ---
    if st.session_state.awaiting_confirmation:
        if any(word in kysymys for word in positive_replies):
            st.session_state.awaiting_confirmation = False
            st.session_state.last_topic = None
            return random.choice([
                "Hienoa! 😊 Ilo kuulla, että pystyin auttamaan!",
                "Mahtavaa! 😄 Kiva että ohje auttoi!"
            ])
        elif any(word in kysymys for word in negative_replies):
            st.session_state.awaiting_confirmation = False
            st.session_state.last_topic = None
            return (
                "Voi ei 😅 Yritetään uudelleen:\n"
                "Voit myös ottaa yhteyttä asiakaspalveluumme support@verkkokauppa.fi, "
                "jos tarvitset tarkempaa apua."
            )

    # --- Ystävälliset vastaukset ---
    tervehdykset = ["hei", "moi", "terve", "hello", "päivää"]
    kiitokset = ["kiitos", "thx", "thanks", "kiitti"]
    kehumiset = ["hyvä", "kiva", "mahtava", "paras", "super"]

    if any(sana in kysymys for sana in tervehdykset):
        return random.choice([
            "Hei! 😊 Miten voin auttaa sinua tänään?",
            "Moi! Miten voin olla avuksi?",
            "Terve! 😊 Mitä haluaisit tietää?"
        ])
    if any(sana in kysymys for sana in kiitokset):
        return random.choice([
            "Ole hyvä! 💙 Kiva että pystyin auttamaan.",
            "Ei kestä! 😊",
            "Aina ilo auttaa!"
        ])
    if any(sana in kysymys for sana in kehumiset):
        return "Aww kiitos! 😄 Teen parhaani auttaakseni."

    # --- Lopetus ---
    if "lopeta" in kysymys:
        return "Näkemiin! Toivottavasti olin avuksi 😊"

    # --- Tuotelistaus ---
    if "tuotteet" in kysymys or ("näytä" in kysymys and "tuotte" in kysymys):
        lista = "\n".join(
            [f"- {t['nimi']} ({t['kategoria']}) – {t.get('hinta', 'Hinta ei saatavilla')}€" for t in tuotteet]
        )
        return f"Tässä meidän tuotteet:\n{lista}"

    # --- Syvät vastaukset ---
    vastaukset = {
        "palautus": "Voit palauttaa tuotteet 30 päivän sisällä ostopäivästä.",
        "palautus_syva": (
            "Palautus tapahtuu näin:\n"
            "1. Täytä palautuslomake tililläsi.\n"
            "2. Pakkaa tuote alkuperäiseen pakkaukseen.\n"
            "3. Lähetä paketti takaisin osoitteeseen, joka löytyy palautuslomakkeesta.\n"
            "4. Kun palautus on vastaanotettu, rahat palautetaan alkuperäiselle maksutavalle."
        ),
        "toimitus": "Toimitamme tuotteet 2–5 arkipäivässä.",
        "toimitus_syva": (
            "Toimituksen voit seurata näin:\n"
            "1. Saat seurantakoodin sähköpostilla.\n"
            "2. Pakkaukset toimitetaan valitulla kuljetustavalla.\n"
            "3. Jos toimitus viivästyy, ota yhteyttä asiakaspalveluun."
        ),
        "aukiolo": "Asiakaspalvelumme on auki ma–pe klo 9–17.",
        "maksutavat": "Hyväksymme Visa, Mastercard, PayPal ja Klarna-maksut.",
        "maksutavat_syva": (
            "Maksaminen tapahtuu näin:\n"
            "1. Valitse maksutapa kassalla.\n"
            "2. Syötä korttitiedot tai kirjaudu PayPaliin.\n"
            "3. Maksu on turvallinen ja varmennettu.\n"
            "4. Saat vahvistuksen sähköpostiisi."
        ),
        "alennukset": "Tarjoamme kampanjoita ja alennuksia.",
        "alennukset_syva": (
            "Alennukset:\n"
            "- Uutiskirjeen tilaajat saavat kampanjakoodeja.\n"
            "- Sesonkialennukset ja tarjouskampanjat vaihtelevat.\n"
            "- Tarkista ajankohtaiset tarjoukset verkkosivuiltamme."
        ),
        "tilausseuranta": "Voit seurata tilaustasi tililläsi.",
        "tilausseuranta_syva": (
            "Tilausseuranta:\n"
            "1. Kirjaudu tilillesi.\n"
            "2. Valitse 'Omat tilaukset'.\n"
            "3. Näet tilausten tilan ja seurantakoodit.\n"
            "4. Saat myös ilmoituksia sähköpostiisi."
        ),
        "vaihto": "Voit vaihtaa tuotteita 30 päivän sisällä, kunhan ne ovat käyttämättömiä.",
        "vaihto_syva": (
            "Vaihto tapahtuu näin:\n"
            "1. Täytä vaihtolomake tililläsi.\n"
            "2. Pakkaa tuote alkuperäiseen pakkaukseen.\n"
            "3. Lähetä paketti vaihtoon.\n"
            "4. Saat uuden tuotteen, kun vanha on vastaanotettu."
        ),
        "lahjakortti": "Tarjoamme lahjakortteja, jotka ovat voimassa 12 kuukautta ostopäivästä.",
        "tuki": "Voit ottaa yhteyttä asiakaspalveluumme sähköpostitse support@verkkokauppa.fi."
    }

    # --- Pehmeä avainsanahaku ja syvä vastaus ---
    if "palaut" in kysymys:
        st.session_state.last_topic = "palautus"
        st.session_state.awaiting_confirmation = True
        return vastaukset["palautus_syva"] + "\n\nAuttoiko tämä sinua? 😊"
    if "toimit" in kysymys or "kuljet" in kysymys or "paket" in kysymys:
        st.session_state.last_topic = "toimitus"
        st.session_state.awaiting_confirmation = True
        return vastaukset["toimitus_syva"] + "\n\nAuttoiko tämä sinua? 😊"
    if "maksu" in kysymys or "kortti" in kysymys or "paypal" in kysymys or "klarna" in kysymys:
        st.session_state.last_topic = "maksutavat"
        st.session_state.awaiting_confirmation = True
        return vastaukset["maksutavat_syva"] + "\n\nAuttoiko tämä sinua? 😊"
    if "alenn" in kysymys or "kampanja" in kysymys:
        st.session_state.last_topic = "alennukset"
        st.session_state.awaiting_confirmation = True
        return vastaukset["alennukset_syva"] + "\n\nHaluatko tietää vielä enemmän alennuksista? 😊"
    if "tilausseuranta" in kysymys or "seuranta" in kysymys:
        st.session_state.last_topic = "tilausseuranta"
        st.session_state.awaiting_confirmation = True
        return vastaukset["tilausseuranta_syva"] + "\n\nAuttoiko tämä sinua? 😊"
    if "vaihto" in kysymys or "vaihda" in kysymys:
        st.session_state.last_topic = "vaihto"
        st.session_state.awaiting_confirmation = True
        return vastaukset["vaihto_syva"] + "\n\nAuttoiko tämä sinua? 😊"
    if "auki" in kysymys or "ajat" in kysymys:
        st.session_state.last_topic = None
        return vastaukset["aukiolo"]
    if "lahjakortti" in kysymys or "lahja" in kysymys:
        st.session_state.last_topic = None
        return vastaukset["lahjakortti"]
    if "tuki" in kysymys or "yhteys" in kysymys:
        st.session_state.last_topic = None
        return vastaukset["tuki"]

    # --- Fallback ---
    st.session_state.last_topic = None
    st.session_state.awaiting_confirmation = False
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

# --- Chat-container ---
chat_container = st.empty()

# --- Syöttökenttä formissa ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Kirjoita viesti:", "")
    submit_button = st.form_submit_button("Lähetä")

# --- Tyhjennä keskustelu ---
if st.button("Tyhjennä keskustelu"):
    st.session_state.chat_history = []
    st.session_state.last_topic = None
    st.session_state.awaiting_confirmation = False

# --- Logiikka vastauksen hakemiseen ---
if submit_button and user_input:
    st.session_state.chat_history.append(("user", user_input))
    vastaus = get_vastaus(user_input)
    st.session_state.chat_history.append(("assistant", vastaus))

# --- Chat-historia ---
with chat_container.container():
    for sender, msg in st.session_state.chat_history[-50:]:
        st.chat_message(sender).write(msg)








