# 📊 Metodološki Okvir Projekta

## Vsebina
1. [Raziskovalna vprašanja](#raziskovalna-vprašanja)
2. [Podatkovni viri](#podatkovni-viri)
3. [Struktura notebooka](#struktura-notebooka)
4. [Načrt vizualizacij](#načrt-vizualizacij)
5. [Metodološki okvir](#metodološki-okvir)
6. [Survival analiza - teoretično ozadje](#survival-analiza)

---

## Raziskovalna vprašanja

### Glavno raziskovalno vprašanje (GRV)

> **Ali platforma Spotify skozi čas omogoča vstop novih izvajalcev v vrh popularnosti ali predvsem utrjuje že obstoječe uspešne izvajalce?**

### Podvprašanja in hipoteze

| # | Podvprašanje | Hipoteza |
|---|--------------|----------|
| **H1** | Ali se ovire za dosego visoke popularnosti povečujejo? | P90/mediana se skozi čas povečuje |
| **H2** | Kako verjetno je, da uspešen izvajalec ostane uspešen? | P(uspeh t+1 \| uspeh t) je višja za uveljavljene |
| **H3** | Ali se uspeh koncentrira pri manjšem številu izvajalcev? | Gini koeficient in delež top izvajalcev naraščata |
| **H4** | Koliko časa povprečen izvajalec ostane relevanten? | Novejše kohorte imajo krajši mediani čas |

---

## Podatkovni viri

### Primarni vir: Kaggle Spotify Dataset

| Datoteka | Velikost | Opis |
|----------|----------|------|
| `dataset.csv` | ~19 MB | Glavna datoteka s skladbami (~114k vrstic) |
| `tracks.csv` | ~106 MB | Razširjena datoteka skladb |
| `artists.csv` | ~62 MB | Podatki o izvajalcih |
| `dict_artists.json` | ~317 MB | Slovar izvajalcev |

### Ključne spremenljivke

| Spremenljivka | Tip | Vloga |
|---------------|-----|-------|
| `popularity` | int (0-100) | **Ciljna spremenljivka** |
| `release_date` | date | Časovna dimenzija |
| `artists` | string | Ključna spremenljivka |
| `explicit` | bool | Kontrolna |
| `track_genre` | string | Kontrolna |

### Omejitve podatkov

1. **Popularnost je dinamična** - snapshot, ne zgodovinski trend
2. **Survivorship bias** - samo skladbe ki so še na platformi
3. **Selekcijska pristranskost** - ni naključni vzorec
4. **Manjkajoči podatki** - nekateri izvajalci nimajo vseh metapodatkov

---

## Struktura notebooka

```
📁 SPOTIFY ANALYSIS NOTEBOOK
│
├── 1. UVOD IN RAZISKOVALNI OKVIR
│   ├── 1.1 Tema in motivacija
│   └── 1.2 Hipoteze (H1-H12)
│
├── 2. PODATKI IN PRIPRAVA
│   ├── 2.1-2.4 Nalaganje, čiščenje, feature engineering
│   └── 2.5 API Enrichment (Spotify API, MusicBrainz)
│
├── 3. EDA (Exploratory Data Analysis)
│   ├── Opisna statistika
│   └── Vizualizacije distribucij
│
├── 4-7. PROBLEMSKI SKLOPI
│   ├── 4. Barrier-to-entry (H1)
│   ├── 5. Retention (H2)
│   ├── 6. Concentration (H3)
│   └── 7. Survival (H4)
│
├── 8. DODATNE HIPOTEZE (H5-H8)
│   ├── H5: Explicit content
│   ├── H6: Prolificnost
│   ├── H7: Genre gatekeeping
│   └── H8: Audio features
│
├── 9. ŽANRSKA ANALIZA (H9-H12)
│   ├── H9: Žanrska koncentracija
│   ├── H10: Žanrski trendi
│   ├── H11: Žanrska preživetja
│   └── H12: Žanrske ovire
│
├── 10. MODELIRANJE
│   ├── PCA, K-Means Clustering
│   ├── Logistična regresija
│   └── Feature importance
│
├── 11. SIMULACIJE IN OBČUTLJIVOST
│   └── What-If analiza, robustnost
│
└── 12. ZAKLJUČEK
    └── Povzetek vseh 12 hipotez
```

---

## Načrt vizualizacij

### Enostavne vizualizacije
- Histogrami popularnosti
- Bar charts (top izvajalci)
- Line charts (trendi)
- Box plots (po žanrih)

### Kompleksne vizualizacije
- Violin plots (distribucije)
- Heatmaps (prehodne matrike)
- Lorenz curves (koncentracija)
- Kaplan-Meier curves (preživetje)

### Večdimenzionalne vizualizacije
- Faceted line charts
- Sankey diagrami
- 3D scatter plots
- Radar grafi

### Interaktivne vizualizacije (Plotly)
- Dashboard z dropdown menus
- Hover tooltips
- Drill-down od agregatov do posameznikov

---

## Metodološki okvir

### Definicije ključnih konceptov

| Koncept | Operacionalna definicija | Prag |
|---------|--------------------------|------|
| Uspešen izvajalec | Vsaj 1 skladba v top X% | X = 10 (primarno) |
| Nov izvajalec | Prvo leto s skladbo | min(release_year) |
| Uveljavljen | ≥3 leta od prve skladbe | tenure ≥ 3 |
| "Izpad" | Prvo leto brez top X% | - |

### Statistične metode

| Metoda | Uporaba |
|--------|---------|
| Percentilna normalizacija | Primerjava med leti |
| Gini koeficient | Merjenje neenakosti |
| Kaplan-Meier | Survival analiza |
| Logistična regresija | Napovedni model |
| Chi-square test | Testiranje neodvisnosti |
| Mann-Kendall | Trend test |
| Bootstrap | Intervali zaupanja |

### Robustnost rezultatov

Vsak rezultat validiran z:
1. Alternativnimi pragi (top 5%, 10%, 20%)
2. Bootstrap CI (95%, 1000 iteracij)
3. Podvzorčenjem po žanrih
4. Časovnimi okni

---

## Survival analiza

### Teoretično ozadje

**Survival analiza** je statistična metoda za analizo časa do nekega dogodka.

Uporaba v tem projektu:
- **Dogodek** = izpad iz top X% popularnosti
- **Čas** = leta od prvega uspeha
- **Cenzura** = izvajalec je še aktiven

### Ključni koncepti

1. **Survival function S(t)** = P(T > t) - verjetnost preživetja do časa t
2. **Hazard function h(t)** = instantana stopnja dogodka ob času t
3. **Kaplan-Meier estimator** - neparametrična ocena S(t)
4. **Log-rank test** - primerjava krivulj med skupinami

### Interpretacija rezultatov

- **Mediana preživetja** = čas, ko 50% izvajalcev izpade
- **95% CI** = interval zaupanja za oceno
- **p-vrednost** (log-rank) = statistična značilnost razlike med skupinami

---

## Časovnica projekta

| Teden | Faza | Aktivnosti |
|-------|------|------------|
| 1 | Zasnova | Definicija problema, hipoteze |
| 2 | Podatki | Nalaganje, čiščenje, feature engineering |
| 3 | EDA | Opisna statistika, osnovne vizualizacije |
| 4 | Vizualizacije | Kompleksne in interaktivne vizualizacije |
| 5 | Analiza I | Barrier, Concentration, literatura |
| 6 | Analiza II | Retention, Survival, model, zaključek |
