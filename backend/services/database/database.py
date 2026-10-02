# =====================================================
# iVerify V2 - Database Core
# Sosyal Medya Veri Analiz Motoru
# =====================================================

import sqlite3
from pathlib import Path


# -----------------------------------------------------
# Proje ana dizinini bul
# -----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]


# -----------------------------------------------------
# Database konumu
# -----------------------------------------------------

DATABASE_FOLDER = BASE_DIR / "database"

DATABASE_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


DATABASE_FILE = DATABASE_FOLDER / "iverify_v2.db"


# -----------------------------------------------------
# Veritabanı bağlantısı
# -----------------------------------------------------

def get_connection():

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    return connection



# -----------------------------------------------------
# Tabloları oluştur
# -----------------------------------------------------

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    # Analiz geçmişleri
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        analysis_id TEXT UNIQUE,

        filename TEXT,

        created_at TEXT,

        total_users INTEGER,

        status TEXT

    )
    """)


    # Kullanıcı kayıtları
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        category TEXT,

        source TEXT,

        discovered_at TEXT,

        reason TEXT

    )
    """)


    # Audit kayıtları
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        action TEXT,

        created_at TEXT,

        details TEXT

    )
    """)


    connection.commit()

    connection.close()



# -----------------------------------------------------
# Test
# -----------------------------------------------------

if __name__ == "__main__":

    initialize_database()

    print(
        "iVerify V2 database hazır."
    )