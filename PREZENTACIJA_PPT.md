# 🎵 SPOTIFY ANALIZA - PREZENTACIJA ZA PPT

**Avtor:** Nino Lisjak  
**Datum:** Januar 2026  
**Projekt:** Spotify Success Dynamics Analysis

---

## 📋 STRUKTURA PREZENTACIJE (15-20 minut)

---

# SLIDE 1: NASLOVNICA

```
🎵 SPOTIFY: PLATFORMA ODKRIVANJA ALI UTRJEVANJA?

Analiza dinamike uspeha na streaming platformi

Nino Lisjak
Januar 2026

[Slika: Spotify logo + glasben val / vizualizacija]
```

---

# SLIDE 2: KONTEKST IN MOTIVACIJA

```
📊 ZAKAJ SPOTIFY?

• 600+ MILIJONOV aktivnih uporabnikov
• Dominantna platforma za distribucijo glasbe
• Kompleksni algoritmi za priporočanje vsebine
• Ključno vprašanje za celotno industrijo

🎯 RELEVANTNOST:
┌─────────────────────────────────────────────┐
│ • Za izvajalce: Strategije za preboj       │
│ • Za založbe: Investicijske odločitve      │
│ • Za regulatorje: Tržna koncentracija      │
│ • Za platformo: Transparentnost algoritmov │
└─────────────────────────────────────────────┘
```

---

# SLIDE 3: GLAVNO RAZISKOVALNO VPRAŠANJE

```
❓ CENTRALNO VPRAŠANJE

╔══════════════════════════════════════════════════════════════╗
║  "Ali Spotify omogoča vstop NOVIH izvajalcev v vrh          ║
║   popularnosti ali utrjuje že OBSTOJEČE uspešne izvajalce?" ║
╚══════════════════════════════════════════════════════════════╝

           🚪                    🏆
    DEMOKRATIZATOR        vs.    GATEKEEPER
    (Odprt vstop)               (Zaprta elita)
```

---

# SLIDE 4: OSEM RAZISKOVALNIH HIPOTEZ

```
🔬 8 PODVPRAŠANJ (4 TEMELJNE + 4 RAZŠIRITVE)

TEMELJNE (H1-H4):
┌──────────────────────────────────────────────────────────┐
│ H1: BARRIER-TO-ENTRY → Ali se ovire povečujejo?         │
│ H2: RETENTION → Ali uspešni ostanejo uspešni?           │
│ H3: CONCENTRATION → Ali se uspeh koncentrira?           │
│ H4: SURVIVAL → Koliko časa trajajo kariere?             │
└──────────────────────────────────────────────────────────┘

RAZŠIRITVE (H5-H8):
┌──────────────────────────────────────────────────────────┐
│ H5: FIRST-HIT MOMENTUM → Prvi hit odpre vrata?          │
│ H6: CAREER VELOCITY → Hitrost preboja napoveduje?       │
│ H7: COMEBACK → Vrnitev po zatišju možna?                │
│ H8: MULTI-TRACK → Več skladb = več možnosti?            │
└──────────────────────────────────────────────────────────┘
```

---

# SLIDE 5: PODATKI IN METODOLOGIJA

```
📊 PODATKOVNI VIRI

┌────────────────────────────────────────────┐
│ DATASET:                                   │
│ • 586,671 skladb                          │
│ • 70,986 izvajalcev                       │
│ • Obdobje: 1922 - 2021 (100 let glasbe!)  │
│ • Ključna metrika: POPULARITY (0-100)     │
└────────────────────────────────────────────┘

🔧 METODOLOGIJA:
• Čiščenje in standardizacija podatkov
• Feature engineering (temporal features)
• Statistični testi (Mann-Kendall, Kruskal-Wallis)
• Machine Learning (PCA, K-Means, Logistična regresija)
• Survival analiza (Kaplan-Meier)

🆕 API ENRICHMENT:
• Spotify API (real-time popularity, playlists)
• MusicBrainz API (geografija izvajalcev)
```

---

# SLIDE 6: H1 - BARRIER-TO-ENTRY REZULTATI

