import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

import os

# This prints the directory of the current script
print("Script directory:", os.path.dirname(os.path.abspath(__file__)))

# This prints the full path (including filename)
print("Full path to script:", os.path.abspath(__file__))


def bereken_ncw(kasstromen, disconteringsvoet):
    """Bereken de Netto Contante Waarde (NCW)"""
    jaren = np.arange(len(kasstromen))
    ncw = sum(kasstromen / (1 + disconteringsvoet) ** jaren)
    return ncw

def bereken_tvt(kasstromen, initiële_investering):
    """Bereken de terugverdientijd (TVT)"""
    cumulatieve_kasstroom = np.cumsum(kasstromen)  # Bereken cumulatieve kasstroom
    jaren = np.where(cumulatieve_kasstroom >= 0)[0]  # Zoek het eerste jaar waarin de investering is terugverdiend
    return int(jaren[0]) if len(jaren) > 0 else None

st.title("Frisdrankfabriek Business Case Analyse")

# Gebruikersinput via Streamlit
initiële_investering        = st.number_input("Startinvestering in euro", value=1000.0)
verkoopprijs_per_eenheid    = st.number_input("Verkoopprijs per fles frisdrank", value=1.5)
productiekosten_per_eenheid = st.number_input("Kosten om één fles te produceren", value=0.5)
aantal_verkochte_eenheden   = st.number_input("Hoeveelheid flesjes verkocht", value=1000)
onderzoek_en_ontwikkeling   = st.number_input("R&D kosten voor nieuwe smaak", value=1000.0)
keurings_en_testkosten      = st.number_input("Certificering en kwaliteitscontroles", value=1000.0)

st.subheader("Overige kosten")
opslagkosten        = st.number_input("Opslagkosten", value=1000.0)
distributiekosten   = st.number_input("Distributiekosten", value=1000.0)
personeelskosten    = st.number_input("Personeelskosten", value=1000.0)
fabriekskosten      = st.number_input("Fabriekskosten", value=1000.0)
verpakkingskosten   = st.number_input("Verpakkingskosten", value=1000.0)
marketingkosten     = st.number_input("Marketingkosten", value=1000.0)

# Berekeningen
inkomsten = aantal_verkochte_eenheden * verkoopprijs_per_eenheid
productiekosten = aantal_verkochte_eenheden * productiekosten_per_eenheid
totale_kosten = (productiekosten + fabriekskosten + verpakkingskosten + marketingkosten +
                 opslagkosten + distributiekosten + personeelskosten) + onderzoek_en_ontwikkeling + keurings_en_testkosten

kasstromen = np.insert(inkomsten - totale_kosten, 0, -initiële_investering)

disconteringsvoet = 0.08

# NCW en TVT berekenen
tvt = bereken_tvt(kasstromen, initiële_investering)
ncw = bereken_ncw(kasstromen, disconteringsvoet)

st.subheader("Resultaten")
st.write(f"Terugverdientijd (TVT): {tvt} jaar")
st.write(f"Netto Contante Waarde (NCW): {ncw:.2f}")

# Plot de kasstromen
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(range(len(kasstromen)), kasstromen, color='blue', alpha=0.7)
ax.set_xlabel('Jaren')
ax.set_ylabel('Kasstromen')
ax.set_title('Jaarlijkse Kasstromen van de Frisdrankfabriek')
ax.grid()
st.pyplot(fig)
