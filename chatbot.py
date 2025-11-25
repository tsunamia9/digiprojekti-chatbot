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

# --- Funktio vastauksen hakemiseen ---
def get_vastaus(kysymys: str) -> str:
    kysymys = kysymys.lower()

    # Ystävälliset vastaukset
    tervehdykset = ["hei", "moi", "terve", "hello", "päivää"]
    kiitokset = ["kiitos", "thx", "thanks", "kiitti"]
    kehumiset = ["hyvä", "kiva", "mahtava", "paras", "super"]
    myonteiset = ["joo", "kyllä", "ok", "selvä", "go", "jatka", "haluan", "kyllä kiitos"]

    # Perus- ja syvät vastaukset
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
        "alennukset": "Tarjoamme satunnaisia kampanjoita ja uutiskirjeen tilaajille alennuksia.",
        "alennukset_syva": (
            "Alennukset:\n"
            "- Uutiskirjeen tilaajat saavat kampanjakoodeja.\n"
            "- Sesonkialennukset ja tarjouskampanjat vaihtelevat.\n"
            "- Tarkista ajankohtaiset tarjoukset verkkosivuiltamme."
        ),
        "tilausseuranta": "Voit seurata tilaustasi sisäänkirjautumalla omalle tilillesi.",
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

    # --- Syvempi vastaus jos käyttäjä vastaa myönteisesti ---
    if st.session_state.last_topic and any(word in kysymys for word in myonteiset):
        if st.session_state.last_topic == "palautus":
            return vastaukset["palautus_syva"]
        if st.session_state.last_topic == "toimitus":
            return vastaukset["toimitus_syva"]
        if st.session_state.last_topic == "maksutavat":
            return vastaukset["maksutavat_syva"]
        if st.session_state.last_topic == "alennukset":
            return vastaukset["alennukset_syva"]
        if st.session_state.last_topic == "tilausseuranta":
            return vastaukset["tilausseuranta_syva"]
        if st.session_state.last_topic == "vaihto":
            return vastaukset["vaihto_syva"]

    # --- Ystävälliset vastaukset ---
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

    # --- Pehmeä avainsanahaku ja konteksti ---
    if "palaut" in kysymys:
        st.session_state.last_topic = "palautus"
        return "Voit palauttaa tuotteet 30 päivän sisällä ostopäivästä. Haluatko tietää, miten palautus tehdään käytännössä?"
    if "toimit" in kysymys or "kuljet" in kysymys or "paket" in kysymys:
        st.session_state.last_topic = "toimitus"
        return "Toimitamme tuotteet 2–5 arkipäivässä. Haluatko tietää, miten toimitusta voi seurata?"
    if "auki" in kysymys or "ajat" in kysymys:
        st.session_state.last_topic = None
        return vastaukset["aukiolo"]
    if "maksu" in kysymys or "kortti" in kysymys or "paypal" in kysymys or "klarna" in kysymys:
        st.session_state.last_topic = "maksutavat"
        return "Hyväksymme Visa, Mastercard, PayPal ja Klarna. Haluatko tietää maksamisen tarkemmat ohjeet?"
    if "alenn" in kysymys or "kampanja" in kysymys:
        st.session_state.last_topic = "alennukset"
        return "Tarjoamme kampanjoita ja alennuksia. Haluatko tietää lisää alennusten käytöstä?"
    if "tilausseuranta" in kysymys or "seuranta" in kysymys:
        st.session_state.last_topic = "tilausseuranta"
        return "Voit seurata tilaustasi tililläsi. Haluatko ohjeet tilauksen seurantaan?"
    if "vaihto" in kysymys or "vaihda" in kysymys:
        st.session_state.last_topic = "vaihto"
        return "Voit vaihtaa tuotteita 30 päivän sisällä. Haluatko tietää tarkemmat vaihto-ohjeet?"
    if "lahjakortti" in kysymys or "lahja" in kysymys:
        st.session_state.last_topic = None
        return vastaukset["lahjakortti"]
    if "tuki" in kysymys or "yhteys" in kysymys:
        st.session_state.last_topic = None
        return vastaukset["tuki"]

    # --- Fallback ---
    st.session_state.last_topic = None
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
    st.session_state.last_topic = None

# --- Logiikka vastauksen hakemiseen ---
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    vastaus = get_vastaus(user_input)
    st.session_state.chat_history.append(("assistant", vastaus))

# --- Chat-historia ---
for sender, msg in st.session_state.chat_history[-50:]:
    st.chat_message(sender).write(msg)







