# 📊 Indicadores COVID-19 + PIB (World Bank)

Pipeline de extração, tratamento e integração de dados de COVID-19 e PIB
anual do Brasil.

## 📌 Sobre o projeto

Este projeto realiza a coleta automática de:

-   **Dados históricos de COVID-19 do Brasil** (casos, óbitos, novos
    casos e média móvel)\
    Fonte: API pública *disease.sh*
-   **Dados anuais de PIB do Brasil**\
    Fonte: *World Bank Open Data API*

O resultado final é um arquivo CSV consolidado:

    data/indicadores_covid_pib.csv

## 🏗️ Funcionalidades

### ✔️ 1. Baixar dados de COVID-19

A função `get_covid()` baixa e processa todos os dados históricos,
gerando:

-   Casos acumulados\
-   Óbitos acumulados\
-   Novos casos por dia\
-   Média móvel de 7 dias\
-   Ano e mês da observação

### ✔️ 2. Baixar dados do World Bank

A função `get_worldbank()` obtém o indicador econômico desejado --- por
padrão:

-   **NY.GDP.MKTP.CD** → PIB (US\$ correntes)

### ✔️ 3. Pipeline principal

A função `main()` executa:

-   Agregação mensal dos dados de COVID-19\
-   Junção com o PIB anual\
-   Geração do arquivo final em `data/`

## 📂 Estrutura de diretórios

    project/
    │── final.py
    │── data/
    │     └── indicadores_covid_pib.csv
    └── README.md

## ▶️ Como executar

### 1. Instale as dependências

``` bash
pip install requests pandas
```

### 2. Execute o script

``` bash
python final.py
```

### 3. Arquivo gerado

    data/indicadores_covid_pib.csv

## 🔧 Tecnologias utilizadas

-   Python 3+
-   Pandas
-   Requests
-   APIs:
    -   disease.sh
    -   World Bank Open Data

## 📌 Possíveis melhorias futuras

-   Mais indicadores econômicos
-   Gráficos automáticos
-   Suporte a múltiplos países
-   Exportação XLSX/JSON
