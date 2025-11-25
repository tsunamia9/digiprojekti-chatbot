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

try:
    with open(file_path, "r", encoding="utf-8") as f:
        tuotteet = json.load(f)
except Exception as e:
    tuotteet = []
    print("Virhe ladattaessa tuotteita:", e)

st.title("Verkkokaupan Chatbot 🤖")
st.write("Hei! Olen verkkokaupan chatbot. Kuinka voin auttaa?")

# --- Tallennetaan keskustelu ja viimeinen aihe ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_topic" not in st.session_state:
    st.session_state.last_topic = None
if "awaiting_confirmation" not in st.session_state:
    st.session_state.awaiting_confirmation = False

# --- Vastaukset ja FAQ ---
positive_replies = ["joo", "kyllä", "ok", "selvä", "go", "jatka", "kyllä kiitos"]
negative_replies = ["ei", "en", "en oikein", "en halua"]

# --- Yleiset FAQ-vastaukset ---
general_faq = {
    "palautus": "Palautus onnistuu 30 päivän sisällä ostopäivästä. Täytä palautuslomake tililläsi, pakkaa tuote ja lähetä takaisin.",
    "palautus_lisä": "Varmista, että tuote on alkuperäisessä kunnossa ja kaikki lisävarusteet mukana. Tarvittaessa voit tulostaa palautuslomakkeen verkkosivuiltamme uudelleen.",
    "vaihto": "Voit vaihtaa tuotteen 30 päivän sisällä ostopäivästä. Täytä vaihtolomake ja lähetä vanha tuote takaisin.",
    "vaihto_lisä": "Huomioi, että uusi tuote lähetetään heti kun vanha tuote on vastaanotettu. Jos haluat nopeamman toimituksen, ota yhteys asiakaspalveluun.",
    "toimituskulut": "Toimituskulut määräytyvät tilauksen koon ja toimitustavan mukaan. Perustoimitus Suomessa on 4,90€.",
    "toimituskulut_lisä": "Jos tilaat useamman tuotteen, saatamme yhdistää toimitukset. Express-toimitus on mahdollinen lisämaksusta.",
    "toimitusaika": "Toimitusaika Suomessa on yleensä 2–5 arkipäivää tilauksen vahvistamisesta.",
    "toimitusaika_lisä": "Viivästyksen sattuessa saat seurantakoodilla tarkemmat tiedot toimituksesta.",
    "seurantalinkki": "Voit seurata pakettisi sijaintia saamallasi seurantakoodilla verkkosivullamme.",
    "maksutavat": "Hyväksymme maksutavat: kortti, PayPal ja Klarna. Maksu on turvallinen ja varmennettu.",
    "maksutavat_lisä": "Korttimaksu tapahtuu salatulla yhteydellä, PayPal ja Klarna varmistavat maksun turvallisuuden.",
    "kampanjat": "Seuraa uutiskirjettä ja some-kanavia ajankohtaisista kampanjoista ja erikoistarjouksista.",
    "kampanjat_lisä": "Lisäksi jotkut tuotteet sisältävät automaattisesti alennuksia kassalla. Tarkista tuotteen sivulta voimassa olevat kampanjat.",
    "varasto": "Voit tarkistaa tuotteen saatavuuden tuotesivulta. Päivitämme varastosaldon reaaliajassa.",
    "takuuaika": "Tuotteilla on 12 kuukauden takuu ostopäivästä, ellei tuotekohtaisesti toisin mainita.",
    "tilauksen_muokkaus": "Voit muokata tilaustasi 1–2 tunnin sisällä sen tekemisestä. Ota tarvittaessa yhteyttä asiakaspalveluun.",
    "tilauksen_muokkaus_lisä": "Muokkaus sisältää osoitteen, toimitustavan ja lisätilaukset. Tilauksen peruuttaminen onnistuu vain 2 tunnin sisällä.",
    "alennuskoodi": "Syötä alennuskoodi kassalla kenttään 'Koodin syöttö'. Varmista, että koodi on voimassa.",
    "alennuskoodi_lisä": "Jos koodi ei toimi, tarkista voimassaoloaika tai ota yhteyttä asiakaspalveluun.",
    "kirjautuminen": "Jos et pääse kirjautumaan, tarkista sähköposti ja salasana. Voit myös käyttää 'Unohditko salasanasi?' -linkkiä.",
    "kansainvälinen_toimitus": "Toimitamme EU-maihin ja muualle maailmaan. Toimituskulut ja -ajat vaihtelevat maittain.",
    "tuotetiedot": "Tuotesivuilla on saatavilla materiaalit, koot, värit ja yhteensopivuusohjeet.",
    "tilausvahvistus": "Saat tilausvahvistuksen ja laskun sähköpostiisi heti tilauksen jälkeen.",
    "lahjakortti": "Tarjoamme lahjakortteja, jotka ovat voimassa 12 kuukautta ostopäivästä.",
    "asiakaspalvelu": "Asiakaspalvelumme tavoitat:\n- 📞 09 123 4567\n- 📧 support@verkkokauppa.fi\n- ⏰ ma–pe 9–17"
}

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