```
📈 H1: ALI SE VSTOPNE OVIRE POVEČUJEJO?

[GRAF: Line chart - P90/P50 ratio skozi leta]

┌────────────────────────────────────────────┐
│ UGOTOVITEV:                                │
│                                            │
│ P90/P50 ratio: 1.72 → 1.58 (-8%)          │
│ Trend: PADAJOČ (Mann-Kendall p < 0.01)    │
│                                            │
│ ➡️ OVIRE SE ZNIŽUJEJO, NE POVEČUJEJO!     │
└────────────────────────────────────────────┘

✅ H1 ZAVRNJENA - Vstop je postal LAŽJI
```

---

# SLIDE 7: H2 - RETENTION REZULTATI

```
📊 H2: ALI USPEŠNI OSTANEJO USPEŠNI?

[GRAF: Retention matrix / Transition probabilities]

┌────────────────────────────────────────────────────┐
│ VERJETNOST OHRANITVE USPEHA:                      │
│                                                    │
│ • Uspešen → Uspešen:     34% (P(stay|success))    │
│ • Neuspešen → Neuspešen: 92% (lock-in effect)     │
│ • Razmerje:              4.3x PREDNOST za uspešne │
└────────────────────────────────────────────────────┘

🔑 KLJUČNA UGOTOVITEV:
"Enkrat uspešen = 4.3x lažje ostanek"
"Enkrat neuspešen = 92% verjetnost padca"

⚠️ H2 POTRJENA - "Rich-get-richer" dinamika OBSTAJA
```

---

# SLIDE 8: H3 - KONCENTRACIJA REZULTATI

```
📊 H3: ALI SE USPEH KONCENTRIRA?

[GRAF: Lorenz curve + Gini koeficient skozi čas]

┌────────────────────────────────────────────────────┐
│ GINI KOEFICIENT POPULARNOSTI:                     │
│                                                    │
│ 1990s: 0.42                                       │
│ 2000s: 0.45                                       │
│ 2010s: 0.48                                       │
│ 2020s: 0.47 (stabilizacija!)                      │
│                                                    │
│ Trend: RAHLO NARAŠČAJOČ, nato STABILIZACIJA       │
└────────────────────────────────────────────────────┘

⚖️ H3 DELNO POTRJENA - Koncentracija visoka, a STABILNA
   (Winner-take-all, ampak ni ekstremno naraščanje)
```

---

# SLIDE 9: H4 - SURVIVAL REZULTATI

```
📈 H4: KOLIKO ČASA TRAJAJO KARIERE?

[GRAF: Kaplan-Meier survival curves po kohortah]

┌────────────────────────────────────────────────────┐
│ MEDIANA PREŽIVETJA V TOP 25%:                     │
│                                                    │
│ 1980s kohorta: 3.2 leta                           │
│ 1990s kohorta: 2.8 leta                           │
│ 2000s kohorta: 2.1 leta                           │
│ 2010s kohorta: 1.4 leta  ⬇️                       │
│                                                    │
│ 84% izvajalcev izpade v PRVEM LETU!              │
│ Le 2% ohranja uspeh 5+ let                        │
└────────────────────────────────────────────────────┘

✅ H4 POTRJENA - Kariere se KRAJŠAJO
   Log-rank test: p < 0.001 (statistično značilno)
```

---

# SLIDE 10: API ENRICHMENT - PLATFORM DEPENDENCY

```
🆕 ALI JE SPOTIFY GATEKEEPER?

[GRAF: Platform vs Organic Reach pie chart]

┌────────────────────────────────────────────────────┐
│ KLJUČNE UGOTOVITVE:                               │
│                                                    │
│ Platform dependency ratio:    1.8%                │
│ Organic reach:               98.2%                │
│                                                    │
│ Korelacija platform ↔ popularity: r = -0.076     │
│ (Platform podpora NI povezana z uspehom!)         │
│                                                    │
│ 100% top artists ima večinoma ORGANIC reach       │
└────────────────────────────────────────────────────┘

✅ SPOTIFY JE DEMOKRATIZATOR, NE GATEKEEPER
   Organski uspeh je MOŽEN brez platform podpore
```

---

