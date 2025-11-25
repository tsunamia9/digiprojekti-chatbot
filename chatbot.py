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
if "awaiting_followup" not in st.session_state:
    st.session_state.awaiting_followup = False  # uusi jatkokysymys-tila

# --- Vastaukset ja FAQ ---
positive_replies = ["joo", "kyllä", "ok", "selvä", "go", "jatka", "kyllä kiitos"]
negative_replies = ["ei", "en", "en oikein", "en halua"]

# --- Yleiset FAQ-vastaukset ja lisätiedot ---
general_faq = {
    "palautus": {
        "basic": "Palautus onnistuu 30 päivän sisällä ostopäivästä. Täytä palautuslomake tililläsi, pakkaa tuote ja lähetä takaisin.",
        "extra": "Varmista, että tuotteen pakkaus on ehjä ja liitä mukaan kuitti. Tarvittaessa ota yhteyttä asiakaspalveluun, jos palautus ei onnistu."
    },
    "vaihto": {
        "basic": "Voit vaihtaa tuotteen 30 päivän sisällä ostopäivästä. Täytä vaihtolomake ja lähetä vanha tuote takaisin.",
        "extra": "Jos haluat vaihtaa eri kokoisen tuotteen, muista merkitä uusi koko lomakkeeseen. Express-vaihto onnistuu lisämaksusta."
    },
    "toimituskulut": {
        "basic": "Toimituskulut määräytyvät tilauksen koon ja toimitustavan mukaan. Perustoimitus Suomessa on 4,90€.",
        "extra": "Jos tilaat useamman tuotteen, saatamme yhdistää toimitukset. Express-toimitus on mahdollinen lisämaksusta."
    },
    "toimitusaika": {
        "basic": "Toimitusaika Suomessa on yleensä 2–5 arkipäivää tilauksen vahvistamisesta.",
        "extra": "Viivästyksen sattuessa saat seurantakoodilla tarkemmat tiedot toimituksesta."
    },
    "seurantalinkki": {
        "basic": "Voit seurata pakettisi sijaintia saamallasi seurantakoodilla verkkosivullamme.",
        "extra": "Seurantakoodi löytyy tilausvahvistussähköpostista tai tilisi 'Omat tilaukset' -osiosta."
    },
    "maksutavat": {
        "basic": "Hyväksymme maksutavat: kortti, PayPal ja Klarna. Maksu on turvallinen ja varmennettu.",
        "extra": "Korttimaksussa veloitetaan heti, Klarna mahdollistaa eräpäivän, PayPal tarjoaa lisäturvaa."
    },
    "kampanjat": {
        "basic": "Seuraa uutiskirjettä ja some-kanavia ajankohtaisista kampanjoista ja erikoistarjouksista.",
        "extra": "Uutiskirjeen tilaajat saavat usein lisäkampanjoita ja alennuskoodeja."
    },
    "varasto": {
        "basic": "Voit tarkistaa tuotteen saatavuuden tuotesivulta. Päivitämme varastosaldon reaaliajassa.",
        "extra": "Jos tuote on loppu, voit tilata ilmoituksen, kun se tulee varastoon."
    },
    "takuuaika": {
        "basic": "Tuotteilla on 12 kuukauden takuu ostopäivästä.",
        "extra": "Joissakin tuotteissa takuu voi olla pidempi; tarkista tuotesivulta."
    },
    "tilauksen_muokkaus": {
        "basic": "Voit muokata tilaustasi 1–2 tunnin sisällä sen tekemisestä.",
        "extra": "Jos tilaus on jo lähetetty, ota yhteyttä asiakaspalveluun peruutusta varten."
    },
    "alennuskoodi": {
        "basic": "Syötä alennuskoodi kassalla kenttään 'Koodin syöttö'. Varmista, että koodi on voimassa.",
        "extra": "Jos koodi ei toimi, tarkista voimassaoloaika ja kampanjan ehdot."
    },
    "kirjautuminen": {
        "basic": "Jos et pääse kirjautumaan, tarkista sähköposti ja salasana.",
        "extra": "Voit myös käyttää 'Unohditko salasanasi?' -linkkiä tai palauttaa salasanan."
    },
    "kansainvälinen_toimitus": {
        "basic": "Toimitamme EU-maihin ja muualle maailmaan. Toimituskulut ja -ajat vaihtelevat maittain.",
        "extra": "Tarkista kansainvälisen toimituksen hinnat ja tullimaksut tilauksen yhteydessä."
    },
    "tuotetiedot": {
        "basic": "Tuotesivuilla on saatavilla materiaalit, koot, värit ja yhteensopivuusohjeet.",
        "extra": "Jos tarvitset lisätietoja, ota yhteyttä asiakaspalveluun."
    },
    "tilausvahvistus": {
        "basic": "Saat tilausvahvistuksen ja laskun sähköpostiisi heti tilauksen jälkeen.",
        "extra": "Jos et saanut sähköpostia, tarkista roskapostikansio tai ota yhteyttä asiakaspalveluun."
    },
    "lahjakortti": {
        "basic": "Tarjoamme lahjakortteja, jotka ovat voimassa 12 kuukautta ostopäivästä.",
        "extra": "Lahjakortti voidaan käyttää useammassa ostoksessa kunnes arvo on käytetty."
    },
    "asiakaspalvelu": {
        "basic": "Asiakaspalvelumme tavoitat:\n- 📞 09 123 4567\n- 📧 support@verkkokauppa.fi\n- ⏰ ma–pe 9–17",
        "extra": "Voit myös kysyä chatbotilta ohjeita useisiin aiheisiin."
    }
}

