# 🎵 SPOTIFY API + SOCIAL MEDIA INTEGRATION
# ============================================
# Zero-Cost implementacija izboljšav
# 
# ⚠️ NOTE: Audio Features in Genres API endpoints so DEPRECATED (Januar 2026)
# Odstranjene funkcije: get_audio_features(), enrich_genres()
# 
# Avtor: Spotify Analysis Project
# Datum: Januar 2026

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
from datetime import datetime
import time
import os
import json

# =============================================================================
# KONFIGURACIJA - VNESI SVOJE CREDENTIALS
# =============================================================================

# 1. Registriraj app: https://developer.spotify.com/dashboard
# 2. Kopiraj Client ID in Secret

SPOTIFY_CLIENT_ID = "9ec80be4c678400bb562c2b2918e87db"
SPOTIFY_CLIENT_SECRET = "dfeead37e4cb41e8b8dd9d607dbf33b0"

# Za Instagram (opcijsko)
# Registracija: https://developers.facebook.com/apps/
INSTAGRAM_ACCESS_TOKEN = "YOUR_INSTAGRAM_TOKEN_HERE"  # Opcijsko

# Output folder
OUTPUT_DIR = "data/api_enrichment"

# =============================================================================
# SPOTIFY API SETUP
# =============================================================================

def setup_spotify():
    """Initialize Spotify API connection"""
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        ))
        # Test connection
        sp.search('test', limit=1)
        print("✅ Spotify API povezava uspešna!")
        return sp
    except Exception as e:
        print(f"❌ Napaka pri povezavi s Spotify API: {e}")
        print("   Preveri, da si vnesel pravilne credentials!")
        return None

# =============================================================================
# 1. POPULARITY TRACKING (Časovno beleženje)
# =============================================================================

