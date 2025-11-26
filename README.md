# Weather Comparison App

Aplikace pro porovnávání počasí mezi různými městy v České republice.  
Projekt demonstruje práci s daty z veřejného **REST API**, jejich zpracování pomocí **Pandas**, vizualizaci s **Plotly** a interaktivní prezentaci ve **Streamlitu**.

## Online prezentace
Aplikaci můžete vyzkoušet přímo online přes Streamlit: [ :arrow_forward: Spustit Weather Comparison App](https://weather-comparison-app.streamlit.app/)

## Porovnávaná města
- **Brno**
- **Plzeň**

## Sledované meteorologické ukazatele
- **Sunshine duration** – délka slunečního svitu za den

## Použité technologie a knihovny
- **REST API** – získávání historických dat o počasí  
- **Pandas** – zpracování a analýza dat  
- **Plotly** – tvorba interaktivních grafů  
- **Streamlit** – distribuce aplikace přes webové rozhraní  

## Spuštění aplikace
1. Klonujte repozitář:
```
git clone https://github.com/DagyDee/weather-comparison-app.git
```
2. Nainstalujte závislosti:
```
pip install -r requirements.txt
```
3. Spusťte aplikaci lokálně:
```
streamlit run app.py
```

## Zdroj dat
Data jsou získávána z veřejného [Open-Meteo API](https://open-meteo.com/).
