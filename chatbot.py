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
    st.session_state.awaiting_confirmation = False

# --- Vastaukset ---
positive_replies = ["joo", "kyllä", "ok", "selvä", "go", "jatka", "kyllä kiitos"]
negative_replies = ["ei", "en", "en oikein", "en halua"]

# --- Yleisesti kysytyt kysymykset ja vastaukset ---
general_faq = {
    "toimituskulut": "Toimituskulut määräytyvät tilauksen koon ja toimitustavan mukaan. Perustoimitus Suomessa on 4,90€.",
    "toimitusaika": "Toimitusaika Suomessa on yleensä 2–5 arkipäivää tilauksen vahvistamisesta.",
    "seurantalinkki": "Voit seurata pakettisi sijaintia saamallasi seurantakoodilla verkkosivullamme.",
    "palautus": "Palautus onnistuu 30 päivän sisällä ostopäivästä. Täytä palautuslomake tililläsi, pakkaa tuote ja lähetä takaisin.",
    "vaihto": "Voit vaihtaa tuotteen 30 päivän sisällä ostopäivästä. Täytä vaihtolomake ja lähetä vanha tuote takaisin.",
    "lahjakortti": "Tarjoamme lahjakortteja, jotka ovat voimassa 12 kuukautta ostopäivästä.",
    "asiakaspalvelu": "Asiakaspalvelumme tavoitat:\n- 📞 09 123 4567\n- 📧 support@verkkokauppa.fi\n- ⏰ ma–pe 9–17",
    "kampanjat": "Seuraa uutiskirjettä ja some-kanavia ajankohtaisista kampanjoista ja erikoistarjouksista.",
    "varasto": "Voit tarkistaa tuotteen saatavuuden tuotesivulta. Päivitämme varastosaldon reaaliajassa.",
    "maksutavat": "Hyväksymme maksutavat: kortti, PayPal ja Klarna. Maksu on turvallinen ja varmennettu.",
    "takuuaika": "Tuotteilla on 12 kuukauden takuu ostopäivästä, ellei tuotekohtaisesti toisin mainita.",
    "tilauksen_muokkaus": "Voit muokata tilaustasi 1–2 tunnin sisällä sen tekemisestä. Ota tarvittaessa yhteyttä asiakaspalveluun.",
    "alennuskoodi": "Syötä alennuskoodi kassalla kenttään 'Koodin syöttö'. Varmista, että koodi on voimassa.",
    "kirjautuminen": "Jos et pääse kirjautumaan, tarkista sähköposti ja salasana. Voit myös käyttää 'Unohditko salasanasi?' -linkkiä.",
    "kansainvälinen_toimitus": "Toimitamme EU-maihin ja muualle maailmaan. Toimituskulut ja -ajat vaihtelevat maittain.",
    "tuotetiedot": "Tuotesivuilla on saatavilla materiaalit, koot, värit ja yhteensopivuusohjeet.",
    "tilausvahvistus": "Saat tilausvahvistuksen ja laskun sähköpostiisi heti tilauksen jälkeen."
}

