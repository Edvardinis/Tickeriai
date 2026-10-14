import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Mano Investicijų Dashboard", page_icon="📈", layout="wide")

st.title("📊 Asmeninis Investicijų Dashboard")
st.markdown("Nemokamas, interaktyvus įrankis tavo stebimiems aktyvams stebėti.")

# Tickeriai ir jų Yahoo Finance simboliai
tickers = {
    "Auksas (XAU)": "GC=F",
    "Gamtinės dujos (XNG)": "NG=F",
    "Nafta WTI (XTI)": "CL=F",
    "Bitcoin (BTC)": "BTC-USD",
    "Quant (QNT)": "QNT-USD",
    "Intel (INTC)": "INTC",
    "Netflix (NFLX)": "NFLX",
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "USDCAD=X"
}

# Pasirinkimas šoniniame meniu
selected_name = st.sidebar.selectbox("Pasirink aktyvą:", list(tickers.keys()))
ticker_symbol = tickers[selected_name]

period = st.sidebar.selectbox("Laikotarpis:", ["1 mėn.", "3 mėn.", "6 mėn.", "1 metai", "Nuo metų pradžios"], index=1)
period_map = {"1 mėn.": "1mo", "3 mėn.": "3mo", "6 mėn.": "6mo", "1 metai": "1y", "Nuo metų pradžios": "ytd"}

interval = st.sidebar.selectbox("Intervalas (Žvakės):", ["1 diena", "1 valanda"], index=0)
interval_map = {"1 diena": "1d", "1 valanda": "60m"}

st.subheader(f"🕯️ Žvakių grafikas: {selected_name} ({ticker_symbol})")

@st.cache_data(ttl=300)
def load_data(symbol, p, i):
    data = yf.download(symbol, period=p, interval=i, progress=False)
    return data

data = load_data(ticker_symbol, period_map[period], interval_map[interval])

if not data.empty:
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
        
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=selected_name
    )])
    
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Kaina (USD)",
        height=500,
        margin=dict(l=10, r=10, t=30, b=10),
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    latest_close = float(data['Close'].iloc[-1])
    prev_close = float(data['Close'].iloc[-2])
    change = latest_close - prev_close
    pct_change = (change / prev_close) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Paskutinė kaina", f"{latest_close:.4f} USD", f"{pct_change:+.2f}%")
    col2.metric("Aukščiausia (periodas)", f"{float(data['High'].max()):.4f} USD")
    col3.metric("Žemiausia (periodas)", f"{float(data['Low'].min()):.4f} USD")
else:
    st.warning("Nepavyko gauti duomenų šiam aktyvui. Pabandykite vėliau arba pasirinkite kitą laikotarpį.")

st.markdown("---")
st.subheader("📌 Makroekonominė įtaka ir strateginiai punktai stebimiems tickeriams")

st.markdown("""
Štai 5 pagrindiniai punktai, įvertinantys dabartinę rinkų dinamiką ir jų įtaką tavo portfeliui:

1. **Energetikos ištekliai (XNG ir XTI):** Gamtinių dujų ir naftos kainų svyravimai tiesiogiai veikia infliacijos lūkesčius. Geopoltinė įtampa bei atsargų pokyčiai JAV sukelia didelį *volatility*, todėl pozicijų rizikos valdymas (stop-loss) čia yra kritinis.
2. **Taurusis metalas (XAU):** Auksas išlieka pagrindiniu saugiu prieglobsčiu (safe haven) esant makroekonominiam neapibrėžtumui ir centrinių bankų palūkanų normų pokyčiams. Silpnėjantis doleris arba infliacijos šuoliai teigiamai veikia XAU kainą.
3. **Kriptovaliutų rinkos dinamika (BTC ir QNT):** Bitcoin likvidumas ir institucinis kapitalo srautas lemia visos kripto rinkos kryptį. Quant (QNT) specifiniai integraciniai sprendimai bankiniame sektoriuje suteikia nepriklausomą impulsą, tačiau koreliacija su bendra rizikingų aktyvų nuotaika išlieka aukšta.
4. **Akcijų rinka (INTC ir NFLX):** 
   - *Intel (INTC):* Technologijų sektoriaus tiekimo grandinės ir puslaidininkių paklausa lemia atsigavimo perspektyvas.
   - *Netflix (NFLX):* Vartotojų prenumeratos augimo rodikliai ir reklamos modelio plėtra stiprina pozicijas prieš konkurentus.
5. **Forex poros (EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD):** JAV dolerio stiprumas ar silpnumas, lemiamas Federalinio Rezervų Banko (FED) palūkanų sprendimų, daro didžiausią įtaką visoms 5 pagrindinėms Forex poroms, nustatydamas valiutų kursų kryptį.
6. **Rizikos valdymas ir naujienų kalendorius:** Makroekonominiai duomenys (NFP, infliacija CPI, FED posėdžiai) sukelia staigius kainų šuolius, todėl prieš svarbias naujienas rekomenduojama peržiūrėti atviras pozicijas visuose stebimuose aktyvuose.
""")
  
