
import streamlit as st
import datetime
import pandas as pd

# 1. NASTAVENIE DIZAJNU WEBU
st.set_page_config(page_title="FérovéHotely.sk", page_icon="🏨", layout="wide")

st.title("🏨 FérovéHotely.sk")
st.subheader("Porovnávač ubytovania: Radenie podľa celkového hodnotenia s najnižšou cenou napriamo")

# 2. DATABÁZA HOTELOV
hotely_databaza = [
    {"nazov": "Hotel Zlatý Kľúčik (Nitra)", "region": "Západné Slovensko", "mesto": "Nitra", "google_rating": 4.7, "cena_noc": 130, "web_hotela": "https://zlatyklyucik.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.3245, "lon": 18.0961},
    {"nazov": "Hotel Holiday Inn (Trnava)", "region": "Západné Slovensko", "mesto": "Trnava", "google_rating": 4.6, "cena_noc": 110, "web_hotela": "https://holidayinn-trnava.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.3780, "lon": 17.5890},
    {"nazov": "Hotel Penzión Pribina (Nitra)", "region": "Západné Slovensko", "mesto": "Nitra", "google_rating": 4.4, "cena_noc": 65, "web_hotela": "https://penzionpribina.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.3115, "lon": 18.0865},
    {"nazov": "Hotel Národný Dom (Banská Bystrica)", "region": "Stredné Slovensko", "mesto": "Banská Bystrica", "google_rating": 4.4, "cena_noc": 75, "web_hotela": "https://hotelnarodnydom.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.7352, "lon": 19.1461},
    {"nazov": "Hotel Ambra (Žilina)", "region": "Stredné Slovensko", "mesto": "Žilina", "google_rating": 4.5, "cena_noc": 80, "web_hotela": "https://hotelambra.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 49.2231, "lon": 18.7394},
    {"nazov": "Boutique Hotel Slávia (Košice)", "region": "Východné Slovensko", "mesto": "Košice", "google_rating": 4.8, "cena_noc": 125, "web_hotela": "https://hotelslavia.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.7214, "lon": 21.2582},
    {"nazov": "Hotel Metropol (Spišská Nová Ves)", "region": "Východné Slovensko", "mesto": "Spišská Nová Ves", "google_rating": 4.3, "cena_noc": 55, "web_hotela": "https://hotel-metropol.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.9442, "lon": 20.5615}
]

# 3. FILTRE V BOČNOM PANELI
st.sidebar.header("🔍 Nastavenia vyhľadávania")
vybraty_region = st.sidebar.selectbox("Vyberte región Slovenska:", ["Západné Slovensko", "Stredné Slovensko", "Východné Slovensko"])

dnes = datetime.date.today()
termin = st.sidebar.date_input("Termín pobytu (Príchod - Odchod):", [dnes, dnes + datetime.timedelta(days=2)])
pocet_osob = st.sidebar.number_input("Počet osôb:", min_value=1, value=2)

st.sidebar.markdown("---")
st.sidebar.header("💰 Cenové a kvalitatívne filtre")
max_rozpocet = st.sidebar.slider("Koľko ste ochotný dať za CELÝ pobyt? (€)", min_value=30, max_value=500, value=250, step=10)

sposob_radenia = st.sidebar.radio(
    "Zoradiť výsledky podľa:",
    ["Celkového hodnotenia (Od najvyššieho)", "Ceny za pobyt (Od najlacnejšieho)"]
)

# 4. LOGIKA VÝPOČTU A FILTROVANIA
if len(termin) == 2:
    datum_od, datum_do = termin
    pocet_noci = (datum_do - datum_od).days
    
    if pocet_noci == 0:
        st.error("Dátum odchodu musí byť iný ako dátum príchodu.")
        st.stop()
        
    ziadane_dni = [str(datum_od + datetime.timedelta(days=x)) for x in range(pocet_noci)]
    filtrovane_hotely = []
    map_data = []

    for hotel in hotely_databaza:
        if hotel["region"] == vybraty_region:
            celkova_cena_pobytu = hotel["cena_noc"] * pocet_noci
            if celkova_cena_pobytu <= max_rozpocet:
                je_volny = not any(den in hotel["obsadene_dni"] for den in ziadane_dni)
                if je_volny:
                    hotel_kopia = hotel.copy()
                    hotel_kopia["celkova_cena"] = celkova_cena_pobytu
                    filtrovane_hotely.append(hotel_kopia)
                    map_data.append({"lat": hotel["lat"], "lon": hotel["lon"], "name": hotel["nazov"]})

    if sposob_radenia == "Celkového hodnotenia (Od najvyššieho)":
        hotely_zoradene = sorted(filtrovane_hotely, key=lambda x: (-x["google_rating"], x["celkova_cena"]))
    else:
        hotely_zoradene = sorted(filtrovane_hotely, key=lambda x: x["celkova_cena"], reverse=False)

    # 5. ZOBRAZENIE NA STRÁNKE
    st.write(f"### 📋 Nájdené ubytovania v cene do **{max_rozpocet} €** za celý pobyt ({pocet_noci} nocí)")
    col_lavo, col_pravo = st.columns(2)

    with col_lavo:
        if hotely_zoradene:
            for hotel in hotely_zoradene:
                with st.expander(f"⭐ {hotel['google_rating']} - {hotel['nazov']} ({hotel['celkova_cena']} € za pobyt)", expanded=True):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"📍 Mesto: {hotel['mesto']} | Celkové hodnotenie: **{hotel['google_rating']} / 5**")
                        st.write(f"💵 Cena za jednu noc: {hotel['cena_noc']} €")
                    with c2:
                        st.link_button("🌐 Najnižšia cena napriamo", hotel["web_hotela"], type="primary", use_container_width=True)
                        st.link_button("Cez Booking.com", hotel["booking_url"], use_container_width=True)
        else:
            st.warning(f"Ľutujeme, v regióne {vybraty_region} nemáme na tento termín žiadny hotel voľný v cene do {max_rozpocet} €.")

    with col_pravo:
        st.write("#### 📍 Poloha hotelov v cenovej relácii")
        if map_data and hotely_zoradene:
            st.map(pd.DataFrame(map_data))
else:
    st.info("Pre zobrazenie hotelov označte v kalendári dva dátumy.")
