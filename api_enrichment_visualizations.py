"""
🎵 SPOTIFY API ENRICHMENT - VIZUALIZACIJE ZA NOVE HIPOTEZE
============================================================

Ta skripta vsebuje vse vizualizacije za API enrichment analize:
1. Platform Dependency - ali je Spotify podpora potrebna za uspeh?
2. Organic vs Platform-driven - kakšen je vpliv kuracije?
3. Geografska analiza - od kod prihajajo uspešni artists?
4. Generacijska analiza - kako starost vpliva na uspeh?
5. Network analiza - playlist overlaps in doseg

Avtor: Nino Lisjak
Datum: Januar 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Nastavi stil
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# =============================================================================
# NALAGANJE PODATKOV
# =============================================================================

print("="*80)
print("📊 NALAGANJE API ENRICHMENT PODATKOV")
print("="*80)

# Naloži enriched master dataset
enriched = pd.read_csv('data/api_enrichment/enriched_artists_master.csv')
playlist = pd.read_csv('data/api_enrichment/playlist_analysis_20260110.csv')

print(f"\n✅ Naloženo {len(enriched)} artists iz enriched_artists_master.csv")
print(f"✅ Naloženo {len(playlist)} artists iz playlist_analysis.csv")

# Združi podatke
df_api = enriched.merge(playlist, on='artist_name', how='left', suffixes=('', '_pl'))
df_api['platform_ratio'] = df_api['platform_ratio'].fillna(0)
df_api['organic_ratio'] = df_api['organic_ratio'].fillna(0)

print(f"\n📋 Stolpci v združenem datasetu:")
print(df_api.columns.tolist())

# =============================================================================
# HIPOTEZA 1: PLATFORM DEPENDENCY - ALI JE SPOTIFY PODPORA POTREBNA?
# =============================================================================

print("\n" + "="*80)
print("📊 HIPOTEZA 1: PLATFORM DEPENDENCY ANALIZA")
print("="*80)

# Definiraj kategorije
df_api['success_category'] = pd.cut(
    df_api['popularity'], 
    bins=[0, 50, 70, 100], 
    labels=['📉 Nizka', '📊 Srednja', '⭐ Visoka']
)

df_api['platform_category'] = pd.cut(
    df_api['platform_ratio'],
    bins=[-0.1, 0.01, 0.1, 1.0],
    labels=['🌱 Organic', '🎯 Hibrid', '🎪 Platform-driven']
)

# Statistika
print("\n📋 Distribucija po kategorijah:")
print(df_api.groupby(['success_category', 'platform_category']).size().unstack(fill_value=0))

# Korelacijska analiza
corr_platform_pop = df_api[['platform_ratio', 'organic_ratio', 'popularity', 'followers']].corr()
print("\n📈 Korelacijska matrika:")
print(corr_platform_pop)

# =============================================================================
# VIZ 1.1: PLATFORM DEPENDENCY VS POPULARITY - SCATTER PLOT
# =============================================================================

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# Graf 1: Platform ratio vs Popularity
ax1 = fig.add_subplot(gs[0, 0])
scatter = ax1.scatter(
    df_api['platform_ratio'], 
    df_api['popularity'],
    c=df_api['followers'],
    s=df_api['followers'] / 500000,
    alpha=0.6,
    cmap='viridis',
    edgecolors='black',
    linewidth=0.5
)
ax1.set_xlabel('Platform Dependency Ratio', fontsize=12, fontweight='bold')
ax1.set_ylabel('Popularity Score', fontsize=12, fontweight='bold')
ax1.set_title('🎪 Platform Dependency vs Uspešnost\n(Velikost = Followers)', 
              fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Dodaj trend linijo
z = np.polyfit(df_api['platform_ratio'].dropna(), 
               df_api['popularity'].dropna(), 1)
p = np.poly1d(z)
ax1.plot(df_api['platform_ratio'].sort_values(), 
         p(df_api['platform_ratio'].sort_values()), 
         "r--", alpha=0.8, linewidth=2, 
         label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}')
ax1.legend()

# Korelacija
r, p_val = stats.pearsonr(df_api['platform_ratio'].dropna(), 
                           df_api['popularity'].dropna())
ax1.text(0.95, 0.05, f'r = {r:.3f}\np = {p_val:.3f}', 
         transform=ax1.transAxes, 
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
         ha='right', fontsize=10)

# Graf 2: Organic ratio vs Followers
ax2 = fig.add_subplot(gs[0, 1])
scatter2 = ax2.scatter(
    df_api['organic_ratio'],
    df_api['followers'],
    c=df_api['popularity'],
    s=100,
    alpha=0.6,
    cmap='RdYlGn',
    edgecolors='black',
    linewidth=0.5
)
ax2.set_xlabel('Organic Reach Ratio', fontsize=12, fontweight='bold')
ax2.set_ylabel('Followers', fontsize=12, fontweight='bold')
ax2.set_title('🌱 Organic Reach vs Followers\n(Barvna skala = Popularity)', 
              fontsize=14, fontweight='bold')
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3)

# Korelacija
r2, p_val2 = stats.pearsonr(df_api['organic_ratio'].dropna(), 
                            df_api['followers'].dropna())
ax2.text(0.95, 0.95, f'r = {r2:.3f}\np = {p_val2:.3f}', 
         transform=ax2.transAxes,
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
         ha='right', va='top', fontsize=10)

# Graf 3: Distribucija Platform Dependency po Success kategoresume categories
ax3 = fig.add_subplot(gs[1, 0])
success_cats = df_api.groupby('success_category')['platform_ratio'].apply(list)
positions = range(len(success_cats))
bp = ax3.boxplot([cat for cat in success_cats], 
                  labels=success_cats.index,
                  patch_artist=True,
                  showmeans=True,
                  meanprops=dict(marker='D', markerfacecolor='red', markersize=8))

# Barvanje boxplotov
colors = ['#E74C3C', '#F39C12', '#27AE60']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

ax3.set_xlabel('Kategorija uspešnosti', fontsize=12, fontweight='bold')
ax3.set_ylabel('Platform Dependency Ratio', fontsize=12, fontweight='bold')
ax3.set_title('📊 Platform Dependency po Kategorijah Uspešnosti', 
              fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# Dodaj statistiko
for i, (cat, vals) in enumerate(success_cats.items()):
    median_val = np.median(vals)
    ax3.text(i+1, median_val, f'{median_val:.3f}', 
             ha='center', va='bottom', fontsize=9, fontweight='bold')

# Graf 4: Pie chart - Organic vs Platform vs Hybrid
ax4 = fig.add_subplot(gs[1, 1])
platform_dist = df_api['platform_category'].value_counts()
colors_pie = ['#27AE60', '#F39C12', '#E74C3C']
wedges, texts, autotexts = ax4.pie(
    platform_dist.values,
    labels=platform_dist.index,
    colors=colors_pie,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 12, 'fontweight': 'bold'}
)
ax4.set_title('🎯 Distribucija Artists po Tipu Podpore', 
              fontsize=14, fontweight='bold', pad=20)

# Dodaj legenddo z absolutnimi številkami
legend_labels = [f'{label}: {count} artists' 
                for label, count in zip(platform_dist.index, platform_dist.values)]
ax4.legend(legend_labels, loc='upper left', bbox_to_anchor=(0.85, 0.1))

plt.savefig('outputs/viz_platform_dependency_analysis.png', dpi=300, bbox_inches='tight')
print("\n✅ Vizualizacija 1 shranjena: outputs/viz_platform_dependency_analysis.png")
plt.show()

# =============================================================================
# VIZ 1.2: INTERAKTIVNI SCATTER - PLOTLY
# =============================================================================

fig_interactive = px.scatter(
    df_api,
    x='platform_ratio',
    y='popularity',
    size='followers',
    color='success_category',
    hover_data=['artist_name', 'followers', 'total_reach', 'country'],
    title='🎪 Interaktivna Analiza: Platform Dependency vs Uspešnost',
    labels={
        'platform_ratio': 'Platform Dependency Ratio',
        'popularity': 'Popularity Score'
    },
    color_discrete_map={
        '📉 Nizka': '#E74C3C',
        '📊 Srednja': '#F39C12',
        '⭐ Visoka': '#27AE60'
    }
)

fig_interactive.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')))
fig_interactive.update_layout(
    height=600,
    font=dict(size=12),
    hovermode='closest'
)

fig_interactive.write_html('outputs/viz_platform_dependency_interactive.html')
print("✅ Interaktivna vizualizacija: outputs/viz_platform_dependency_interactive.html")

# =============================================================================
# HIPOTEZA 2: GEOGRAFSKA ANALIZA - USPEH PO DRŽAVAH
# =============================================================================

print("\n" + "="*80)
print("📊 HIPOTEZA 2: GEOGRAFSKA DIMENZIJA USPEHA")
print("="*80)

# Filtriraj samo artists z znanimi državami
df_geo = df_api[df_api['country'].notna()].copy()

print(f"\n🌍 Artists z geografskimi podatki: {len(df_geo)}")
print(f"\n📋 Distribucija po državah:")
print(df_geo['country'].value_counts())

# Agregiraj po državah
geo_stats = df_geo.groupby('country').agg({
    'popularity': ['mean', 'median', 'max', 'count'],
    'followers': ['mean', 'median', 'sum'],
    'platform_ratio': 'mean',
    'organic_ratio': 'mean'
}).round(2)

geo_stats.columns = ['pop_mean', 'pop_median', 'pop_max', 'artist_count',
                     'followers_mean', 'followers_median', 'followers_total',
                     'platform_ratio_avg', 'organic_ratio_avg']
geo_stats = geo_stats.reset_index()
geo_stats = geo_stats.sort_values('pop_mean', ascending=False)

print("\n📊 Statistika po državah:")
print(geo_stats.to_string(index=False))

# =============================================================================
# VIZ 2.1: GEOGRAFSKA ANALIZA - MULTI-PANEL
# =============================================================================

fig2 = plt.figure(figsize=(16, 12))
gs2 = fig2.add_gridspec(3, 2, hspace=0.35, wspace=0.3)

# Graf 1: Popularnost po državah (bar chart)
ax21 = fig2.add_subplot(gs2[0, :])
countries = geo_stats['country'].values
pop_means = geo_stats['pop_mean'].values
artist_counts = geo_stats['artist_count'].values

bars = ax21.bar(countries, pop_means, color='#1DB954', alpha=0.7, edgecolor='black', linewidth=1)
ax21.set_xlabel('Država', fontsize=12, fontweight='bold')
ax21.set_ylabel('Povprečna Popularity', fontsize=12, fontweight='bold')
ax21.set_title('🌍 Geografska Analiza: Povprečna Uspešnost po Državah\n(Višina stolpca = Popularity)', 
               fontsize=14, fontweight='bold')
ax21.grid(True, alpha=0.3, axis='y')

# Dodaj vrednosti in število artists
for bar, pop, count in zip(bars, pop_means, artist_counts):
    ax21.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
              f'{pop:.1f}\n({count} artists)',
              ha='center', va='bottom', fontsize=9, fontweight='bold')

# Graf 2: Followers po državah (horizontal bar)
ax22 = fig2.add_subplot(gs2[1, 0])
geo_sorted_followers = geo_stats.sort_values('followers_mean')
ax22.barh(geo_sorted_followers['country'], 
          geo_sorted_followers['followers_mean']/1e6,
          color='#3498DB', alpha=0.7, edgecolor='black')
ax22.set_xlabel('Povprečno št. Followers (milijoni)', fontsize=12, fontweight='bold')
ax22.set_ylabel('Država', fontsize=12, fontweight='bold')
ax22.set_title('👥 Povprečno Followers po Državah', fontsize=14, fontweight='bold')
ax22.grid(True, alpha=0.3, axis='x')

for i, (country, val) in enumerate(zip(geo_sorted_followers['country'], 
                                       geo_sorted_followers['followers_mean'])):
    ax22.text(val/1e6 + 1, i, f'{val/1e6:.1f}M', 
              va='center', fontsize=9, fontweight='bold')

# Graf 3: Platform dependency po državah
ax23 = fig2.add_subplot(gs2[1, 1])
x = np.arange(len(geo_stats))
width = 0.35

bars1 = ax23.bar(x - width/2, geo_stats['platform_ratio_avg'], 
                 width, label='Platform', color='#E74C3C', alpha=0.7)
bars2 = ax23.bar(x + width/2, geo_stats['organic_ratio_avg'], 
                 width, label='Organic', color='#27AE60', alpha=0.7)

ax23.set_xlabel('Država', fontsize=12, fontweight='bold')
ax23.set_ylabel('Povprečni Ratio', fontsize=12, fontweight='bold')
ax23.set_title('🎯 Platform vs Organic Reach po Državah', fontsize=14, fontweight='bold')
ax23.set_xticks(x)
ax23.set_xticklabels(geo_stats['country'])
ax23.legend()
ax23.grid(True, alpha=0.3, axis='y')

# Graf 4: Bubble chart - Popularity vs Followers by Country
ax24 = fig2.add_subplot(gs2[2, :])
colors_countries = plt.cm.Set3(np.linspace(0, 1, len(geo_stats)))

for i, (idx, row) in enumerate(geo_stats.iterrows()):
    ax24.scatter(row['followers_mean'], row['pop_mean'],
                s=row['artist_count']*200,
                alpha=0.6,
                color=colors_countries[i],
                edgecolors='black',
                linewidth=1,
                label=row['country'])
    ax24.text(row['followers_mean'], row['pop_mean'], row['country'],
             ha='center', va='center', fontsize=9, fontweight='bold')

ax24.set_xlabel('Povprečno Followers', fontsize=12, fontweight='bold')
ax24.set_ylabel('Povprečna Popularity', fontsize=12, fontweight='bold')
ax24.set_title('🎯 Bubble Chart: Popularity vs Followers by Country\n(Velikost = Število Artists)', 
               fontsize=14, fontweight='bold')
ax24.set_xscale('log')
ax24.grid(True, alpha=0.3)

plt.savefig('outputs/viz_geographic_analysis.png', dpi=300, bbox_inches='tight')
print("\n✅ Vizualizacija 2 shranjena: outputs/viz_geographic_analysis.png")
plt.show()

# =============================================================================
# VIZ 2.2: INTERAKTIVNA MAPA - CHOROPLETH (če imamo več podatkov)
# =============================================================================

# Pripravi podatke za mapo (ISO kode držav)
country_codes = {
    'CA': 'CAN', 'US': 'USA', 'AU': 'AUS', 'GB': 'GBR',
    'DE': 'DEU', 'FR': 'FRA', 'IT': 'ITA', 'ES': 'ESP'
}

geo_stats['country_code'] = geo_stats['country'].map(country_codes)
geo_stats = geo_stats[geo_stats['country_code'].notna()]

if len(geo_stats) >= 3:
    fig_map = px.choropleth(
        geo_stats,
        locations='country_code',
        color='pop_mean',
        hover_name='country',
        hover_data=['artist_count', 'followers_mean', 'platform_ratio_avg'],
        color_continuous_scale='RdYlGn',
        title='🌍 Globalna Distribucija Uspešnosti Artists',
        labels={'pop_mean': 'Povprečna Popularity'}
    )
    
    fig_map.update_layout(
        height=600,
        font=dict(size=12)
    )
    
    fig_map.write_html('outputs/viz_geographic_map.html')
    print("✅ Geografska mapa: outputs/viz_geographic_map.html")

# =============================================================================
# HIPOTEZA 3: PLAYLIST DIVERSITY - ORGANIC VS PLATFORM
# =============================================================================

print("\n" + "="*80)
print("📊 HIPOTEZA 3: PLAYLIST DIVERSITY ANALIZA")
print("="*80)

# Kategorije playlist dosega
df_api['playlist_category'] = 'Brez dosega'
df_api.loc[df_api['organic_reach'] > 0, 'playlist_category'] = '🌱 Organic Only'
df_api.loc[df_api['algorithmic_reach'] > 0, 'playlist_category'] = '🤖 Algorithm'
df_api.loc[df_api['editorial_reach'] > 0, 'playlist_category'] = '🎪 Editorial'
df_api.loc[(df_api['organic_reach'] > 0) & 
           (df_api['algorithmic_reach'] > 0), 'playlist_category'] = '🎯 Hybrid'

print("\n📋 Distribucija po playlist kategorijah:")
print(df_api['playlist_category'].value_counts())

# Povprečna uspešnost po kategorijah
playlist_success = df_api.groupby('playlist_category').agg({
    'popularity': ['mean', 'median', 'std'],
    'followers': ['mean', 'median'],
    'artist_name': 'count'
}).round(2)

print("\n📊 Uspešnost po playlist kategorijah:")
print(playlist_success)

# =============================================================================
# VIZ 3: PLAYLIST DIVERSITY VISUALIZATION
# =============================================================================

fig3, axes3 = plt.subplots(2, 2, figsize=(16, 12))

# Graf 1: Violin plot - Popularity po playlist kategorijah
ax31 = axes3[0, 0]
categories = df_api['playlist_category'].unique()
data_violins = [df_api[df_api['playlist_category'] == cat]['popularity'].dropna() 
                for cat in categories]

parts = ax31.violinplot(data_violins, positions=range(len(categories)), 
                        showmeans=True, showmedians=True)
ax31.set_xticks(range(len(categories)))
ax31.set_xticklabels(categories, rotation=15, ha='right')
ax31.set_ylabel('Popularity Score', fontsize=12, fontweight='bold')
ax31.set_title('🎵 Distribucija Popularnosti po Playlist Kategorijah', 
               fontsize=14, fontweight='bold')
ax31.grid(True, alpha=0.3, axis='y')

# Graf 2: Stacked bar - Reach composition
ax32 = axes3[0, 1]
reach_data = playlist[['editorial_reach', 'algorithmic_reach', 'organic_reach']].fillna(0)
reach_totals = reach_data.sum()

bars = ax32.bar(['Editorial', 'Algorithmic', 'Organic'], reach_totals,
                color=['#E74C3C', '#F39C12', '#27AE60'], alpha=0.7, edgecolor='black')
ax32.set_ylabel('Total Reach (summed)', fontsize=12, fontweight='bold')
ax32.set_title('📊 Skupni Reach po Tipu Playlista', fontsize=14, fontweight='bold')
ax32.grid(True, alpha=0.3, axis='y')

# Dodaj percentages
total_reach_sum = reach_totals.sum()
for bar, val in zip(bars, reach_totals):
    pct = val / total_reach_sum * 100
    ax32.text(bar.get_x() + bar.get_width()/2, bar.get_height() + reach_totals.max()*0.02,
              f'{val:,.0f}\n({pct:.1f}%)',
              ha='center', va='bottom', fontsize=10, fontweight='bold')

# Graf 3: Scatter - Organic reach vs Popularity
ax33 = axes3[1, 0]
scatter3 = ax33.scatter(df_api['organic_reach'], df_api['popularity'],
                       c=df_api['followers'], s=80, alpha=0.6,
                       cmap='viridis', edgecolors='black', linewidth=0.5)
ax33.set_xlabel('Organic Reach', fontsize=12, fontweight='bold')
ax33.set_ylabel('Popularity Score', fontsize=12, fontweight='bold')
ax33.set_title('🌱 Organic Reach vs Uspešnost', fontsize=14, fontweight='bold')
ax33.set_xscale('log')
ax33.grid(True, alpha=0.3)

# Korelacija
valid_mask = (df_api['organic_reach'] > 0) & df_api['popularity'].notna()
if valid_mask.sum() > 0:
    r3, p_val3 = stats.pearsonr(df_api[valid_mask]['organic_reach'], 
                                df_api[valid_mask]['popularity'])
    ax33.text(0.95, 0.05, f'r = {r3:.3f}\np = {p_val3:.3f}',
             transform=ax33.transAxes,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
             ha='right', fontsize=10)

# Graf 4: Heatmap - Korelacije
ax34 = axes3[1, 1]
corr_cols = ['editorial_reach', 'algorithmic_reach', 'organic_reach', 
             'popularity', 'followers', 'platform_ratio']
corr_matrix = df_api[corr_cols].corr()

sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdYlGn', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8},
            ax=ax34, vmin=-1, vmax=1)
ax34.set_title('🔥 Korelacijska Matrika: Reach Metrike', 
               fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('outputs/viz_playlist_diversity.png', dpi=300, bbox_inches='tight')
print("\n✅ Vizualizacija 3 shranjena: outputs/viz_playlist_diversity.png")
plt.show()

# =============================================================================
# SKUPNI DASHBOARD - INTERAKTIVNI
# =============================================================================

print("\n" + "="*80)
print("📊 USTVARJANJE INTERAKTIVNEGA DASHBOARDA")
print("="*80)

# Ustvari multi-subplot Plotly dashboard
fig_dashboard = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        '🎪 Platform Dependency vs Popularity',
        '🌍 Uspešnost po Državah',
        '🎯 Organic vs Platform Reach',
        '📊 Followers Distribution'
    ),
    specs=[[{'type': 'scatter'}, {'type': 'bar'}],
           [{'type': 'scatter'}, {'type': 'box'}]],
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

# Subplot 1: Platform dependency scatter
fig_dashboard.add_trace(
    go.Scatter(
        x=df_api['platform_ratio'],
        y=df_api['popularity'],
        mode='markers',
        marker=dict(
            size=df_api['followers']/1e6,
            color=df_api['popularity'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(x=0.46, len=0.4)
        ),
        text=df_api['artist_name'],
        name='Artists'
    ),
    row=1, col=1
)

# Subplot 2: Geo bar chart
fig_dashboard.add_trace(
    go.Bar(
        x=geo_stats['country'],
        y=geo_stats['pop_mean'],
        marker_color='#1DB954',
        name='Popularity',
        text=geo_stats['pop_mean'].round(1),
        textposition='outside'
    ),
    row=1, col=2
)

# Subplot 3: Organic vs Platform scatter
fig_dashboard.add_trace(
    go.Scatter(
        x=df_api['organic_ratio'],
        y=df_api['platform_ratio'],
        mode='markers',
        marker=dict(
            size=10,
            color=df_api['popularity'],
            colorscale='RdYlGn',
            showscale=False
        ),
        text=df_api['artist_name'],
        name='Artists'
    ),
    row=2, col=1
)

# Subplot 4: Box plot followers by success
for i, cat in enumerate(df_api['success_category'].dropna().unique()):
    fig_dashboard.add_trace(
        go.Box(
            y=df_api[df_api['success_category'] == cat]['followers'],
            name=str(cat),
            marker_color=['#E74C3C', '#F39C12', '#27AE60'][i]
        ),
        row=2, col=2
    )

# Update layout
fig_dashboard.update_xaxes(title_text="Platform Ratio", row=1, col=1)
fig_dashboard.update_yaxes(title_text="Popularity", row=1, col=1)
fig_dashboard.update_xaxes(title_text="Country", row=1, col=2)
fig_dashboard.update_yaxes(title_text="Avg Popularity", row=1, col=2)
fig_dashboard.update_xaxes(title_text="Organic Ratio", row=2, col=1)
fig_dashboard.update_yaxes(title_text="Platform Ratio", row=2, col=1)
fig_dashboard.update_yaxes(title_text="Followers (log scale)", type="log", row=2, col=2)

fig_dashboard.update_layout(
    height=900,
    title_text="🎵 API ENRICHMENT DASHBOARD - Celostni Pregled",
    title_font_size=18,
    showlegend=True,
    font=dict(size=11)
)

fig_dashboard.write_html('outputs/viz_api_enrichment_dashboard.html')
print("\n✅ Interaktivni dashboard: outputs/viz_api_enrichment_dashboard.html")

# =============================================================================
# ZAKLJUČEK - STATISTIČNI POVZETEK
# =============================================================================

print("\n" + "="*80)
print("📊 STATISTIČNI POVZETEK - API ENRICHMENT ANALIZE")
print("="*80)

# Korelacije
print("\n📈 KLJUČNE KORELACIJE:")
print(f"   • Platform ratio ↔ Popularity: r = {r:.3f} (p = {p_val:.3f})")
print(f"   • Organic ratio ↔ Followers: r = {r2:.3f} (p = {p_val2:.3f})")

# Platform dependency
platform_avg = df_api['platform_ratio'].mean()
organic_avg = df_api['organic_ratio'].mean()
print(f"\n🎯 PLATFORM DEPENDENCY:")
print(f"   • Povprečni platform ratio: {platform_avg:.3f} ({platform_avg*100:.1f}%)")
print(f"   • Povprečni organic ratio: {organic_avg:.3f} ({organic_avg*100:.1f}%)")
print(f"   • Artists z >50% organic reach: {(df_api['organic_ratio'] > 0.5).sum()} / {len(df_api)}")

# Geografska distribucija
print(f"\n🌍 GEOGRAFSKA DISTRIBUCIJA:")
print(f"   • Št. različnih držav: {len(geo_stats)}")
print(f"   • Top država (popularity): {geo_stats.iloc[0]['country']} ({geo_stats.iloc[0]['pop_mean']:.1f})")
print(f"   • Top država (followers): {geo_stats.iloc[0]['country']}")

# Uspeh po kategorijah
success_dist = df_api['success_category'].value_counts()
print(f"\n⭐ DISTRIBUCIJA USPEŠNOSTI:")
for cat, count in success_dist.items():
    pct = count / len(df_api) * 100
    print(f"   • {cat}: {count} artists ({pct:.1f}%)")

print("\n" + "="*80)
print("✅ VSE VIZUALIZACIJE USTVARJENE!")
print("="*80)
print("\n📁 Generirane datoteke:")
print("   • outputs/viz_platform_dependency_analysis.png")
print("   • outputs/viz_platform_dependency_interactive.html")
print("   • outputs/viz_geographic_analysis.png")
print("   • outputs/viz_geographic_map.html")
print("   • outputs/viz_playlist_diversity.png")
print("   • outputs/viz_api_enrichment_dashboard.html")
print("\n🎊 Vizualizacije pripravljene za vključitev v projekt!")
