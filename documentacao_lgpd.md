# 🔐 Documentação de Governança de Dados (LGPD)

## 🧾 Objetivo

Garantir que os dados utilizados no projeto estejam em conformidade com os princípios da **Lei Geral de Proteção de Dados Pessoais (LGPD)**.

---

## ✅ Ações Implementadas

### 1. Anonimização de Identificadores Pessoais

- O identificador `user_pseudo_id` foi convertido em `hash_id` utilizando algoritmo **SHA-256**, impedindo a identificação reversa do usuário.

### 2. Simulação de Consentimento

- Foi assumido que **10% dos usuários não consentiram com o uso de seus dados**, sendo assim excluídos do dataset final de análise.

### 3. Minimização de Dados

- Apenas dados necessários para análise de comportamento foram utilizados (eventos, categorias e métricas agregadas).
- Nenhum dado sensível foi coletado ou inferido.

---

## 📌 Considerações Finais

Este projeto é apenas um exercício de estudo e não coleta ou processa dados pessoais reais. As práticas aqui simuladas visam educar e exemplificar a importância da **privacidade desde o design (Privacy by Design)**.

---

**Autor:** Pedro Ribeiro  
**Última Atualização:** Abril de 2025