# --- Funktio vastauksen hakemiseen ---
def get_vastaus(kysymys: str) -> str:
    kysymys = kysymys.lower()

    # --- Jos käyttäjä kirjoittaa uuden kysymyksen kesken vahvistuksen ---
    if st.session_state.awaiting_confirmation:
        if not any(word in kysymys for word in positive_replies + negative_replies):
            st.session_state.awaiting_confirmation = False
            st.session_state.last_topic = None

    # --- Jos odotetaan vahvistusta ---
    if st.session_state.awaiting_confirmation:
        topic = st.session_state.last_topic
        positive = any(word in kysymys for word in positive_replies)
        negative = any(word in kysymys for word in negative_replies)

        predefined_topics = ["palautus","toimitus","maksutavat","alennukset","tilausseuranta","vaihto"]
        if topic in predefined_topics:
            if positive:
                st.session_state.awaiting_confirmation = False
                st.session_state.last_topic = None
                return {
                    "palautus": "Hienoa! 😊 Ilo kuulla, että pystyin auttamaan palautuksessa!",
                    "toimitus": "Mahtavaa! 😄 Kiva että toimitusohjeet auttoivat!",
                    "maksutavat": "Hienoa! 😊 Maksutavat selkeät?",
                    "alennukset": "Mahtavaa! 😄 Tässä lisää tietoa kampanjoista:\n- Erikoistarjoukset voimassa rajoitetun ajan\n- Käytä kampanjakoodeja kassalla\n- Seuraa uutiskirjettä ja some-kanavia lisätarjouksista",
                    "tilausseuranta": "Hienoa! 😊 Nyt voit seurata tilaustasi helposti tililläsi.",
                    "vaihto": "Mahtavaa! 😄 Vaihto onnistui näin helposti!"
                }.get(topic, "Hups! Tapahtui virhe, yritä uudelleen.")
            elif negative:
                st.session_state.awaiting_confirmation = False
                st.session_state.last_topic = None
                return (
                    "Voi ei! Voit olla suoraan yhteydessä asiakaspalveluumme, jotta saat tarkempaa apua:\n"
                    "- 📞 Puhelin: 09 123 4567\n"
                    "- 📧 Sähköposti: support@verkkokauppa.fi\n"
                    "- ⏰ Aukiolo: ma–pe 9–17"
                )
        elif topic == "tuki_kysymys":
            st.session_state.awaiting_confirmation = False
            st.session_state.last_topic = None
            return general_faq["asiakaspalvelu"]

    # --- Ystävälliset vastaukset ---
    tervehdykset = ["miten menee", "haloo", "moro", "hei", "moi", "terve", "hello", "päivää"]
    kiitokset = ["kiitos", "thx", "thanks", "kiitti"]
    kehumiset = ["hienoa", "hyvä", "kiva", "mahtava", "paras", "super"]

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

    # --- FAQ-avainsanat ---
    faq_keywords = {
        "palaut": "palautus",
        "palauta": "palautus",
        "toimit": "toimituskulut",
        "kuljet": "toimituskulut",
        "paket": "toimituskulut",
        "maksu": "maksutavat",
        "kortti": "maksutavat",
        "paypal": "maksutavat",
        "klarna": "maksutavat",
        "alenn": "kampanjat",
        "kampanj": "kampanjat",
        "kampanjo": "kampanjat",
        "tarjou": "kampanjat",
        "tilausseuranta": "seurantalinkki",
        "seuranta": "seurantalinkki",
        "vaihto": "vaihto",
        "vaihda": "vaihto",
        "lahja": "lahjakortti",
        "lahjakortti": "lahjakortti",
        "asiakas": "asiakaspalvelu",
        "tuki": "asiakaspalvelu",
        "yhteys": "asiakaspalvelu",
        "toimitusaika": "toimitusaika",
        "taku": "takuuaika",
        "muokkaus": "tilauksen_muokkaus",
        "peruuta": "tilauksen_muokkaus",
        "koodi": "alennuskoodi",
        "kirjaudu": "kirjautuminen",
        "valuutta": "kansainvälinen_toimitus",
        "tuotetiedot": "tuotetiedot",
        "lasku": "tilausvahvistus",
        "kuitti": "tilausvahvistus"
    }

    for key, topic in faq_keywords.items():
        if key in kysymys:
            st.session_state.last_topic = topic
            st.session_state.awaiting_confirmation = True
            return general_faq.get(topic, "Valitettavasti en löytänyt tietoa tästä aiheesta.") + "\n\nAuttoiko tämä sinua? 😊"

    # --- Fallback ---
    st.session_state.last_topic = "tuki_kysymys"
    st.session_state.awaiting_confirmation = True
    return (
        "Hmm… en ole varma mitä tarkoitit 🤔\n"
        "Ehkä haluat tietoa jostakin seuraavista:\n"
        "- Palautus- ja vaihto-ohjeet\n"
        "- Toimituskulut ja toimitusaika\n"
        "- Maksutavat\n"
        "- Alennukset ja kampanjat\n"
        "- Tilausseuranta\n"
        "- Aukioloajat\n"
        "- Lahjakortit\n"
        "- Asiakaspalvelu\n"
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






