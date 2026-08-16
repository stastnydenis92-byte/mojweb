import streamlit as st
import datetime
import pandas as pd

# 1. NASTAVENIE DIZAJNU A MODERNEJ TÉMY
st.set_page_config(page_title="FérovéHotely.sk", page_icon="🏨", layout="wide")

# CSS kód na úpravu celkového vzhľadu (písmo, pozadie, zaoblenie)
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
    }
    
    /* Štýl pre hotelovú kartu */
    .hotel-card {
        background-color: white;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s;
    }
    .hotel-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    
    /* Hodnotenie - hviezdičky */
    .rating-badge {
        background-color: #fef9c3;
        color: #854d0e;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
        display: inline-block;
    }
    
    /* Vlastné tlačidlá cez HTML */
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
        font-size: 14px;
    }
    .btn-direct:hover { background-color: #059669; }
    
    .btn-booking {
        background-color: #1e40af;
        color: white !important;
        padding: 12px 20px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        display: block;
        text-align: center;
        font-size: 14px;
    }
    .btn-booking:hover { background-color: #1d4ed8; }
    </style>
""", unsafe_allow_html=True)

# Hlavička webu s moderným dizajnom
st.markdown("<h1 style='text-align: center; color: #1e293b; font-weight: 800;'>🏨 FérovéHotely.sk</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 18px; margin-bottom: 40px;'>Radenie podľa čistého Google hodnotenia. Rezervácie napriamo pre najlepšiu cenu.</p>", unsafe_allow_html=True)

# 2. ROZŠÍRENÁ DATABÁZA HOTELOV (Pridané fotky)
hotely_databaza = [
    {
        "nazov": "Hotel Zlatý Kľúčik", "region": "Západné Slovensko", "mesto": "Nitra", "google_rating": 4.7, "cena_noc": 130, 
        "web_hotela": "https://zlatyklyucik.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.3245, "lon": 18.0961,
        "foto": "https://unsplash.com"
    },
    {
        "nazov": "Hotel Holiday Inn", "region": "Západné Slovensko", "mesto": "Trnava", "google_rating": 4.6, "cena_noc": 110, 
        "web_hotela": "https://holidayinn-trnava.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.3780, "lon": 17.5890,
        "foto": "https://unsplash.com"
    },
    {
        "nazov": "Hotel Penzión Pribina", "region": "Západné Slovensko", "mesto": "Nitra", "google_rating": 4.4, "cena_noc": 65, 
        "web_hotela": "https://penzionpribina.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.3115, "lon": 18.0865,
        "foto": "https://unsplash.com"
    },
    {
        "nazov": "Hotel Národný Dom", "region": "Stredné Slovensko", "mesto": "Banská Bystrica", "google_rating": 4.4, "cena_noc": 75, 
        "web_hotela": "https://hotelnarodnydom.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.7352, "lon": 19.1461,
        "foto": "https://unsplash.com"
    },
    {
        "nazov": "Hotel Ambra", "region": "Stredné Slovensko", "mesto": "Žilina", "google_rating": 4.5, "cena_noc": 80, 
        "web_hotela": "https://hotelambra.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 49.2231, "lon": 18.7394,
        "foto": "https://unsplash.com"
    },
    {
        "nazov": "Boutique Hotel Slávia", "region": "Východné Slovensko", "mesto": "Košice", "google_rating": 4.8, "cena_noc": 125, 
        "web_hotela": "https://hotelslavia.sk", "booking_url": "https://booking.com", "obsadene_dni": [], "lat": 48.7214, "lon": 21.2582,
        "foto": "https://unsplash.com"
    }
]

# 3. FILTRE V BOČNOM PANELI (Vylepšený dizajn bočného panelu)
st.sidebar.markdown("<h3 style='color: #1e293b;'>🔍 Kam to bude?</h3>", unsafe_allow_html=True)
vybraty_region = st.sidebar.selectbox("Región Slovenska:", ["Západné Slovensko", "Stredné Slovensko", "Východné Slovensko"])

dnes = datetime.date.today()
termin = st.sidebar.date_input("Termín pobytu:", [dnes, dnes + datetime.timedelta(days=2)])

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color: #1e293b;'>💰 Váš rozpočet</h3>", unsafe_allow_html=True)
max_rozpocet = st.sidebar.slider("Maximálna cena za CELÝ pobyt (€):", min_value=30, max_value=500, value=250, step=10)

sposob_radenia = st.sidebar.radio(
    "Zoradiť podľa:",
    ["Hodnotenia (Od najlepšieho)", "Ceny (Od najlacnejšieho)"]
)

# 4. LOGIKA FILTROVANIA
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

    if sposob_radenia == "Hodnotenia (Od najlepšieho)":
        hotely_zoradene = sorted(filtrovane_hotely, key=lambda x: (-x["google_rating"], x["celkova_cena"]))
    else:
        hotely_zoradene = sorted(filtrovane_hotely, key=lambda x: x["celkova_cena"], reverse=False)

    # 5. ZOBRAZENIE S NOVÝM DIZAJNOM
    st.markdown(f"<h3 style='color: #1e293b; margin-bottom: 20px;'>📋 Nájdené hotely do {max_rozpocet} € ({pocet_noci} nocí)</h3>", unsafe_allow_html=True)
    
    col_lavo, col_pravo = st.columns([2, 1]) # Ľavý stĺpec je širší pre krajšie rozloženie

    with col_lavo:
        if hotely_zoradene:
            for hotel in hotely_zoradene:
                # HTML Karta hotela kombinovaná so Streamlit stĺpcami pre fotku a text
                st.markdown(f"""
                    <div class="hotel-card">
                        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                            <div style="flex: 1; min-width: 200px;">
                                <img src="{hotel['foto']}" style="width: 100%; border-radius: 12px; height: 160px; object-fit: cover;">
                            </div>
                            <div style="flex: 2; min-width: 250px; display: flex; flex-direction: column; justify-content: space-between;">
                                <div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                        <h3 style="margin: 0; color: #1e293b; font-size: 20px; font-weight: 700;">{hotel['nazov']}</h3>
                                        <span class="rating-badge">⭐ {hotel['google_rating']} / 5</span>
                                    </div>
                                    <p style="color: #64748b; margin: 0 0 8px 0; font-size: 14px;">📍 Mesto: {hotel['mesto']} | {hotel['region']}</p>
                                    <p style="color: #059669; font-size: 13px; font-weight: 500; margin: 0;">💡 Tip: Rezerváciou napriamo ušetríte hotelu províziu Bookingu.</p>
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 15px;">
                                    <div>
                                        <span style="color: #64748b; font-size: 12px; display: block;">Cena za noc: {hotel['cena_noc']} €</span>
                                        <span style="color: #1e293b; font-size: 24px; font-weight: 700;">{hotel['celkova_cena']} €</span>
                                        <span style="color: #64748b; font-size: 12px;">za celý pobyt</span>
                                    </div>
                                    <div style="width: 200px;">
                                        <a href="{hotel['web_hotela']}" target="_blank" class="btn-direct">🌐 Rezervovať napriamo</a>
                                        <a href="{hotel['booking_url']}" target="_blank" class="btn-booking">Cez Booking.com</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