def track_artist_popularity(sp, artist_ids, batch_name="snapshot"):
    """
    Zabeleži trenutno popularnost izbranih izvajalcev.
    Kliči mesečno/tedensko za zgodovinsko beleženje.
    
    Parameters:
    - sp: Spotipy client
    - artist_ids: List of Spotify artist IDs
    - batch_name: Ime za batch (npr. "2026-01-10")
    
    Returns:
    - DataFrame s popularity podatki
    """
    timestamp = datetime.now()
    data = []
    errors = []
    
    print(f"🔄 Beleženje popularnosti za {len(artist_ids)} izvajalcev...")
    
    # Spotify API omogoča batch requests (do 50 naenkrat)
    batch_size = 50
    for i in range(0, len(artist_ids), batch_size):
        batch = artist_ids[i:i+batch_size]
        
        try:
            artists = sp.artists(batch)['artists']
            
            for artist in artists:
                if artist:
                    data.append({
                        'artist_id': artist['id'],
                        'artist_name': artist['name'],
                        'popularity': artist['popularity'],
                        'followers': artist['followers']['total'],
                        'genres': artist['genres'],
                        'timestamp': timestamp,
                        'batch': batch_name
                    })
        except Exception as e:
            errors.append({'batch_start': i, 'error': str(e)})
            print(f"   ⚠️ Napaka pri batch {i}: {e}")
        
        # Rate limiting - 180 requests/min max
        if i > 0 and i % 500 == 0:
            print(f"   Processed {i}/{len(artist_ids)} artists...")
            time.sleep(1)  # Počakaj 1 sekundo vsak 500 batch
    
    df = pd.DataFrame(data)
    
    # Shrani rezultate
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{OUTPUT_DIR}/popularity_{timestamp.strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    
    print(f"✅ Zabeleženo {len(data)} izvajalcev!")
    print(f"   Shranjeno v: {filename}")
    if errors:
        print(f"   ⚠️ {len(errors)} napak med procesiranjem")
    
    return df

# =============================================================================
# 2. AUDIO FEATURES - DEPRECATED ❌
# =============================================================================
# ⚠️ Spotify je depreciral Audio Features API endpoint (januar 2026)
# Ta funkcija NI VEČ NA VOLJO
# 
# Alternativa: Uporabi tretje osebe API-je (npr. AcousticBrainz, Last.fm)
# Ali ročna analiza z librosa library (za lokalne datoteke)

# REMOVED: get_audio_features()

# =============================================================================
# 3. PLAYLIST ANALYSIS (Organic vs Algorithmic)
# =============================================================================

def analyze_playlist_presence(sp, artist_name, limit=50):
    """
    Analizira prisotnost izvajalca v playlistih.
    Loči med:
    - Editorial playlists (Spotify uredniske)
    - Algorithmic playlists (Discover Weekly, Radio, Mix)
    - Organic playlists (uporabniške)
    
    Returns:
    - Dict z metrikami playlist presence
    """
    try:
        # Poišči playliste z izvajalcem
        results = sp.search(q=f'artist:{artist_name}', type='playlist', limit=limit)
        
        editorial_reach = 0
        algorithmic_reach = 0
        organic_reach = 0
        playlist_count = {'editorial': 0, 'algorithmic': 0, 'organic': 0}
        
        for playlist in results['playlists']['items']:
            if not playlist:
                continue
                
            try:
                # Pridobi podrobnosti playlista
                playlist_info = sp.playlist(playlist['id'], fields='owner,name,followers')
                followers = playlist_info['followers']['total'] if playlist_info['followers'] else 0
                owner_id = playlist_info['owner']['id'] if playlist_info['owner'] else ''
                name = playlist_info['name'].lower() if playlist_info['name'] else ''
                
                # Kategorizacija
                is_editorial = owner_id == 'spotify'
                is_algorithmic = any(x in name for x in ['discover', 'radar', 'mix', 'radio', 'daily', 'release'])
                
                if is_editorial:
                    editorial_reach += followers
                    playlist_count['editorial'] += 1
                elif is_algorithmic:
                    algorithmic_reach += followers
                    playlist_count['algorithmic'] += 1
                else:
                    organic_reach += followers
                    playlist_count['organic'] += 1
                    
            except Exception as e:
                continue
        
        total_reach = editorial_reach + algorithmic_reach + organic_reach
        
        return {
            'artist_name': artist_name,
            'editorial_reach': editorial_reach,
            'algorithmic_reach': algorithmic_reach,
            'organic_reach': organic_reach,
            'total_reach': total_reach,
            'editorial_playlists': playlist_count['editorial'],
            'algorithmic_playlists': playlist_count['algorithmic'],
            'organic_playlists': playlist_count['organic'],
            'algorithmic_ratio': (editorial_reach + algorithmic_reach) / total_reach if total_reach > 0 else 0,
            'organic_ratio': organic_reach / total_reach if total_reach > 0 else 0
        }
        
    except Exception as e:
        return {
            'artist_name': artist_name,
            'error': str(e)
        }

def batch_playlist_analysis(sp, artist_names, delay=1):
    """
    Analizira playlist presence za več izvajalcev.
    
    Parameters:
    - sp: Spotipy client
    - artist_names: List of artist names
    - delay: Seconds to wait between artists (rate limiting)
    
    Returns:
    - DataFrame z playlist metrics
    """
    print(f"🔄 Analiziranje playlist presence za {len(artist_names)} izvajalcev...")
    print(f"   (Pričakovani čas: ~{len(artist_names) * delay / 60:.1f} minut)")
    
    results = []
    
    for i, artist in enumerate(artist_names):
        metrics = analyze_playlist_presence(sp, artist)
        results.append(metrics)
        
        if i > 0 and i % 10 == 0:
            print(f"   Processed {i}/{len(artist_names)}: {artist}")
        
        time.sleep(delay)
    
    df = pd.DataFrame(results)
    
    # Shrani
    filename = f"{OUTPUT_DIR}/playlist_analysis_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    
    print(f"✅ Analizirano {len(df)} izvajalcev!")
    print(f"   Shranjeno v: {filename}")
    
    return df

# =============================================================================
# 4. GENRE ENRICHMENT - DEPRECATED ❌
# =============================================================================
# ⚠️ Spotify genres API je postal manj zanesljiv (podatki niso več aktivno vzdrževani)
# Mnogi izvajalci nimajo žanrov ali imajo zastarele/napačne žanre
# 
# Alternativa: 
# - Uporabi obstoječe podatke iz artists.csv (26% ima žanre)
# - Last.fm API (boljša žanrska klasifikacija)
# - MusicBrainz tags

# REMOVED: enrich_genres()

# =============================================================================
# 5. RELATED ARTISTS (Network Data)
# =============================================================================

def get_related_artists_network(sp, artist_ids, max_artists=100):
    """
    Zgradi omrežje povezanih izvajalcev.
    Spotify API vrne "related artists" na podlagi poslušalnih vzorcev.
    
    Uporabno za:
    - Network analysis (kolaboracije, podobnost)
    - Identificiranje "bridge artists" med žanri
    - Community detection
    
    Returns:
    - DataFrame z edges (artist1 -> artist2)
    """
    print(f"🔄 Gradnja network grafa za {min(len(artist_ids), max_artists)} izvajalcev...")
    
    edges = []
    nodes_processed = set()
    
    for i, artist_id in enumerate(artist_ids[:max_artists]):
        if artist_id in nodes_processed:
            continue
            
        try:
            related = sp.artist_related_artists(artist_id)['artists']
            
            for rel_artist in related:
                edges.append({
                    'source_id': artist_id,
                    'target_id': rel_artist['id'],
                    'target_name': rel_artist['name'],
                    'target_popularity': rel_artist['popularity'],
                    'target_followers': rel_artist['followers']['total']
                })
            
            nodes_processed.add(artist_id)
            
        except Exception as e:
            print(f"   ⚠️ Napaka za {artist_id}: {e}")
        
        if i > 0 and i % 20 == 0:
            print(f"   Processed {i}/{max_artists}...")
        
        time.sleep(0.5)  # Rate limiting
    
    df = pd.DataFrame(edges)
    
    # Shrani
    filename = f"{OUTPUT_DIR}/artist_network_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    
    print(f"✅ Zgrajeno {len(df)} network edges!")
    
    return df

# =============================================================================
# 6. NEW RELEASES TRACKING
# =============================================================================

def track_new_releases(sp, country='US', limit=50):
    """
    Sledi novim izdajam na Spotify.
    Uporabno za analizo trendov novih izvajalcev.
    
    Returns:
    - DataFrame z novimi albumi
    """
    try:
        releases = sp.new_releases(country=country, limit=limit)['albums']['items']
        
        data = []
        for album in releases:
            artists = [a['name'] for a in album['artists']]
            artist_ids = [a['id'] for a in album['artists']]
            
            data.append({
                'album_id': album['id'],
                'album_name': album['name'],
                'album_type': album['album_type'],
                'release_date': album['release_date'],
                'artists': artists,
                'artist_ids': artist_ids,
                'total_tracks': album['total_tracks'],
                'timestamp': datetime.now()
            })
        
        df = pd.DataFrame(data)
        
        # Shrani
        filename = f"{OUTPUT_DIR}/new_releases_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        
        print(f"✅ Zabeleženo {len(df)} novih izdaj!")
        
        return df
        
    except Exception as e:
        print(f"❌ Napaka pri pridobivanju novih izdaj: {e}")
        return pd.DataFrame()

# =============================================================================
# 7. SOCIAL MEDIA ENRICHMENT (Manual/Semi-automated)
# =============================================================================

# Instagram API je omejen, zato ponujamo ročno mapiranje + CSV

SOCIAL_MEDIA_MAPPING = {
    # Top artists mapping (ročno ali s scrapingom)
    # Format: 'Spotify Artist Name': {'instagram': '@handle', 'tiktok': '@handle', 'twitter': '@handle'}
    
    'Taylor Swift': {'instagram': '@taylorswift', 'tiktok': '@taylorswift', 'twitter': '@taylorswift13'},
    'Ed Sheeran': {'instagram': '@teddysphotos', 'tiktok': '@edsheeran', 'twitter': '@edsheeran'},
    'Drake': {'instagram': '@champagnepapi', 'tiktok': '@drake', 'twitter': '@Drake'},
    'Bad Bunny': {'instagram': '@badbunnypr', 'tiktok': '@badbunny', 'twitter': '@sanikibadbunny'},
    'The Weeknd': {'instagram': '@theweeknd', 'tiktok': '@theweeknd', 'twitter': '@theweeknd'},
    'Ariana Grande': {'instagram': '@arianagrande', 'tiktok': '@arianagrande', 'twitter': '@ArianaGrande'},
    'Post Malone': {'instagram': '@postmalone', 'tiktok': '@postmalone', 'twitter': '@PostMalone'},
    'Dua Lipa': {'instagram': '@dualipa', 'tiktok': '@dualipaofficial', 'twitter': '@DUALIPA'},
    'Billie Eilish': {'instagram': '@billieeilish', 'tiktok': '@billieeilish', 'twitter': '@billieeilish'},
    'Justin Bieber': {'instagram': '@justinbieber', 'tiktok': '@justinbieber', 'twitter': '@justinbieber'},
    # Dodaj več ročno...
}

def create_social_media_template(artist_names, output_file='data/social_media_mapping.csv'):
    """
    Ustvari CSV template za ročno mapiranje social media handles.
    
    Uporaba:
    1. Poženi to funkcijo
    2. Odpri CSV in ročno vnesi Instagram/TikTok handles
    3. Uporabi v analizi
    """
    data = []
    for artist in artist_names:
        mapping = SOCIAL_MEDIA_MAPPING.get(artist, {})
        data.append({
            'artist_name': artist,
            'instagram': mapping.get('instagram', ''),
            'tiktok': mapping.get('tiktok', ''),
            'twitter': mapping.get('twitter', ''),
            'youtube': '',
            'notes': ''
        })
    
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"✅ Template ustvarjen: {output_file}")
    print("   Odpri CSV in ročno vnesi manjkajoče social media handles!")
    
    return df

