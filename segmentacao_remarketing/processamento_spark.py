import os
import random
import hashlib
from google.cloud import bigquery
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit, udf
from pyspark.sql.types import StringType, IntegerType

def inicializar_spark():
    """Inicializa uma sessão Spark."""
    spark = SparkSession.builder \
        .appName("ProcessamentoRemarketing") \
        .getOrCreate()
    return spark

def consulta_bigquery(spark):
    """Consulta o BigQuery e converte o resultado para Spark DataFrame."""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
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

    df_pd = client.query(query).to_dataframe()
    df = spark.createDataFrame(df_pd)
    return df

def aplicar_regras_remarketing(df):
    """Aplica regras de negócio para definir flag de remarketing."""
    df = df.withColumn('flag_comprou', when(col('n_compras') > 0, 1).otherwise(0))

    # Calcula a mediana de n_views para condicional
    n_views_median = df.filter(col('flag_comprou') == 0).approxQuantile("n_views", [0.5], 0.01)[0]

    cond1 = (col('flag_comprou') == 0) & (col('n_views') > n_views_median)
    cond2 = (col('flag_comprou') == 0) & (col('dias_ativos') > 1)
    cond3 = (col('flag_comprou') == 0) & (col('n_adds') > 1)

    df = df.withColumn('flag_remarketing', when(cond1 | cond2 | cond3, 1).otherwise(0))
    return df

def gerar_hash(user_id):
    """Gera hash SHA-256 para anonimização."""
    return hashlib.sha256(user_id.encode()).hexdigest()

def gerar_consentimento(_):
    """Gera flag de consentimento simulada (90% aprovados)."""
    return 0 if random.random() < 0.1 else 1

def anonimizar_usuarios(df):
    """Anonimiza usuários e filtra apenas aqueles com consentimento."""
    udf_hash = udf(gerar_hash, StringType())
    udf_consentimento = udf(gerar_consentimento, IntegerType())

    df = df.withColumn('hash_id', udf_hash(col('user_pseudo_id')))
    df = df.withColumn('consentimento', udf_consentimento(lit(1)))
    df = df.filter(col('consentimento') == 1)
    df = df.drop('user_pseudo_id', 'consentimento')
    return df

def salvar_parquet(df, caminho='dados/dados_usuarios_remarketing'):
    """Salva o DataFrame final em formato Parquet."""
    df.write.mode('overwrite').parquet(caminho)

def main():
    """Pipeline principal de processamento."""
    try:
        spark = inicializar_spark()
        df = consulta_bigquery(spark)
        df = aplicar_regras_remarketing(df)
        df = anonimizar_usuarios(df)
        salvar_parquet(df)
        print("Processamento concluído com sucesso!")
    except Exception as e:
        print(f"Erro durante o processamento: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
