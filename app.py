import streamlit as st

from data_processor import get_city_data, prepare_weather_data, get_monthly_averages
from data_visualizer import plot_monthly_sunshine

with st.spinner("Načítám a zpracovávám data..."):
    df_data_brno = get_city_data("Brno")
    df_data_plzen = get_city_data("Plzeň")
    df_data = prepare_weather_data([df_data_brno, df_data_plzen])
    df_monthly_data = get_monthly_averages(df_data)

if df_monthly_data.empty:
    st.error("Nepodařilo se načíst nebo zpracovat data.")
    st.stop()

st.markdown("""

            # Porovnání počasí v Brně a v Plzni

            ## Průměrná délka slunečního svitu – měsíční hodnoty

            """)

st.plotly_chart(plot_monthly_sunshine(df_monthly_data))

st.markdown("""
            
            ### Popis:
                        
            Graf zobrazuje průměrnou denní délku slunečního svitu v Brně a Plzni pro jednotlivé měsíce. 
            Údaje vycházejí z historických dat Open-Meteo API (období 2022 až současnost). 
            Hodnoty udávají průměrný počet hodin slunečního svitu za den v daném měsíci.

            ### Závěr:
            
            Z porovnání vyplývá, že Brno má po většinu roku delší sluneční svit než Plzeň. 
            Nejvýraznější rozdíly se objevují v zimních měsících.

            """)
