import requests
import pandas as pd
from sqlalchemy import create_engine

# Clave de API (debes registrarte en Alpha Vantage para obtenerla)
API_KEY = "TU_API_KEY"
SYMBOL = "AAPL"

# URL de la API para datos de acciones
def obtener_datos_financieros(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=compact"
    response = requests.get(url)
    data = response.json()
    return data.get("Time Series (Daily)", {})

# Procesar los datos en un DataFrame
def procesar_datos(datos):
    df = pd.DataFrame.from_dict(datos, orient='index')
    df.reset_index(inplace=True)
    df.columns = ['fecha', 'apertura', 'maximo', 'minimo', 'cierre', 'volumen']
    df['fecha'] = pd.to_datetime(df['fecha'])
    return df

# Guardar los datos en MySQL
def guardar_en_mysql(df):
    DATABASE_URL = "mysql+pymysql://root:password@localhost/base de datos"
    engine = create_engine(DATABASE_URL)
    df.to_sql('datos_financieros', con=engine, if_exists='replace', index=False)
    print("Datos guardados en MySQL correctamente")

# Ejecutar proceso
datos = obtener_datos_financieros(SYMBOL)
df = procesar_datos(datos)
guardar_en_mysql(df)
print(df.head())