# SLIDE 11: GEOGRAFSKA ANALIZA

```
🌍 GEOGRAFSKA DISTRIBUCIJA USPEHA

[GRAF: World map z označenimi državami]

┌────────────────────────────────────────────────────┐
│ TOP DRŽAVE MED USPEŠNIMI:                         │
│                                                    │
│ 🇨🇦 Kanada (CA):     95.0 avg popularity         │
│ 🇺🇸 ZDA (US):        86.0 avg popularity         │
│ 🇦🇺 Avstralija (AU): 62.0 avg popularity         │
│                                                    │
│ CA/US = 80% vseh top artists                      │
│ Razmerje CA vs AU: 1.53x                          │
└────────────────────────────────────────────────────┘

⚠️ GEOGRAFSKA PREDNOST OBSTAJA
   Ampak NI absolutna ovira - tudi non-US artists uspejo
   (Primer: Masked Wolf iz Avstralije)
```

---

# SLIDE 12: DODATNE HIPOTEZE H5-H8

```
🔬 DODATNE ANALIZE - MOMENTUM EFEKTI

┌────────────────────────────────────────────────────────────┐
│ H5: FIRST-HIT MOMENTUM                                    │
│     → Ali prvi hit odpre vrata naslednjim?                │
│     ✅ POTRJENA: P(hit2|hit1) = 67% vs baseline 34%       │
│        Prvi uspeh PODVOJI verjetnost naslednjega!          │
├────────────────────────────────────────────────────────────┤
│ H6: CAREER VELOCITY                                        │
│     → Ali hitrost preboja napoveduje dolžino kariere?     │
│     ✅ POTRJENA: Hitri preboj = 2.4x daljša kariera       │
│        (≤2 leti do prvega hita vs >5 let)                 │
├────────────────────────────────────────────────────────────┤
│ H7: COMEBACK FEASIBILITY                                   │
│     → Ali je comeback po zatišju možen?                   │
│     ⚖️ DELNO: P(comeback|gap≥3 let) = 45%                │
│        Možen, ampak verjetnost pada z dolžino zatišja     │
├────────────────────────────────────────────────────────────┤
│ H8: MULTI-TRACK STRATEGY                                   │
│     → Ali več skladb = večja verjetnost uspeha?           │
│     ✅ POTRJENA: ρ = 0.23 (p < 0.001)                     │
│        Več poskusov = več možnosti za uspeh               │
└────────────────────────────────────────────────────────────┘
```

---

# SLIDE 13: 5 TIPOV IZVAJALCEV (CLUSTERING)

```
🎭 TIPOLOGIJA IZVAJALCEV (K-Means Clustering)

[GRAF: PCA 2D scatter plot z 5 clustri]

┌──────────────────────────────────────────────────────────┐
│ 5 PROFILOV IZVAJALCEV:                                  │
│                                                          │
│ ⭐ ZVEZDE (8%)                                           │
│    Visoka popularnost, veliki katalogi, dolge kariere   │
│                                                          │
│ 📈 HITRI VZPON (15%)                                    │
│    Visok peak, kratka kariera, viralni hiti            │
│                                                          │
│ 🎸 NIŠNI PRODUCENTI (22%)                              │
│    Nizka popularnost, veliki katalogi, stabilnost      │
│                                                          │
│ 📊 KONZISTENTNI (35%)                                   │
│    Stabilna srednja popularnost                         │
│                                                          │
│ 🎲 ONE-HIT WONDERS (20%)                               │
│    Enkraten uspeh, hitri izpad                          │
└──────────────────────────────────────────────────────────┘
```

---

# SLIDE 14: NAPOVEDNO MODELIRANJE

```
🤖 LOGISTIČNA REGRESIJA - NAPOVED USPEHA

[GRAF: ROC Curve + Feature Importance]

┌────────────────────────────────────────────────────┐
│ MODEL PERFORMANCE:                                 │
│                                                    │
│ • Accuracy:  85%                                  │
│ • ROC AUC:   0.92 (odlično!)                      │
│ • Precision: 0.83                                 │
│ • Recall:    0.87                                 │
└────────────────────────────────────────────────────┘

🔑 NAJPOMEMBNEJŠI FAKTORJI:
1. artist_avg_pop (povprečna popularnost) - 35%
2. artist_max_pop (maksimalna popularnost) - 28%
3. artist_track_count (število skladb) - 15%
4. release_year (leto izdaje) - 12%
5. explicit (eksplicitna vsebina) - 10%
```