# =============================================================================
# 8. INSTAGRAM API (če imaš Graph API access)
# =============================================================================

def get_instagram_metrics(username, access_token=INSTAGRAM_ACCESS_TOKEN):
    """
    Pridobi Instagram metrike (potrebuje Graph API access).
    
    NOTE: Instagram Graph API zahteva Business/Creator account
    in Meta Developer registration.
    
    Alternativa: Uporabi social-media-scraper libraries (na lastno odgovornost)
    """
    import requests
    
    if access_token == "YOUR_INSTAGRAM_TOKEN_HERE":
        print("⚠️ Instagram API token ni nastavljen!")
        return None
    
    try:
        # Instagram Graph API endpoint
        url = f"https://graph.instagram.com/v18.0/{username}"
        params = {
            'fields': 'username,followers_count,media_count',
            'access_token': access_token
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"   ⚠️ Instagram API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ⚠️ Instagram API exception: {e}")
        return None

# =============================================================================
# 9. MUSICBRAINZ API (Free, no auth needed)
# =============================================================================

def get_musicbrainz_data(artist_name):
    """
    Pridobi podatke iz MusicBrainz (brezplačni, odprtokodni).
    Vključuje: birth year, area, type, disambiguation, etc.
    
    MusicBrainz je dobra alternativa za dodatne metapodatke.
    """
    import requests
    import urllib.parse
    
    try:
        # Search for artist
        encoded_name = urllib.parse.quote(artist_name)
        url = f"https://musicbrainz.org/ws/2/artist/?query={encoded_name}&fmt=json&limit=1"
        
        headers = {'User-Agent': 'SpotifyAnalysis/1.0 (research project)'}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data['artists']:
                artist = data['artists'][0]
                return {
                    'name': artist.get('name'),
                    'type': artist.get('type'),  # Person, Group, etc.
                    'country': artist.get('country'),
                    'begin_year': artist.get('life-span', {}).get('begin', ''),
                    'end_year': artist.get('life-span', {}).get('end', ''),
                    'disambiguation': artist.get('disambiguation', ''),
                    'score': artist.get('score')
                }
        
        return None
        
    except Exception as e:
        return None

