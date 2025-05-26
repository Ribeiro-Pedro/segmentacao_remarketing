from google.cloud import bigquery
import pandas as pd
import os

# --- Configurações ---
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ecommerce_dashboard\credentials.json"  # Altere!

PROJECT_ID = 'bigquery-public-data'
DATASET = 'ga4_obfuscated_sample_ecommerce'
TABLE = 'events_*'

# --- Função para extrair dados ---
def extract_data():
    client = bigquery.Client()
    
    query = f"""
        SELECT
            event_date,
            event_name,
            user_pseudo_id,
            event_bundle_sequence_id,
            event_timestamp,
            geo.country,
            traffic_source.source AS traffic_source,
            device.category AS device_category,
            ecommerce.total_item_quantity,
            ecommerce.purchase_revenue_in_usd
        FROM
            `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE
            _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
            AND event_name IN ('purchase', 'add_to_cart', 'view_item', 'begin_checkout')
    """
    
    print("Executando consulta no BigQuery...")
    df = client.query(query).to_dataframe()
    print(f"Consulta concluída. {len(df)} registros extraídos.")
    
    return df

# --- Função de pré-processamento ---
def preprocess_data(df):
    print("Iniciando pré-processamento...")
    
    # Converter event_date para datetime
    df['event_date'] = pd.to_datetime(df['event_date'], format='%Y%m%d')
    
    # Normalizar nomes de eventos
    df['event_name'] = df['event_name'].str.lower().str.strip()
    
    # Criar identificadores de sessão: combinando user_pseudo_id + event_date + sequence_id
    df['session_id'] = df['user_pseudo_id'].astype(str) + '_' + df['event_date'].astype(str) + '_' + df['event_bundle_sequence_id'].astype(str)
    
    # Ordenar eventos para reconstrução de funis
    df = df.sort_values(['user_pseudo_id', 'event_timestamp'])
    
    # Remover possíveis duplicatas
    df = df.drop_duplicates()

    print("Pré-processamento concluído.")
    return df

# --- Função para salvar os dados ---
def save_data(df, output_path='ecommerce_dashboard\data\ecommerce_data_preprocessed.csv'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dados salvos em {output_path}")

# --- Main ---
if __name__ == "__main__":
    df_raw = extract_data()
    df_processed = preprocess_data(df_raw)
    save_data(df_processed)
