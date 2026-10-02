# =====================================================
# iVerify V2 - Configuration File
# Sosyal Medya Veri Analiz Motoru
# =====================================================

from pathlib import Path


# -----------------------------------------------------
# Uygulama Bilgileri
# -----------------------------------------------------

APP_NAME = "iVerify"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Sosyal Medya Veri Analiz Motoru"


# -----------------------------------------------------
# Ana Proje Konumu
# -----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent


# -----------------------------------------------------
# Veri Klasörleri
# -----------------------------------------------------

DATA_DIR = BASE_DIR / "data"

UPLOAD_DIR = DATA_DIR / "uploads"

HISTORY_DIR = DATA_DIR / "history"

LOG_DIR = DATA_DIR / "logs"

CACHE_DIR = DATA_DIR / "cache"


# -----------------------------------------------------
# Veritabanı
# -----------------------------------------------------

DATABASE_DIR = BASE_DIR / "database"

DATABASE_FILE = DATABASE_DIR / "iverify_v2.db"


# -----------------------------------------------------
# Dosya Ayarları
# -----------------------------------------------------

ALLOWED_EXTENSIONS = [
    ".zip"
]


# -----------------------------------------------------
# Sistem Ayarları
# -----------------------------------------------------

DEBUG_MODE = True

VERSION_LABEL = "iVerify V2"


# -----------------------------------------------------
# İlk Çalışmada Gerekli Klasörleri Oluştur
# -----------------------------------------------------

REQUIRED_DIRECTORIES = [
    DATA_DIR,
    UPLOAD_DIR,
    HISTORY_DIR,
    LOG_DIR,
    CACHE_DIR,
    DATABASE_DIR
]


for directory in REQUIRED_DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)