---

# SLIDE 15: WHAT-IF SIMULACIJA

```
🎮 WHAT-IF SCENARIJI

[GRAF: 3 scenariji z verjetnostmi]

┌────────────────────────────────────────────────────────────┐
│ SCENARIJ           │ P(USPEH) │ P(TOP 10%) │ P(5+ LET)   │
├────────────────────┼──────────┼────────────┼─────────────┤
│ 🆕 NOV IZVAJALEC   │   35%    │     8%     │     2%      │
│ 📊 POVPREČEN       │   52%    │    22%     │    15%      │
│ ⭐ TOP IZVAJALEC   │   78%    │    55%     │    45%      │
└────────────────────────────────────────────────────────────┘

➡️ ZAKLJUČEK:
   "Zgodovina je najboljši napovedovalec uspeha"
   Top izvajalci imajo 2.2x večjo verjetnost uspeha
```

---

# SLIDE 16: POVZETEK HIPOTEZ

```
📋 REZULTATI VSEH 8 HIPOTEZ

╔════════════════════════════════════════════════════════════╗
║ HIPOTEZA                 │ STATUS      │ IMPLIKACIJA       ║
╠══════════════════════════╪═════════════╪═══════════════════╣
║ H1: Ovire naraščajo      │ ❌ ZAVRNJENA │ Vstop je LAŽJI   ║
╠══════════════════════════╪═════════════╪═══════════════════╣
║ H2: Rich-get-richer      │ ✅ POTRJENA │ 4.3x prednost    ║
╠══════════════════════════╪═════════════╪═══════════════════╣
║ H3: Koncentracija ↑      │ ⚖️ DELNO    │ Stabilna         ║
╠══════════════════════════╪═════════════╪═══════════════════╣
║ H4: Krajše kariere       │ ✅ POTRJENA │ 84% pade v 1 leto║
╠══════════════════════════╪═════════════╪═══════════════════╣
║ H5: First-hit momentum   │ ✅ POTRJENA │ 2x verjetnost    ║
╠══════════════════════════╪═════════════╪═══════════════════╣
║ H6: Career velocity      │ ✅ POTRJENA │ Hitrost napoveduje║
╠══════════════════════════╪═════════════╪═══════════════════╣
║ H7: Comeback možen       │ ⚖️ DELNO    │ 45% verjetnost   ║
╠══════════════════════════╪═════════════╪═══════════════════╣
║ H8: Mul7i-track strategija│ ✅ POTRJENA │ Več = več možnosti║
╠══════════════════════════╪═════════════╪═══════════════════╣
║ 🆕 Platform dependency   │ ❌ NIZKA    │ 98.2% organic    ║
╚════════════════════════════════════════════════════════════╝
```

---

# SLIDE 16: GLAVNA UGOTOVITEV

```
🎯 KLJUČNI ZAKLJUČEK

╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   SPOTIFY OMOGOČA VSTOP NOVIH IZVAJALCEV,                 ║
║   AMPAK HKRATI UTRJUJE ŽE USPEŠNE                         ║
║                                                            ║
║   🚪 VSTOP = LAHEK (nizke ovire, organski uspeh možen)   ║
║   🏆 OSTANEK = TEŽEK (4.3x prednost za uspešne)          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

             ┌─────────────────────────────────────┐
         8   │   MODEL "VRTLJIVIH VRAT"           │
             │   Vsakdo lahko VSTOPI,             │
             │   ampak le redki VZTRAJAJO         │
             └─────────────────────────────────────┘
```

---

# SLIDE 17: METAFORA

