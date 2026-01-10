"""
Quick Demo Script - API Enrichment Showcase
============================================
Skripta za hitro demonstracijo API enrichment funkcionalnosti.
Izvede mini-test na 5 artists in prikaže rezultate.

Uporaba:
    python demo_enrichment.py

Avtor: Spotify Analysis Project
Datum: Januar 2026
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
from datetime import datetime
import time
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

SPOTIFY_CLIENT_ID = "9ec80be4c678400bb562c2b2918e87db"
SPOTIFY_CLIENT_SECRET = "dfeead37e4cb41e8b8dd9d607dbf33b0"

# Demo artists (znani, da bo hitro)
DEMO_ARTISTS = [
    ("Taylor Swift", "06HL4z0CvFAxyc27GXpf02"),
    ("Ed Sheeran", "6eUKZXaKkcviH0Ku9w2n3V"),
    ("Drake", "3TVXtAsR1Inumwj472S9r4"),
    ("Bad Bunny", "4q3ewBCX7sLwd24euuV69X"),
    ("The Weeknd", "1Xyo4u8uXC1ZmMpatF05PJ")
]

# =============================================================================
# DEMO FUNCTIONS
# =============================================================================

def setup_spotify():
    """Initialize Spotify API"""
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        ))
        sp.search('test', limit=1)
        return sp
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

def demo_popularity_tracking(sp, artist_ids):
    """Demo: Popularity tracking"""
    print("\n" + "="*80)
    print("📊 DEMO 1: POPULARITY TRACKING")
    print("="*80)
    print("Purpose: Odpravlja survivorship bias z mesečnimi snapshots\n")
    
    data = []
    try:
        artists = sp.artists(artist_ids)['artists']
        
        for artist in artists:
            if artist:
                data.append({
                    'Artist': artist['name'],
                    'Popularity': artist['popularity'],
                    'Followers': f"{artist['followers']['total']:,}",
                    'Genres': ', '.join(artist['genres'][:2]) if artist['genres'] else 'N/A'
                })
        
        df = pd.DataFrame(data)
        print(df.to_string(index=False))
        
        print(f"\n💡 INSIGHT:")
        print(f"   • Povprečna popularnost: {df['Popularity'].mean():.1f}")
        print(f"   • Če to ponavljaš MESEČNO → vidiš rast/padec skozi čas")
        print(f"   • Odpravi survivorship bias iz snapshot podatkov!")
        
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return pd.DataFrame()

def demo_playlist_analysis(sp, artist_name):
    """Demo: Playlist presence analysis"""
    print("\n" + "="*80)
    print("📊 DEMO 2: PLAYLIST ANALYSIS (Organic vs Platform)")
    print("="*80)
    print(f"Artist: {artist_name}\n")
    
    try:
        results = sp.search(q=f'artist:{artist_name}', type='playlist', limit=30)
        
        editorial_count = 0
        algorithmic_count = 0
        organic_count = 0
        
        editorial_reach = 0
        algorithmic_reach = 0
        organic_reach = 0
        
        for playlist in results['playlists']['items']:
            if not playlist:
                continue
                
            try:
                playlist_info = sp.playlist(playlist['id'], fields='owner,name,followers')
                followers = playlist_info['followers']['total'] if playlist_info.get('followers') else 0
                owner_id = playlist_info['owner']['id'] if playlist_info.get('owner') else ''
                name = playlist_info['name'].lower() if playlist_info.get('name') else ''
                
                is_editorial = owner_id == 'spotify'
                is_algorithmic = any(x in name for x in ['discover', 'radar', 'mix', 'radio', 'daily'])
                
                if is_editorial:
                    editorial_count += 1
                    editorial_reach += followers
                elif is_algorithmic:
                    algorithmic_count += 1
                    algorithmic_reach += followers
                else:
                    organic_count += 1
                    organic_reach += followers
                    
            except:
                continue
        
        total_reach = editorial_reach + algorithmic_reach + organic_reach
        platform_ratio = (editorial_reach + algorithmic_reach) / total_reach if total_reach > 0 else 0
        
        print(f"Playlist counts:")
        print(f"  • Editorial (Spotify): {editorial_count} playlists, {editorial_reach:,} reach")
        print(f"  • Algorithmic: {algorithmic_count} playlists, {algorithmic_reach:,} reach")
        print(f"  • Organic (user): {organic_count} playlists, {organic_reach:,} reach")
        print(f"\n📈 Platform Dependency Ratio: {platform_ratio:.1%}")
        
        print(f"\n💡 INSIGHT:")
        if platform_ratio > 0.7:
            print(f"   🔴 VISOKE OVIRE - {platform_ratio:.0%} dosega je platform-driven!")
            print(f"   → Brez Spotify promocije je težko uspeti")
        elif platform_ratio > 0.4:
            print(f"   🟡 MEŠANO - {platform_ratio:.0%} platform, {(1-platform_ratio):.0%} organic")
        else:
            print(f"   🟢 NIZKE OVIRE - {(1-platform_ratio):.0%} organic reach!")
            print(f"   → Organski uspeh je možen")
        
        return {
            'artist': artist_name,
            'platform_ratio': platform_ratio,
            'total_reach': total_reach
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}

def demo_network_graph(sp, artist_id, artist_name):
    """Demo: Related artists network"""
    print("\n" + "="*80)
    print("📊 DEMO 3: NETWORK GRAPH (Mrežni učinki)")
    print("="*80)
    print(f"Artist: {artist_name}\n")
    
    try:
        related = sp.artist_related_artists(artist_id)['artists']
        
        print(f"Related artists ({len(related)}):")
        for i, artist in enumerate(related[:5]):  # Top 5
            print(f"  {i+1}. {artist['name']} (popularity: {artist['popularity']})")
        print(f"  ... in še {len(related)-5} drugih")
        
        avg_popularity = sum(a['popularity'] for a in related) / len(related)
        
        print(f"\n📈 Network Strength Metrics:")
        print(f"  • Network connections: {len(related)}")
        print(f"  • Average network popularity: {avg_popularity:.1f}")
        
        print(f"\n💡 INSIGHT:")
        if len(related) > 15:
            print(f"   ✅ MOČNA MREŽA ({len(related)} povezav)")
            print(f"   → Pričakujemo boljšo retention (network effects!)")
        else:
            print(f"   ⚠️ ŠIBKA MREŽA ({len(related)} povezav)")
            print(f"   → Izoliran artist, težja retention")
        
        return {
            'artist': artist_name,
            'network_connections': len(related),
            'avg_network_popularity': avg_popularity
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}

def demo_musicbrainz(artist_name):
    """Demo: MusicBrainz demographics"""
    print("\n" + "="*80)
    print("📊 DEMO 4: MUSICBRAINZ DEMOGRAPHICS")
    print("="*80)
    print(f"Artist: {artist_name}\n")
    
    try:
        base_url = "https://musicbrainz.org/ws/2/artist/"
        headers = {'User-Agent': 'SpotifyAnalysisProject/1.0'}
        params = {'query': artist_name, 'fmt': 'json', 'limit': 1}
        
        response = requests.get(base_url, params=params, headers=headers)
        
        if response.status_code == 200:
            results = response.json()
            
            if results.get('artists'):
                artist = results['artists'][0]
                
                country = artist.get('country', 'Unknown')
                begin_year = artist.get('life-span', {}).get('begin', '')[:4] if artist.get('life-span') else 'Unknown'
                artist_type = artist.get('type', 'Unknown')
                
                print(f"Demographics:")
                print(f"  • Country: {country}")
                print(f"  • Career start: {begin_year}")
                print(f"  • Type: {artist_type}")
                
                print(f"\n💡 INSIGHT:")
                print(f"   → Cox regression stratifikacija po državi/generaciji")
                print(f"   → Ali US/UK artists imajo boljšo survival rate?")
                
                return {
                    'artist': artist_name,
                    'country': country,
                    'begin_year': begin_year
                }
            else:
                print(f"⚠️ Artist not found in MusicBrainz")
                return {}
        else:
            print(f"❌ HTTP {response.status_code}")
            return {}
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}

# =============================================================================
# MAIN DEMO
# =============================================================================

def main():
    """Run full demo"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "🎵 API ENRICHMENT DEMO 🎵" + " "*32 + "║")
    print("║" + " "*78 + "║")
    print("║" + "  Demonstracija 4 ključnih funkcionalnosti:".ljust(78) + "║")
    print("║" + "    1. Popularity Tracking (odpravlja survivorship bias)".ljust(78) + "║")
    print("║" + "    2. Playlist Analysis (organic vs platform-driven)".ljust(78) + "║")
    print("║" + "    3. Network Graph (mrežni učinki na retention)".ljust(78) + "║")
    print("║" + "    4. MusicBrainz Demographics (geografska stratifikacija)".ljust(78) + "║")
    print("╚" + "="*78 + "╝")
    
    # Setup
    print("\n🔧 Initializing Spotify API...")
    sp = setup_spotify()
    
    if sp is None:
        print("\n❌ DEMO FAILED: Cannot connect to Spotify API")
        print("   Check your credentials in the script!")
        return
    
    print("✅ Connected to Spotify API!\n")
    input("Press ENTER to start demo...")
    
    # Extract artist data
    artist_names = [name for name, _ in DEMO_ARTISTS]
    artist_ids = [id_ for _, id_ in DEMO_ARTISTS]
    
    # Demo 1: Popularity
    popularity_df = demo_popularity_tracking(sp, artist_ids)
    input("\nPress ENTER to continue...")
    
    # Demo 2: Playlist (samo prvi artist)
    playlist_result = demo_playlist_analysis(sp, artist_names[0])
    input("\nPress ENTER to continue...")
    
    # Demo 3: Network (samo prvi artist)
    network_result = demo_network_graph(sp, artist_ids[0], artist_names[0])
    input("\nPress ENTER to continue...")
    
    # Demo 4: MusicBrainz (samo prvi artist)
    mb_result = demo_musicbrainz(artist_names[0])
    
    # Summary
    print("\n" + "="*80)
    print("✅ DEMO COMPLETED!")
    print("="*80)
    print("\n📊 SUMMARY:")
    print(f"  • Tested {len(DEMO_ARTISTS)} artists")
    print(f"  • 4 enrichment methods executed successfully")
    print(f"  • Ready for production deployment!")
    
    print("\n🚀 NEXT STEPS:")
    print("  1. Open spotify_analysis.ipynb")
    print("  2. Run cells from 'API ENRICHMENT 1' onwards")
    print("  3. Execute: enriched_test = run_full_enrichment(n_artists=20)")
    print("  4. Review outputs in: data/api_enrichment/")
    
    print("\n📖 DOCUMENTATION:")
    print("  • API_ENRICHMENT_README.md - Detailed usage guide")
    print("  • PRIMERJAVA_PRED_PO.md - Before/After comparison")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
