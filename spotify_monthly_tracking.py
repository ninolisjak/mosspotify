"""
Spotify Monthly Popularity Tracking Script
==========================================
Skripta za avtomatsko mesečno beleženje popularnosti izvajalcev.
Uporabi za cron job / Task Scheduler.

Setup:
------
Windows Task Scheduler:
  Program: C:\Users\Nino Lisjak\mosspotify\.venv\Scripts\python.exe
  Arguments: spotify_monthly_tracking.py
  Start in: C:\Users\Nino Lisjak\mosspotify
  Schedule: Monthly, 1st day, 00:00

Linux/Mac crontab:
  0 0 1 * * cd /path/to/mosspotify && .venv/bin/python spotify_monthly_tracking.py

Avtor: Spotify Analysis Project
Datum: Januar 2026
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from datetime import datetime
import os
import sys
import logging

# Setup logging
log_file = "data/api_enrichment/tracking_log.txt"
os.makedirs("data/api_enrichment", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURATION
# =============================================================================

SPOTIFY_CLIENT_ID = "9ec80be4c678400bb562c2b2918e87db"
SPOTIFY_CLIENT_SECRET = "dfeead37e4cb41e8b8dd9d607dbf33b0"

DATA_PATH = "data/"
OUTPUT_DIR = "data/api_enrichment"

# =============================================================================
# FUNCTIONS
# =============================================================================

def setup_spotify():
    """Initialize Spotify API connection"""
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        ))
        sp.search('test', limit=1)
        logger.info("✅ Spotify API povezava uspešna!")
        return sp
    except Exception as e:
        logger.error(f"❌ Napaka pri povezavi s Spotify API: {e}")
        return None

def load_artist_ids():
    """Naloži artist IDs iz glavnega dataseta"""
    try:
        # Poskusi naložiti tracks.csv
        tracks_df = pd.read_csv(f"{DATA_PATH}tracks.csv")
        
        # Top 500 najbolj popularnih artists
        top_artists = tracks_df.nlargest(500, 'popularity')[['id_artists', 'artists']].copy()
        top_artists.columns = ['artist_id', 'artist_name']
        top_artists = top_artists.drop_duplicates(subset=['artist_id'])
        
        logger.info(f"✅ Naloženo {len(top_artists)} artist IDs iz tracks.csv")
        return top_artists['artist_id'].tolist(), top_artists
        
    except FileNotFoundError:
        logger.error("❌ Ne najdem tracks.csv - preveri pot do podatkov!")
        return [], pd.DataFrame()
    except Exception as e:
        logger.error(f"❌ Napaka pri nalaganju podatkov: {e}")
        return [], pd.DataFrame()

def track_artist_popularity(sp, artist_ids, batch_name="monthly"):
    """
    Zabeleži trenutno popularnost izvajalcev.
    
    Parameters:
    - sp: Spotipy client
    - artist_ids: List of Spotify artist IDs
    - batch_name: Ime za batch (npr. "monthly_202601")
    
    Returns:
    - DataFrame s popularity podatki
    """
    timestamp = datetime.now()
    data = []
    errors = 0
    
    logger.info(f"🔄 Beleženje popularnosti za {len(artist_ids)} izvajalcev...")
    
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
                        'genres': ', '.join(artist['genres']) if artist['genres'] else '',
                        'timestamp': timestamp,
                        'batch': batch_name
                    })
        except Exception as e:
            errors += 1
            logger.warning(f"⚠️ Napaka pri batch {i}: {e}")
        
        # Progress update vsak 200 artists
        if (i + batch_size) % 200 == 0:
            logger.info(f"   Processed {i+batch_size}/{len(artist_ids)} artists...")
    
    df = pd.DataFrame(data)
    
    # Shrani rezultate
    filename = f"{OUTPUT_DIR}/popularity_{timestamp.strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    
    logger.info(f"✅ Zabeleženo {len(data)} izvajalcev!")
    logger.info(f"   Shranjeno v: {filename}")
    if errors > 0:
        logger.warning(f"   ⚠️ {errors} napak med procesiranjem")
    
    return df

def main():
    """Main execution function"""
    logger.info("=" * 80)
    logger.info("🎵 SPOTIFY MONTHLY POPULARITY TRACKING")
    logger.info("=" * 80)
    
    # 1. Setup Spotify API
    sp = setup_spotify()
    if sp is None:
        logger.error("❌ FAILED: Ne morem vzpostaviti povezave s Spotify API")
        sys.exit(1)
    
    # 2. Load artist IDs
    artist_ids, artists_df = load_artist_ids()
    if len(artist_ids) == 0:
        logger.error("❌ FAILED: Ne najdem artist IDs")
        sys.exit(1)
    
    # 3. Track popularity
    batch_name = f"monthly_{datetime.now().strftime('%Y%m')}"
    
    try:
        popularity_df = track_artist_popularity(sp, artist_ids, batch_name)
        
        # Statistics
        avg_popularity = popularity_df['popularity'].mean()
        avg_followers = popularity_df['followers'].mean()
        
        logger.info("\n📊 STATISTICS:")
        logger.info(f"   Povprečna popularnost: {avg_popularity:.1f}")
        logger.info(f"   Povprečno število followerjev: {avg_followers:,.0f}")
        
        # Top 5 most popular
        top5 = popularity_df.nlargest(5, 'popularity')[['artist_name', 'popularity', 'followers']]
        logger.info("\n🏆 TOP 5 najbolj popularnih:")
        for idx, row in top5.iterrows():
            logger.info(f"   {row['artist_name']}: popularity={row['popularity']}, followers={row['followers']:,}")
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ SUCCESS: Mesečno beleženje končano!")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"❌ FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
