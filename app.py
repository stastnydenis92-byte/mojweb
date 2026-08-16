import streamlit as st
import datetime
import pandas as pd

# 1. NASTAVENIE DIZAJNU A MODERNEJ TÉMY
st.set_page_config(page_title="FérovéHotely.sk", page_icon="🏨", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
    }
    
    .hotel-card {
        background-color: white;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    .rating-badge {
        background-color: #fef9c3;
        color: #854d0e;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
    }
    
    .btn-direct {
        background-color: #10b981;
        color: white !important;
        padding: 12px 20px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        display: block;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .btn-booking {
        background-color: #1e40af;
        color: white !important;
        padding: 12px 20px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        display: block;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1e293b; font-weight: 800;'>🏨 FérovéHotely.sk</h1>", unsafe_allow_html=True)

# Databáza so 100% stabilnými odkazmi na Imgur, ktoré žiadny server neblokuje
hotely_databaza = [
    {
        "nazov": "Hotel Zlatý Kľúčik", "region": "Západné Slovensko", "mesto": "Nitra", "google_rating": 4.7, "cena_noc": 130, 
        "web_hotela": "https://zlatyklyucik.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.3245, "lon": 18.0961,
        "foto": "https://imgur.com"
    },
    {
        "nazov": "Hotel Holiday Inn", "region": "Západné Slovensko", "mesto": "Trnava", "google_rating": 4.6, "cena_noc": 110, 
        "web_hotela": "https://holidayinn-trnava.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.3780, "lon": 17.5890,
        "foto": "https://imgur.com"
    },
    {
        "nazov": "Hotel Penzión Pribina", "region": "Západné Slovensko", "mesto": "Nitra", "google_rating": 4.4, "cena_noc": 65, 
        "web_hotela": "https://penzionpribina.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.3115, "lon": 18.0865,
        "foto": "https://imgur.com"
    },
    {
        "nazov": "Hotel Národný Dom", "region": "Stredné Slovensko", "mesto": "Banská Bystrica", "google_rating": 4.4, "cena_noc": 75, 
        "web_hotela": "https://hotelnarodnydom.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.7352, "lon": 19.1461,
        "foto": "https://imgur.com"
    },
    {
        "nazov": "Hotel Ambra", "region": "Stredné Slovensko", "mesto": "Žilina", "google_rating": 4.5, "cena_noc": 80, 
        "web_hotela": "https://hotelambra.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 49.2231, "lon": 18.7394,
        "foto": "https://imgur.com"
    },
    {
        "nazov": "Boutique Hotel Slávia", "region": "Východné Slovensko", "mesto": "Košice", "google_rating": 4.8, "cena_noc": 125, 
        "web_hotela": "https://hotelslavia.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.7214, "lon": 21.2582,
        "foto": "https://imgur.com"
    }
]

st.sidebar.header("🔍 Nastavenia")
vybraty_region = st.sidebar.selectbox("Región:", ["Západné Slovensko", "Stredné Slovensko", "Východné Slovensko"])
dnes = datetime.date.today()
termin = st.sidebar.date_input("Termín:", [dnes, dnes + datetime.timedelta(days=2)])
max_rozpocet = st.sidebar.slider("Rozpočet (€):", min_value=30, max_value=500, value=250, step=10)
sposob_radenia = st.sidebar.radio("Zoradiť podľa:", ["Hodnotenia (Od najlepšieho)", "Ceny (Od najlacnejšieho)"])

if len(termin) == 2:
    datum_od, datum_do = termin
    pocet_noci = (datum_do - datum_od).days
    
    if pocet_noci == 0:
        st.error("Chybný termín.")
        st.stop()
        
    ziadane_dni = [str(datum_od + datetime.timedelta(days=x)) for x in range(pocet_noci)]
    filtrovane_hotely = []
    map_data = []

    for hotel in hotely_databaza:
        if hotel["region"] == vybraty_region:
            celkova_cena_pobytu = hotel["cena_noc"] * pocet_noci
            if celkova_cena_pobytu <= max_rozpocet:
                hotel_kopia = hotel.copy()
                hotel_kopia["celkova_cena"] = celkova_cena_pobytu
                filtrovane_hotely.append(hotel_kopia)
                map_data.append({"lat": hotel["lat"], "lon": hotel["lon"], "name": hotel["nazov"]})

    if sposob_radenia == "Hodnotenia (Od najlepšieho)":
        hotely_zoradene = sorted(filtrovane_hotely, key=lambda x: (-x["google_rating"], x["celkova_cena"]))
    else:
        hotely_zoradene = sorted(filtrovane_hotely, key=lambda x: x["celkova_cena"])

    col_lavo, col_pravo = st.columns(2)

    with col_lavo:
        if hotely_zoradene:
            for hotel in hotely_zoradene:
                st.markdown(f"""
                    <div class="hotel-card">
                        <img src="{hotel['foto']}" style="width: 100%; border-radius: 12px; height: 180px; object-fit: cover; margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin:0; font-size:18px; font-weight:700; color:#1e293b;">{hotel['nazov']}</h4>
                            <span class="rating-badge">⭐ {hotel['google_rating']}</span>
                        </div>
                        <p style="color: #64748b; font-size: 14px; margin: 5px 0 15px 0;">📍 {hotel['mesto']} | Celkom: <strong>{hotel['celkova_cena']} €</strong> za {pocet_noci} nocí</p>
                        <a href="{hotel['web_hotela']}" target="_blank" class="btn-direct">🌐 Rezervovať napriamo</a>
                        <a href="{hotel['booking_url']}" target="_blank" class="btn-booking">Cez Booking.com</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Žiadne hotely v tejto cene.")

    with col_pravo:
        if map_data:
            st.map(pd.DataFrame(map_data))
else:
    st.info("Označte dva dátumy.")
