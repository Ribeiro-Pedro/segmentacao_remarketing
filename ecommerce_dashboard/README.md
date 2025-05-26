# Ecommerce Analytics Dashboard (V1)

Este projeto tem como objetivo analisar dados reais de um e-commerce utilizando a amostra pública do GA4 no BigQuery e desenvolver um dashboard analítico com Streamlit.

## 📁 Estrutura de Pastas

```
ecommerce_dashboard_v1/
├── data/
│   └── dados_ga4_ecommerce.csv          # Dataset pré-processado
├── notebooks/
│   └── eda_ga4_ecommerce.ipynb          # Coleta, pré-processamento e EDA
├── app/
│   └── dashboard.py                     # Código do dashboard Streamlit
├── requirements.txt                     # Dependências do projeto
└── README.md                            # Instruções do projeto
```

## 🚀 Como executar

1. Clone este repositório e entre no diretório:

```bash
git clone https://github.com/seuusuario/ecommerce_dashboard_v1.git
cd ecommerce_dashboard_v1
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o acesso ao BigQuery (se necessário) conforme instruções da [Google Cloud](https://cloud.google.com/bigquery/docs/quickstarts).

4. Execute o notebook de EDA:

```bash
cd notebooks
jupyter notebook eda_ga4_ecommerce.ipynb
```

5. Execute o dashboard:

```bash
cd ../app
streamlit run dashboard.py
```

## 📊 Funcionalidades (V1)

- Análise exploratória de eventos (visualização, adição ao carrinho, compras)
- Análise temporal dos eventos
- Receita por país
- Comportamento por dispositivo
- Dashboard interativo com Streamlit

## 🛠 Tecnologias

- Python
- Google BigQuery
- Pandas, Seaborn, Matplotlib
- Streamlit
- Plotly

## 📌 Observações

- Os dados utilizados são públicos, disponíveis em `bigquery-public-data.ga4_obfuscated_sample_ecommerce`.
- A autenticação GCP pode ser feita via variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS`.

---

Projeto criado para fins de portfólio de Data Science end-to-end.