def batch_musicbrainz_enrichment(artist_names, delay=1):
    """
    Pridobi MusicBrainz podatke za več izvajalcev.
    
    NOTE: MusicBrainz ima rate limit 1 request/sekundo za anonymous
    """
    print(f"🔄 Pridobivanje MusicBrainz podatkov za {len(artist_names)} izvajalcev...")
    print(f"   (Pričakovani čas: ~{len(artist_names) * delay / 60:.1f} minut)")
    
    results = []
    
    for i, artist in enumerate(artist_names):
        data = get_musicbrainz_data(artist)
        if data:
            data['spotify_name'] = artist
            results.append(data)
        
        if i > 0 and i % 50 == 0:
            print(f"   Processed {i}/{len(artist_names)}")
        
        time.sleep(delay)
    
    df = pd.DataFrame(results)
    
    # Shrani
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{OUTPUT_DIR}/musicbrainz_enrichment_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    
    print(f"✅ Pridobljeno {len(df)} MusicBrainz records!")
    
    return df

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Glavna funkcija za poganjanje vseh enrichment procesov.
    """
    print("="*60)
    print("🎵 SPOTIFY API ENRICHMENT - Zero Cost Implementation")
    print("="*60)
    print()
    
    # 1. Setup Spotify
    sp = setup_spotify()
    if not sp:
        print("❌ Spotify API ni nastavljen. Preveri credentials!")
        return
    
    # 2. Naloži obstoječe podatke
    print("\n📂 Nalaganje obstoječih podatkov...")
    try:
        tracks = pd.read_csv('data/tracks.csv')
        artists = pd.read_csv('data/artists.csv')
        print(f"   ✅ Naloženo {len(tracks):,} skladb in {len(artists):,} izvajalcev")
    except Exception as e:
        print(f"   ❌ Napaka pri nalaganju: {e}")
        return
    
    # 3. Identificiraj top izvajalce za enrichment
    top_artists = artists.nlargest(500, 'popularity')
    artist_ids = top_artists['id'].tolist()
    artist_names = top_artists['name'].tolist()
    
    print(f"\n🎯 Izbrani top {len(artist_ids)} izvajalcev za enrichment")
    
    # 4. Izberi kaj želiš pognati
    print("\n" + "="*60)
    print("IZBERI ENRICHMENT PROCESE:")
    print("="*60)
    print("1. Popularity tracking (hitro, ~1 min)")
    print("2. Playlist analysis (počasno, ~8 min za 500 artists)")
    print("3. Artist network (srednje, ~2 min)")
    print("4. MusicBrainz enrichment (počasno, ~8 min)")
    print("5. New releases tracking (instant)")
    print("A. VSE (počasno, ~20+ min)")
    print()
    print("⚠️  Audio Features in Genres API sta DEPRECATED - ne več na voljo")
    print()
    
    choice = input("Vnesi izbiro (1-5, A za vse, ali Q za izhod): ").strip().upper()
    
    if choice == 'Q':
        print("👋 Bye!")
        return
    
    # Execute selected processes
    if choice in ['1', 'A']:
        print("\n" + "-"*40)
        track_artist_popularity(sp, artist_ids)
    
    if choice in ['2', 'A']:
        print("\n" + "-"*40)
        batch_playlist_analysis(sp, artist_names[:100], delay=1)  # Samo top 100 za demo
    
    if choice in ['3', 'A']:
        print("\n" + "-"*40)
        get_related_artists_network(sp, artist_ids, max_artists=100)
    
    if choice in ['4', 'A']:
        print("\n" + "-"*40)
        batch_musicbrainz_enrichment(artist_names[:100], delay=1)
    
    if choice in ['5', 'A']:
        print("\n" + "-"*40)
        track_new_releases(sp, country='US', limit=50)
    
    print("\n" + "="*60)
    print("✅ ENRICHMENT KONČAN!")
    print(f"   Rezultati shranjeni v: {OUTPUT_DIR}/")
    print("="*60)

if __name__ == "__main__":
    main()