def get_vastaus(kysymys: str) -> str:
    kysymys = kysymys.lower()

    # --- Lopetus ---
    if any(word in kysymys for word in ["lopeta", "näkemiin", "hei hei"]):
        st.session_state.awaiting_confirmation = False
        st.session_state.last_topic = None
        return "Näkemiin! 👋 Toivottavasti olin avuksi. Mukavaa päivänjatkoa! 😊"

    # --- Vahvistus ---
    if st.session_state.awaiting_confirmation:
        positive = any(word in kysymys for word in positive_replies)
        negative = any(word in kysymys for word in negative_replies)
        last_topic = st.session_state.last_topic
        st.session_state.awaiting_confirmation = False

        if positive:
            st.session_state.last_topic = None
            return "Hienoa! 😄 Oli ilo auttaa sinua!"
        elif negative:
            # Jos käyttäjä vastaa ei, tarjotaan jatkokysymys lisäinfoa varten
            if last_topic and last_topic + "_lisä" in general_faq:
                return general_faq[last_topic + "_lisä"] + "\n\nHaluatko vielä lisätietoa tästä aiheesta? 😊"
            else:
                return (
                    "Voi ei! 😕 Ei hätää, voit olla suoraan yhteydessä asiakaspalveluumme:\n"
                    "- 📞 09 123 4567\n"
                    "- 📧 support@verkkokauppa.fi\n"
                    "- ⏰ ma–pe 9–17"
                )

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
            "Aina ilo auttaa! 😄"
        ])
    if any(sana in kysymys for sana in kehumiset):
        return "Kiitos! 😄 Teen parhaani auttaakseni."

    # --- Tuotelistaus ---
    if "tuotteet" in kysymys or ("näytä" in kysymys and "tuotte" in kysymys):
        if not tuotteet:
            return "Valitettavasti tuotteita ei ole saatavilla juuri nyt."
        lista = "\n".join(
            [f"- {t['nimi']} ({t['kategoria']}) – {t.get('hinta','Hinta ei saatavilla')}€" for t in tuotteet]
        )
        return f"Tässä meidän tuotteet:\n{lista}"

    # --- FAQ-avainsanat ---
    for key, topic in faq_keywords.items():
        if key in kysymys:
            st.session_state.last_topic = topic
            st.session_state.awaiting_confirmation = True
            return general_faq.get(topic, "Valitettavasti en löytänyt tietoa tästä aiheesta.") + "\n\nAuttoiko tämä sinua? 😊"

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

# --- Logiikka vastauksen hakemiseen ---
if submit_button and user_input:
    st.session_state.chat_history.append(("user", user_input))
    vastaus = get_vastaus(user_input)
    st.session_state.chat_history.append(("assistant", vastaus))

# --- Chat-historia ---
with chat_container.container():
    for sender, msg in st.session_state.chat_history[-50:]:
        st.chat_message(sender).write(msg)









