# 🎯 Projeto: Segmentação de Usuários Elegíveis para Remarketing

Este projeto simula um pipeline analítico de dados de comportamento de usuários com foco na **ativação de dados para campanhas de remarketing**, respeitando boas práticas de **governança (LGPD)** e entregando **insights visuais por meio de um dashboard interativo**.

---

## 📌 Objetivos

- Explorar dados de e-commerce da amostra pública do Google Analytics 4.
- Definir regras de negócio para classificar usuários como **elegíveis para campanhas de remarketing**.
- Aplicar práticas de **anonimização e simulação de consentimento**, em conformidade com a LGPD.
- Construir um **dashboard interativo com Streamlit** para visualização dos resultados e apoio à decisão.

---

## 📊 Visão Geral do Projeto

| Etapa                         | Descrição                                                                 |
|------------------------------|---------------------------------------------------------------------------|
| 📥 Extração de dados         | Consulta via BigQuery no dataset `ga4_obfuscated_sample_ecommerce`.      |
| 🧹 Preparação dos dados      | Criação de features comportamentais por usuário.                          |
| ✅ Regras de Segmentação     | Definição de critérios para remarketing.                                  |
| 🔐 Governança de dados       | Anonimização e simulação de consentimento conforme LGPD.                  |
| 📈 Visualização              | Dashboard com gráficos interativos via Streamlit.                         |

---

## 📁 Estrutura do Repositório

- `app.py`  
  Código da aplicação Streamlit para visualização interativa.

- `processamento.py`  
  Script que realiza a transformação, regras de negócio e anonimização.

- `documentacao_lgpd.md`  
  Documento explicando as práticas de governança adotadas no projeto.

- `README.md`  
  Este arquivo com explicações completas sobre o projeto.

---

## 🧠 Regras de Negócio para Segmentação

Um usuário será considerado **elegível para remarketing** caso:

- Nunca tenha comprado (`flag_comprou == 0`) **e** tenha número de visualizações acima da mediana;  
- **Ou** tenha interagido em mais de um dia diferente;  
- **Ou** tenha adicionado mais de 1 item ao carrinho.

Essas regras foram escolhidas por sua **alta interpretabilidade e aplicabilidade direta** em um contexto de negócio real.

---

## 📌 Governança e LGPD

Este projeto incorpora simulações de conformidade com a LGPD:

- 🔒 **Anonimização de IDs de usuário** com hashing SHA-256;
- ✅ **Simulação de consentimento** com 10% dos usuários "optando por não compartilhar dados";
- 📚 **Documentação de sensibilidade de dados** no arquivo `documentacao_lgpd.md`.

---

## 📊 Visualizações Interativas

A aplicação Streamlit oferece:

- 📦 Distribuição das categorias mais acessadas pelos usuários elegíveis;
- 📈 Gráficos comparativos de comportamento (views, adds, dias ativos);
- 🔍 Filtros dinâmicos por categoria;

Para executar localmente:

```bash
streamlit run app.py
