import requests
import pandas as pd
from pathlib import Path

# Pasta de saída
OUT = Path("data")
OUT.mkdir(exist_ok=True)

# ===============================
# 1. Extrair dados COVID-19
# ===============================
def get_covid(country="brazil"):
    url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=all"
    r = requests.get(url).json()
    timeline = r.get("timeline", {})
    cases = pd.Series(timeline.get("cases", {}))
    deaths = pd.Series(timeline.get("deaths", {}))

    df = pd.DataFrame({
        "Data": pd.to_datetime(cases.index, format="%m/%d/%y", errors="coerce"),
        "Casos Acumulados": cases.values,
        "Óbitos Acumulados": deaths.values
    }).dropna()

    # Novos casos e média móvel
    df["Novos Casos"] = df["Casos Acumulados"].diff().fillna(0).clip(lower=0)
    df["Média Móvel (7 dias)"] = df["Novos Casos"].rolling(7, min_periods=1).mean()
    df["Ano"] = df["Data"].dt.year
    df["Mês"] = df["Data"].dt.month
    return df

# ===============================
# 2. Extrair dados World Bank
# ===============================
def get_worldbank(country_code="BR", indicator="NY.GDP.MKTP.CD"):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=5000"
    r = requests.get(url).json()
    df = pd.json_normalize(r[1])
    df = df[["date", "value"]].dropna()
    df.rename(columns={"date": "Ano", "value": "PIB (US$)"}, inplace=True)
    df["Ano"] = df["Ano"].astype(int)
    return df

# ===============================
# 3. Pipeline principal
# ===============================
def main():
    covid = get_covid("brazil")
    pib = get_worldbank("BR", "NY.GDP.MKTP.CD")

    # Agrega COVID por ano/mês
    covid_monthly = covid.groupby(["Ano", "Mês"]).agg(
        **{
            "Casos Totais": ("Casos Acumulados", "max"),
            "Óbitos Totais": ("Óbitos Acumulados", "max"),
            "Soma de Novos Casos": ("Novos Casos", "sum"),
            "Média de Novos Casos (7d)": ("Média Móvel (7 dias)", "mean")
        }
    ).reset_index()

    # Junta PIB (só por ano, mesmo valor para todos os meses daquele ano)
    final = covid_monthly.merge(pib, on="Ano", how="left")

    # Salva
    out_file = OUT / "indicadores_covid_pib.csv"
    final.to_csv(out_file, index=False)
    print("✅ Arquivo salvo em:", out_file)

if __name__ == "__main__":
    main()
