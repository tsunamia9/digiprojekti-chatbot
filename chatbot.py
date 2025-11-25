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

# --- Vastaukset ---
positive_replies = ["joo", "kyllä", "ok", "selvä", "go", "jatka", "kyllä kiitos"]
negative_replies = ["ei", "en", "en oikein", "en halua"]

def get_vastaus(kysymys: str) -> str:
    kysymys = kysymys.lower()

    # --- Jos käyttäjä kirjoittaa uuden kysymyksen kesken vahvistuksen, aloitetaan alusta ---
    if st.session_state.awaiting_confirmation:
        if not any(word in kysymys for word in positive_replies + negative_replies):
            st.session_state.awaiting_confirmation = False
            st.session_state.last_topic = None

    # --- Jos odotetaan vahvistusta ---
    if st.session_state.awaiting_confirmation:
        if st.session_state.last_topic in ["palautus","toimitus","maksutavat","alennukset","tilausseuranta","vaihto"]:
            if any(word in kysymys for word in positive_replies):
                st.session_state.awaiting_confirmation = False
                st.session_state.last_topic = None
                return {
                    "palautus": "Hienoa! 😊 Ilo kuulla, että pystyin auttamaan palautuksessa!",
                    "toimitus": "Mahtavaa! 😄 Kiva että toimitusohjeet auttoivat!",
                    "maksutavat": "Hienoa! 😊 Maksutavat selkeät?",
                    "alennukset": "Mahtavaa! 😄 Tässä lisää tietoa kampanjoista:\n- Erikoistarjoukset voimassa rajoitetun ajan\n- Käytä kampanjakoodeja kassalla\n- Seuraa uutiskirjettä ja some-kanavia lisätarjouksista",
                    "tilausseuranta": "Hienoa! 😊 Nyt voit seurata tilaustasi helposti tililläsi.",
                    "vaihto": "Mahtavaa! 😄 Vaihto onnistui näin helposti!"
                }[st.session_state.last_topic]
            elif any(word in kysymys for word in negative_replies):
                st.session_state.awaiting_confirmation = False
                st.session_state.last_topic = None
                return (
                    "Voi ei! Voit olla suoraan yhteydessä asiakaspalveluumme, jotta saat tarkempaa apua:\n"
                    "- 📞 Puhelin: 09 123 4567\n"
                    "- 📧 Sähköposti: support@verkkokauppa.fi\n"
                    "- ⏰ Aukiolo: ma–pe 9–17"
                )
        elif st.session_state.last_topic == "tuki_kysymys":
            if any(word in kysymys for word in positive_replies):
                st.session_state.awaiting_confirmation = False
                st.session_state.last_topic = None
                return (
                    "Tässä asiakaspalvelumme tiedot:\n"
                    "- 📞 Puhelin: 09 123 4567\n"
                    "- 📧 Sähköposti: support@verkkokauppa.fi\n"
                    "- ⏰ Aukiolo: ma–pe 9–17"
                )
            elif any(word in kysymys for word in negative_replies):
                st.session_state.awaiting_confirmation = False
                st.session_state.last_topic = None
                return "Selvä! 😊 Jos tarvitset apua myöhemmin, kysy vain."

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
        return "Kiitos! 😄 Teen parhaani auttaakseni."

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
        "palautus_syva": (
            "Palautus tapahtuu näin:\n"
            "1. Täytä palautuslomake tililläsi.\n"
            "2. Pakkaa tuote alkuperäiseen pakkaukseen.\n"
            "3. Lähetä paketti takaisin osoitteeseen, joka löytyy palautuslomakkeesta.\n"
            "4. Kun palautus on vastaanotettu, rahat palautetaan alkuperäiselle maksutavalle."
        ),
        "toimitus_syva": (
            "Toimituksen voit seurata näin:\n"
            "1. Saat seurantakoodin sähköpostilla.\n"
            "2. Pakkaukset toimitetaan valitulla kuljetustavalla.\n"
            "3. Jos toimitus viivästyy, ota yhteyttä asiakaspalveluun."
        ),
        "maksutavat_syva": (
            "Maksaminen tapahtuu näin:\n"
            "1. Valitse maksutapa kassalla.\n"
            "2. Syötä korttitiedot tai kirjaudu PayPaliin.\n"
            "3. Maksu on turvallinen ja varmennettu.\n"
            "4. Saat vahvistuksen sähköpostiisi."
        ),
        "alennukset_syva": (
            "Alennukset ja kampanjat:\n"
            "- Uutiskirjeen tilaajat saavat kampanjakoodeja.\n"
            "- Sesonkialennukset ja tarjouskampanjat vaihtelevat.\n"
            "- Tarkista ajankohtaiset tarjoukset verkkosivuiltamme."
        ),
        "tilausseuranta_syva": (
            "Tilausseuranta:\n"
            "1. Kirjaudu tilillesi.\n"
            "2. Valitse 'Omat tilaukset'.\n"
            "3. Näet tilausten tilan ja seurantakoodit.\n"
            "4. Saat myös ilmoituksia sähköpostiisi."
        ),
        "vaihto_syva": (
            "Vaihto tapahtuu näin:\n"
            "1. Täytä vaihtolomake tililläsi.\n"
            "2. Pakkaa tuote alkuperäiseen pakkaukseen.\n"
            "3. Lähetä paketti vaihtoon.\n"
            "4. Saat uuden tuotteen, kun vanha on vastaanotettu."
        ),
        "säännöt_syva": (
            "Verkkokaupan säännöt:\n"
            "- Tuotteiden palautus ja vaihto 30 päivän sisällä.\n"
            "- Asiakastuki ma–pe 9–17.\n"
            "- Maksutavat: kortti, PayPal, Klarna.\n"
            "- Tarjoukset ja alennukset vaihtelevat sesongin mukaan."
        ),
        "tuki_syva": (
            "Tässä asiakaspalvelumme tiedot:\n"
            "- 📞 Puhelin: 09 123 4567\n"
            "- 📧 Sähköposti: support@verkkokauppa.fi\n"
            "- ⏰ Aukiolo: ma–pe 9–17"
        )
    }

    # --- Pehmeä avainsanahaku ja syvä vastaus ---
    if any(word in kysymys for word in ["palaut", "palauta", "palautus"]):
        st.session_state.last_topic = "palautus"
        st.session_state.awaiting_confirmation = True
        return vastaukset["palautus_syva"] + "\n\nAuttoiko tämä sinua? 😊"

    if any(word in kysymys for word in ["toimit", "kuljet", "paket"]):
        st.session_state.last_topic = "toimitus"
        st.session_state.awaiting_confirmation = True
        return vastaukset["toimitus_syva"] + "\n\nAuttoiko tämä sinua? 😊"

    if any(word in kysymys for word in ["maksu", "kortti", "paypal", "klarna"]):
        st.session_state.last_topic = "maksutavat"
        st.session_state.awaiting_confirmation = True
        return vastaukset["maksutavat_syva"] + "\n\nAuttoiko tämä sinua? 😊"

    if any(word in kysymys for word in ["alenn", "kampanj", "kampanjo", "tarjou"]):
        st.session_state.last_topic = "alennukset"
        st.session_state.awaiting_confirmation = True
        return vastaukset["alennukset_syva"] + "\n\nHaluatko tietää vielä enemmän alennuksista ja kampanjoista? 😊"

    if any(word in kysymys for word in ["tilausseuranta", "seuranta"]):
        st.session_state.last_topic = "tilausseuranta"
        st.session_state.awaiting_confirmation = True
        return vastaukset["tilausseuranta_syva"] + "\n\nAuttoiko tämä sinua? 😊"

    if any(word in kysymys for word in ["vaihto", "vaihda"]):
        st.session_state.last_topic = "vaihto"
        st.session_state.awaiting_confirmation = True
        return vastaukset["vaihto_syva"] + "\n\nAuttoiko tämä sinua? 😊"

    if any(word in kysymys for word in ["säännöt", "ehdot", "käytännöt"]):
        st.session_state.last_topic = "säännöt"
        st.session_state.awaiting_confirmation = False
        return vastaukset["säännöt_syva"]

    # --- Yksinkertaiset vastaukset ---
    if "auki" in kysymys or "ajat" in kysymys:
        return "Asiakaspalvelumme on auki ma–pe klo 9–17."
    if "lahjakortti" in kysymys or "lahja" in kysymys:
        return "Tarjoamme lahjakortteja, jotka ovat voimassa 12 kuukautta ostopäivästä."
    if "tuki" in kysymys or "yhteys" in kysymys:
        st.session_state.last_topic = None
        st.session_state.awaiting_confirmation = False
        return vastaukset["tuki_syva"]

    # --- Fallback ---
    st.session_state.last_topic = "tuki_kysymys"
    st.session_state.awaiting_confirmation = True
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
        "- Asiakastuki\n"
        "\nHaluatko, että annan asiakaspalvelun yhteystiedot? 😊"
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