```
🌊 SPOTIFY KOT OCEAN

┌────────────────────────────────────────────────────────────┐
│                                                            │
│  🌊 OCEAN (Spotify platforma)                             │
│     • Odprt za vse - vsakdo lahko proba plavati           │
│     • Večina plava sama (98.2% organic)                   │
│                                                            │
│  🏊 PLAVALCI (Izvajalci)                                  │
│     • Nekateri plavajo v toplejših vodah (CA/US)          │
│     • Večina se utopi v prvem letu (84%)                  │
│     • Le najboljši preživijo 5+ let (2%)                  │
│                                                            │
│  🏖️ LIFEGUARDI (Editorial playlists)                     │
│     • Redko posegajo (1.8% vpliv)                         │
│     • Ni jasno, ali sploh pomagajo                        │
│                                                            │
│  ➡️ OCEAN JE ODPRT, AMPAK ZAHTEVEN                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

# SLIDE 19: PRAKTIČNE IMPLIKACIJE

```
💡 PRAKTIČNI NASVETI

ZA NOVE IZVAJA (glede na H5-H8):                            │
│    • Prvi hit je KLJUČEN - odpre vrata (H5: 2x efekt)    │
│    • Hitri preboj = daljša kariera (H6: 2.4x)            │
│    • Multi-track strategija - več poskusov (H8: ρ=0.23)  │
│    • Organic growth preko user playlists                   │
│    • Konsistentna prisotnost - comeback težak (H7: 45%)  │
│                                                            │
│ ❌ KAJ NE DELUJE:                                          │
│    • Čakanje na editorial playlist "rešitev"              │
│    • Dolgi odmori - comeback verjetnost pada (H7)        │
│    • Strategija "eden hit in počitek" - momentum se izgubi
│    • Odvisnost od platform algoritmov                      │
│    • Strategija "eden hit in počitek"                      │
└────────────────────────────────────────────────────────────┘

ZA ZALOŽBE:
┌────────────────────────────────────────────────────────────┐
│ • Investiraj v ORGANIC marketing (TikTok, Instagram)      │
│ • Diverzifikacija portfolija (več artists, manj risk)     │
│ • Prvi uspeh je ključen - odpre vrata za naslednje       │
└────────────────────────────────────────────────────────────┘
```

---

# SLIDE 20: OMEJITVE RAZISKAVE

```
⚠️ OMEJITVE IN PRIHODNJE DELO

METODOLOŠKE OMEJITVE:
┌────────────────────────────────────────────────────────────┐
│ • Popularity = SNAPSHOT (ni zgodovinski trend)            │
│ • Survivorship bias (samo skladbe na platformi)           │
│ • Majhen vzorec za API enrichment (n=10)                  │
│ • Korelacija ≠ Kavzalnost                                 │
└────────────────────────────────────────────────────────────┘

PRIHODNJE RAZISKAVE:
┌────────────────────────────────────────────────────────────┐
│ • Longitudinalni tracking (mesečni snapshots 1+ leto)     │
│ • Večji vzorec za API analizo (100+ artists)              │
│ • A/B testiranje playlist placement                        │
│ • Network analiza (collaboration effects)                  │
└────────────────────────────────────────────────────────────┘
```

---

# SLIDE 21: ZAKLJUČEK

```
🎓 ZAKLJUČEK

╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   "The data shows that Spotify is not the gatekeeper      ║
║    of success - USERS are."                               ║
║                                                            ║
║   🌊 SPOTIFY = ODPRT OCEAN, NE ZAPRT KLUB                 ║
║                                                            ║
║   ✅ 98.2% organic reach - platforma NE kontrolira uspeh  ║
║   ✅ Nizke vstopne ovire - vsakdo ima priložnost          ║
║   ⚠️ Visoka tekmovalnost - le 2% vztraja 5+ let           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

                    HVALA ZA POZORNOST!
                    
                    Vprašanja? 🎤
```

---

# DODATNI SLIDES (BACKUP)

## BACKUP SLIDE A: Tehnična implementacija

```
🔧 TEHNIČNA IMPLEMENTACIJA

UPORABLJENE KNJIŽNICE:
• pandas, numpy - manipulacija podatkov
• matplotlib, seaborn - statične vizualizacije
• plotly - interaktivne vizualizacije
• sklearn - ML modeli (PCA, K-Means, LogReg)
• lifelines - survival analiza
• scipy.stats - statistični testi

