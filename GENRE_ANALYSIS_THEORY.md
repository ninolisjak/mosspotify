# 🎸 Žanrska Analiza - Teoretični Okvir

## Ozadje in Motivacija

### Spotify Genres API Status (Januar 2026)
⚠️ **Pomembno:** Spotify Genres API ni več aktivno vzdrževan:
- Novi izvajalci pogosto nimajo žanrov
- Obstoječi žanri niso več ažurirani
- Alternative: Last.fm, MusicBrainz, ročna kategorizacija

**Za ta projekt:** Uporabljamo obstoječe podatke iz `artists.csv` (26.3% coverage)

---

## 📊 Pregled Podatkov

### Dataset: artists.csv
| Metrika | Vrednost |
|---------|----------|
| Skupaj izvajalcev | 1,162,095 |
| Izvajalcev z žanri | 305,595 (26.3%) |
| Izvajalcev brez žanrov | 856,500 (73.7%) |
| Unikatnih žanrov | 5,366 |

### TOP 25 Žanrov po Frekvenci
```
dance pop                  572
pop                        568
rock                       564
electro house              559
classical performance      502
latin                      498
indie rock                 485
hip hop                    484
pop rap                    467
rap                        461
edm                        460
electropop                 458
french hip hop             453
latin rock                 446
modern rock                444
country rock               441
calming instrumental       441
pop edm                    431
lo-fi beats                426
modern alternative rock    420
post-teen pop              419
pop rock                   419
indie folk                 414
k-pop                      407
german hip hop             406
```

---

## 🔍 Ključna Ugotovitev: Žanri Top Izvajalcev

### Primerjava: Top 500 vs Vsi Izvajalci

| Žanr | Top 500 (%) | Vsi (%) | Ratio |
|------|-------------|---------|-------|
| pop | 7.68% | 0.12% | **63x** |
| dance pop | 5.28% | 0.12% | **43x** |
| rap | 4.01% | 0.10% | **41x** |
| pop rap | 3.86% | 0.10% | **39x** |
| post-teen pop | 3.23% | 0.09% | **36x** |
| trap latino | 2.69% | 0.07% | **41x** |
| reggaeton | 2.20% | 0.06% | **40x** |

**Interpretacija:** Pop, Rap, Latin so 40-60x bolj zastopani med top izvajalci kot v celotni populaciji. To nakazuje močan vpliv žanra na verjetnost uspeha.

---

## 💡 Argumenti Za in Proti

### ✅ Argumenti ZA Žanrsko Analizo

1. **Žanr kot napovedni faktor uspeha**
   - 63x večja verjetnost, da je top izvajalec "pop"
   - Izboljša napovedno moč modela (ROC AUC +0.02-0.04)

2. **Žanrsko-specifična survival analiza**
   - Pop: Hitri vzpon, hitri padec
   - Rock/Classical: Počasnejši vzpon, daljše preživetje

3. **Žanrske dinamike skozi čas**
   - Hip hop raste od 2010+
   - Rock pada od 2000+

4. **Barrier-to-entry po žanrih**
   - Electronic: Nizke ovire (produkcija doma)
   - Classical: Visoke ovire (konservatorij)

### ⚠️ Omejitve

1. **73.7% izvajalcev NIMA žanra**
   - Selection bias: Bolj popularni verjetno imajo žanr

2. **Multi-label problem**
   - Povprečno 2-4 žanri na izvajalca
   - Potrebna strategija: primary genre, all genres, embedding

3. **Nekonzistentna taksonomija**
   - 5,366 žanrov je preveč
   - Potrebna konsolidacija v ~10-15 meta-žanrov

4. **Vzročnost ni jasna**
   - Ali izvajalec postane uspešen ZARADI žanra?
   - Ali uspešni izvajalci dobijo "pop" tag ZATO KER so uspešni?

---

## 🎯 Strategija Implementacije

### Meta-Genre Mapiranje

```python
META_GENRES = {
    'pop': ['pop', 'dance pop', 'electropop', 'post-teen pop', 'pop rock', 'pop rap', 'pop edm'],
    'hip hop': ['hip hop', 'rap', 'trap', 'underground hip hop', 'southern hip hop', 'melodic rap'],
    'rock': ['rock', 'indie rock', 'modern rock', 'alternative rock', 'pop rock', 'classic rock'],
    'electronic': ['edm', 'electro house', 'house', 'techno', 'trance', 'dubstep'],
    'latin': ['latin', 'reggaeton', 'latin pop', 'trap latino', 'latin rock'],
    'r&b': ['r&b', 'urban contemporary', 'neo soul', 'contemporary r&b'],
    'country': ['country', 'country rock', 'contemporary country', 'country pop'],
    'classical': ['classical', 'classical performance', 'opera', 'orchestral'],
    'indie': ['indie', 'indie rock', 'indie folk', 'indie pop'],
    'other': []  # Vse ostalo
}
```

---

## 📈 Pričakovani Rezultati

### Glavne Hipoteze
- **Pop/Hip-hop:** Krajše preživetje, višja vrhunska popularnost
- **Rock/Classical:** Daljše preživetje, nižja vrhunska popularnost
- **Electronic/EDM:** Najnižje vstopne ovire
- **Latin:** Najhitreje rastoči žanr v zadnjem desetletju

### ROI Ocena
| Metrika | Vrednost |
|---------|----------|
| Čas implementacije | ~9 ur |
| Izboljšava modela | +0.02-0.04 ROC AUC |
| Nova raziskovalna vprašanja | 4 |
| Nove vizualizacije | 8-10 grafov |
| Akademska vrednost | VISOKA |

---

## 📚 Reference

- Spotify for Developers API Documentation
- MusicBrainz API
- Dataset: Kaggle Spotify Dataset (1.2M+ tracks)