# --- FAQ-avainsanat ---
faq_keywords = {
    "palaut": "palautus",
    "palauta": "palautus",
    "toimit": "toimituskulut",
    "kuljet": "toimituskulut",
    "paket": "toimituskulut",
    "toimitusaika": "toimitusaika",
    "seuranta": "seurantalinkki",
    "maksu": "maksutavat",
    "kortti": "maksutavat",
    "paypal": "maksutavat",
    "klarna": "maksutavat",
    "alenn": "kampanjat",
    "kampanj": "kampanjat",
    "kampanjo": "kampanjat",
    "tarjou": "kampanjat",
    "tilausseuranta": "seurantalinkki",
    "vaihto": "vaihto",
    "vaihda": "vaihto",
    "lahja": "lahjakortti",
    "lahjakortti": "lahjakortti",
    "asiakas": "asiakaspalvelu",
    "tuki": "asiakaspalvelu",
    "yhteys": "asiakaspalvelu",
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

# --- Funktio vastauksen hakemiseen ---
def get_vastaus(kysymys: str) -> str:
    kysymys = kysymys.lower()

    # --- Lopetus ---
    if "lopeta" in kysymys or "näkemiin" in kysymys or "kuulemiin" in kysymys:
        st.session_state.awaiting_confirmation = False
        st.session_state.awaiting_followup = False
        st.session_state.last_topic = None
        return "Näkemiin! 👋 Toivottavasti olin avuksi. Mukavaa päivänjatkoa! 😊"

    # --- Jos odotetaan jatkokysymystä ---
    if st.session_state.awaiting_followup and st.session_state.last_topic:
        positive = any(word in kysymys for word in positive_replies)
        negative = any(word in kysymys for word in negative_replies)
        topic = st.session_state.last_topic
        if negative:
            return general_faq[topic]["extra"] + "\n\nHaluatko vielä lisätietoa tästä aiheesta? 😊"
        elif positive:
            st.session_state.awaiting_followup = False
            st.session_state.last_topic = None
            return "Hienoa! 😄 Oli ilo auttaa sinua!"
        else:
            # jos käyttäjä kirjoittaa jotain muuta, annetaan extra-info
            return general_faq[topic]["extra"] + "\n\nHaluatko vielä lisätietoa tästä aiheesta? 😊"

    # --- Jos odotetaan vahvistusta ---
    if st.session_state.awaiting_confirmation and st.session_state.last_topic:
        positive = any(word in kysymys for word in positive_replies)
        negative = any(word in kysymys for word in negative_replies)
        topic = st.session_state.last_topic
        if positive:
            st.session_state.awaiting_confirmation = False
            st.session_state.awaiting_followup = False
            st.session_state.last_topic = None
            return "Hienoa! 😄 Oli ilo auttaa sinua!"
        elif negative:
            st.session_state.awaiting_confirmation = False
            st.session_state.awaiting_followup = True
            return general_faq[topic]["extra"] + "\n\nHaluatko vielä lisätietoa tästä aiheesta? 😊"

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
            "Hieno juttu! 😄 Oli ilo auttaa.",
            "Ei kestä! 😊",
            "Aina ilo auttaa!"
        ])
    if any(sana in kysymys for sana in kehumiset):
        return "Kiitos! 😄 Teen parhaani auttaakseni."

    # --- Tuotelistaus ---
    if "tuotteet" in kysymys or ("näytä" in kysymys and "tuotte" in kysymys):
        lista = "\n".join(
            [f"- {t['nimi']} ({t['kategoria']}) – {t.get('hinta','Hinta ei saatavilla')}€" for t in tuotteet]
        )
        return f"Tässä meidän tuotteet:\n{lista}"

    # --- FAQ-avainsanat ---
    for key, topic in faq_keywords.items():
        if key in kysymys:
            st.session_state.last_topic = topic
            st.session_state.awaiting_confirmation = True
            return general_faq[topic]["basic"] + "\n\nAuttoiko tämä sinua? 😊"

    # --- Fallback käyttäjälle ---
    st.session_state.last_topic = "tuki_kysymys"
    st.session_state.awaiting_confirmation = True
    return (
        "Hmm… en ole varma mitä tarkoitit 🤔\n"
        "Jos olet epävarma, voit klikata 'Näytä kaikki aiheet', jolloin näet kaiken mitä botti pystyy käsittelemään."
    )

# --- Chat-container ---
chat_container = st.empty()

# --- Syöttökenttä formissa ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Kirjoita viesti:", "")
    submit_button = st.form_submit_button("Lähetä")

# --- Näytä kaikki aiheet -nappi ---
if st.button("Näytä kaikki aiheet"):
    kaikki_aiheet = "\n".join(f"- {topic.replace('_',' ')}" for topic in general_faq.keys())
    st.session_state.chat_history.append(("assistant", f"Tässä kaikki aiheet, joihin botti pystyy vastaamaan:\n{kaikki_aiheet}"))

# --- Tyhjennä keskustelu ---
if st.button("Tyhjennä keskustelu"):
    st.session_state.chat_history = []
    st.session_state.last_topic = None
    st.session_state.awaiting_confirmation = False
    st.session_state.awaiting_followup = False

# --- Logiikka vastauksen hakemiseen ---
if submit_button and user_input:
    st.session_state.chat_history.append(("user", user_input))
    vastaus = get_vastaus(user_input)
    st.session_state.chat_history.append(("assistant", vastaus))

# --- Chat-historia ---
with chat_container.container():
    for sender, msg in st.session_state.chat_history[-50:]:
        st.chat_message(sender).write(msg)