STRUKTURA PROJEKTA:
mosspotify/
├── spotify_analysis.ipynb (6700+ vrstic)
├── data/
│   ├── tracks.csv (586k vrstic)
│   └── api_enrichment/ (real-time podatki)
└── outputs/ (15+ vizualizacij)
```

## BACKUP SLIDE B: Dataset podrobnosti

```
📊 DATASET V ŠTEVILKAH

┌──────────────────────────────────────────┐
│ TRACKS.CSV                              │
│ • 586,671 skladb                        │
│ • 70,986 unikatnih izvajalcev          │
│ • 100 let glasbe (1922-2021)           │
│ • 25+ značilk na skladbo               │
│                                          │
│ API ENRICHMENT                          │
│ • 10 top artists (real-time tracking)   │
│ • Popularity: 62-100 range              │
│ • Followers: 800K - 97M range           │
│ • Geografija: CA, US, AU, UK           │
└──────────────────────────────────────────┘
```

## BACKUP SLIDE C: Vizualizacije overview

```
📈 KLJUČNE VIZUALIZACIJE V PROJEKTU

1. OSNOVNE:
   • Distribucija popularnosti (histogram)
   • Top izvajalci (bar chart)
   • Časovni trendi (line chart)

2. NAPREDNE:
   • Kaplan-Meier survival curves
   • Lorenz curve (koncentracija)
   • Transition matrix (retention)

3. OUT-OF-THE-BOX:
   • Radar grafi (profili izvajalcev)
   • Sankey diagram (prehodi)
   • 3D scatter plot
   • Interaktivni dashboard (Plotly)

4. API ENRICHMENT:
   • Platform dependency pie chart
   • Geografska mapa
   • Organic vs Platform scatter
```

---

# 📝 NAVODILA ZA OBLIKOVANJE PPT

## Splošna priporočila:

1. **Font**: Montserrat ali podoben clean sans-serif
2. **Barve**: 
   - Spotify zelena (#1DB954) za poudarke
   - Temna ozadja (#191414) za kontrast
   - Bela/svetlo siva za tekst
3. **Animacije**: Minimalne, profesionalne
4. **Grafi**: Izvozi iz notebook-a kot PNG (visoka resolucija)

## Za vsak slide:

- **Naslov**: Kratek, jedrnat (max 5 besed)
- **Vsebina**: Max 6 točk, max 6 besed na točko
- **Graf/Slika**: 1 vizualizacija na slide
- **Footer**: Številka slide-a + avtor

## Trajanje prezentacije:

| Sekcija | Slides | Čas |
|---------|--------|-----|
| Uvod (1-3) | 3 | 2 min |
| Metodologija (4-5) | 2 | 2 min |
| Rezultati H1-H4 (6-9) | 4 | 6 min |
| API Enrichment (10-11) | 2 | 2 min |
| H5-H8 & Modeliranje (12-15) | 4 | 4 min |
| Zaključek (16-21) | 6 | 5 min |
| **SKUPAJ** | **21** | **21 min** |

---

## 🎨 VIZUALNI ELEMENTI ZA PPT

### Ikone za uporabo:
- 🎵 Glasba/Spotify
- 📊 Podatki/Grafi
- 🔬 Raziskovanje
- 💡 Ugotovitve
- ⚠️ Omejitve
- ✅ Potrjeno
- ❌ Zavrnjeno
- 🎯 Cilj
- 🚪 Vstop
- 🏆 Uspeh
- 🌍 Geografija
- 🆕 Novo

### Barve za kodiranje:
- **Zelena (#1DB954)**: Pozitivni rezultati, potrjene hipoteze
- **Rdeča (#E53935)**: Negativni rezultati, zavrnjene hipoteze
- **Oranžna (#FF9800)**: Delno potrjeno, opozorila
- **Modra (#2196F3)**: Nevtralne informacije, podatki
- **Vijolična (#9C27B0)**: API enrichment, novo

---

*Dokument pripravljen za prenos v PowerPoint ali Google Slides*
*Vse vizualizacije so na voljo v outputs/ direktoriju*
