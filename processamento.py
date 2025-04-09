from google.cloud import bigquery
import pandas as pd
import hashlib
import random

def consulta_bigquery():
    client = bigquery.Client()

    query = """
    WITH eventos_agg AS (
      SELECT
        user_pseudo_id,
        COUNTIF(event_name = "purchase") AS n_compras,
        COUNTIF(event_name = "add_to_cart") AS n_adds,
        COUNTIF(event_name = "view_item") AS n_views,
        SUM(IFNULL(revenue, 0)) AS total_receita,
        COUNT(DISTINCT event_date) AS dias_ativos,
        APPROX_TOP_COUNT(item_category, 1)[OFFSET(0)].value AS top_category
      FROM (
        SELECT
          user_pseudo_id,
          event_name,
          event_date,
          (SELECT value.double_value FROM UNNEST(event_params) WHERE key = "value") AS revenue,
          (SELECT value.string_value FROM UNNEST(event_params) WHERE key = "item_category") AS item_category
        FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
        WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
          AND event_name IN ("purchase", "view_item", "add_to_cart")
      )
      GROUP BY user_pseudo_id
    )

    SELECT * FROM eventos_agg
    """

    df = client.query(query).to_dataframe()
    return df

def aplicar_regras_remarketing(df):
    df['flag_comprou'] = df['n_compras'].apply(lambda x: 1 if x > 0 else 0)

    cond1 = (df['flag_comprou'] == 0) & (df['n_views'] > df[df['flag_comprou'] == 0]['n_views'].median())
    cond2 = (df['flag_comprou'] == 0) & (df['dias_ativos'] > 1)
    cond3 = (df['flag_comprou'] == 0) & (df['n_adds'] > 1)

    df['flag_remarketing'] = (cond1 | cond2 | cond3).astype(int)
    return df

def anonimizar_usuarios(df):
    df['hash_id'] = df['user_pseudo_id'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
    df['consentimento'] = df['user_pseudo_id'].apply(lambda x: 0 if random.random() < 0.1 else 1)
    df = df[df['consentimento'] == 1]
    df = df.drop(columns=['user_pseudo_id', 'consentimento'])
    return df

def salvar_csv(df, caminho='dados/dados_usuarios_remarketing.csv'):
    df.to_csv(caminho, index=False)

if __name__ == "__main__":
    df = consulta_bigquery()
    df = aplicar_regras_remarketing(df)
    df = anonimizar_usuarios(df)
    salvar_csv(df)
