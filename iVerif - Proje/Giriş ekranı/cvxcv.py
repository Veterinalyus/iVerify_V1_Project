import os
import json
import time
import uuid
import sqlite3
import zipfile
import logging
import re

from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("iVerify")

app = Flask(__name__)
CORS(app)

BASE_DIR = Path("iverify_final_data")
UPLOAD_DIR = BASE_DIR / "uploads"
LOG_DIR = BASE_DIR / "logs"
DATABASE = BASE_DIR / "iverify.db"

BASE_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    with get_db() as db:
        db.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses
        (
            id TEXT PRIMARY KEY,
            filename TEXT,
            created_at INTEGER,
            total_users INTEGER,
            status TEXT
        )
        """
        )
        db.execute(
        """
        CREATE TABLE IF NOT EXISTS discovered_users
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id TEXT,
            username TEXT,
            category TEXT,
            source_file TEXT,
            source_path TEXT,
            timestamp INTEGER,
            profile_url TEXT
        )
        """
        )
        db.commit()


init_database()


def success_response(data):
    return jsonify({"success": True, "data": data, "error": None})


def error_response(message):
    return jsonify({"success": False, "data": None, "error": message})


def clean_text(value):
    if value is None:
        return None
    if not isinstance(value, str):
        return None
    return value.strip()


def clean_username(value):
    value = clean_text(value)
    if not value:
        return None
    value = value.replace("@", "")
    value = value.strip()
    if len(value) < 2:
        return None
    if len(value) > 50:
        return None
    if not re.match(r"^[a-zA-Z0-9._]+$", value):
        return None
    return value.lower()


def profile_url(username):
    if not username:
        return None
    return "https://instagram.com/" + username


def read_json_from_zip(zip_file, filename):
    try:
        with zip_file.open(filename) as file:
            return json.load(file)
    except Exception as error:
        logger.warning(f"JSON okunamadı: {filename} | {error}")
        return None


USER_KEYS = [
    "username", "user", "title", "value", "href",
    "string_list_data", "relationships_following", "label_values"
]

CATEGORY_HINTS = {
    "received_requests": ["received"],
    "pending_requests": ["pending", "requested_sent", "requests_sent"],
    "close_friends": ["close_friend"],
    "blocked": ["blocked"],
    "restricted": ["restricted"],
    "following": ["following", "followings"],
    "followers": ["followers", "follower"]
}


def detect_category_from_name(filename):
    # Use only the file's own name, not the folder path — the real
    # Instagram export folder "followers_and_following" contains the
    # word "followers" and was wrongly matching every file inside it.
    name = os.path.basename(filename).lower()
    for category, words in CATEGORY_HINTS.items():
        for word in words:
            if word in name:
                return category
    return "unknown"


def deep_walk(data, path=""):
    results = []
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = path + "/" + str(key)
            results.append({"key": key, "value": value, "path": current_path})
            results.extend(deep_walk(value, current_path))
    elif isinstance(data, list):
        for index, item in enumerate(data):
            current_path = path + "/" + str(index)
            results.extend(deep_walk(item, current_path))
    return results


def has_user_signal(data):
    if not isinstance(data, (dict, list)):
        return False
    text = json.dumps(data, ensure_ascii=False).lower()
    signals = ["string_list_data", "relationships_following", "href", "title", "username", "label_values"]
    score = 0
    for signal in signals:
        if signal in text:
            score += 1
    return score >= 2


def discover_zip_files(zip_path):
    discovered = []
    with zipfile.ZipFile(zip_path, "r") as archive:
        for filename in archive.namelist():
            if not filename.lower().endswith(".json"):
                continue
            content = read_json_from_zip(archive, filename)
            if content is None:
                continue
            category = detect_category_from_name(filename)
            user_possible = has_user_signal(content)
            discovered.append({
                "filename": filename,
                "category": category,
                "user_possible": user_possible,
                "content": content
            })
    return discovered


def create_discovery_report(files):
    report = {"total_json": len(files), "found_categories": {}, "unknown_files": []}
    for file in files:
        category = file["category"]
        if category == "unknown":
            report["unknown_files"].append(file["filename"])
        else:
            if category not in report["found_categories"]:
                report["found_categories"][category] = []
            report["found_categories"][category].append(file["filename"])
    return report


def extract_username_from_object(obj):
    entries = []
    if not isinstance(obj, dict):
        return entries
    if "title" in obj:
        username = clean_username(obj.get("title"))
        if username:
            entries.append({"username": username, "timestamp": obj.get("timestamp")})
    if "username" in obj:
        username = clean_username(obj.get("username"))
        if username:
            entries.append({"username": username, "timestamp": obj.get("timestamp")})
    string_data = obj.get("string_list_data", [])
    if isinstance(string_data, list):
        for item in string_data:
            if not isinstance(item, dict):
                continue
            for key in ["value", "title", "username"]:
                username = clean_username(item.get(key))
                if username:
                    entries.append({"username": username, "timestamp": item.get("timestamp")})
    labels = obj.get("label_values", [])
    if isinstance(labels, list):
        for item in labels:
            if not isinstance(item, dict):
                continue
            username = clean_username(item.get("value"))
            if username:
                entries.append({"username": username, "timestamp": item.get("timestamp")})
    deduped = {}
    for entry in entries:
        deduped[entry["username"]] = entry
    return list(deduped.values())


def extract_users_recursive(data):
    found = []
    if isinstance(data, dict):
        entries = extract_username_from_object(data)
        for entry in entries:
            username = entry["username"]
            found.append({
                "username": username,
                "url": profile_url(username),
                "timestamp": entry.get("timestamp") or 0
            })
        for value in data.values():
            found.extend(extract_users_recursive(value))
    elif isinstance(data, list):
        for item in data:
            found.extend(extract_users_recursive(item))
    return found


def clean_user_list(users):
    result = {}
    for user in users:
        username = user.get("username")
        if not username:
            continue
        result[username] = user
    return list(result.values())


def collect_category_users(discovered_files):
    categories = {
        "followers": [], "following": [], "pending_requests": [],
        "received_requests": [], "close_friends": [], "blocked": [], "restricted": []
    }
    for file in discovered_files:
        category = file["category"]
        users = extract_users_recursive(file["content"])
        if category in categories:
            for user in users:
                user["source"] = file["filename"]
            categories[category].extend(users)
    for key in categories:
        categories[key] = clean_user_list(categories[key])
    return categories


def analyze_relationships(categories):
    followers = {user["username"] for user in categories["followers"]}
    following = {user["username"] for user in categories["following"]}
    pending = categories["pending_requests"]
    mutual = followers & following
    not_following_back = following - followers
    only_followers = followers - following
    return {
        "stats": {
            "followers": len(followers),
            "following": len(following),
            "mutual": len(mutual),
            "not_following_back": len(not_following_back),
            "only_followers": len(only_followers),
            "pending": len(pending)
        },
        "users": {
            "followers": [u for u in categories["followers"]],
            "following": [u for u in categories["following"]],
            "mutual": [{"username": u, "url": profile_url(u)} for u in sorted(mutual)],
            "not_following_back": [{"username": u, "url": profile_url(u)} for u in sorted(not_following_back)],
            "only_followers": [{"username": u, "url": profile_url(u)} for u in sorted(only_followers)],
            "pending_requests": pending,
            "received_requests": categories["received_requests"],
            "close_friends": categories["close_friends"],
            "blocked": categories["blocked"],
            "restricted": categories["restricted"]
        }
    }


def process_zip(zip_path):
    discovered = discover_zip_files(zip_path)
    categories = collect_category_users(discovered)
    result = analyze_relationships(categories)
    result["report"] = create_discovery_report(discovered)
    result["created_at"] = int(time.time())
    return result, categories


def save_analysis_result(filename, result):
    analysis_id = uuid.uuid4().hex
    created = int(time.time())
    total_users = result.get("stats", {}).get("followers", 0)
    with get_db() as db:
        db.execute(
        """
        INSERT INTO analyses (id, filename, created_at, total_users, status)
        VALUES (?,?,?,?,?)
        """,
        (analysis_id, filename, created, total_users, "completed")
        )
        for category, users in result.get("users", {}).items():
            for user in users:
                db.execute(
                """
                INSERT INTO discovered_users
                (analysis_id, username, category, source_file, source_path, timestamp, profile_url)
                VALUES (?,?,?,?,?,?,?)
                """,
                (
                    analysis_id, user.get("username"), category,
                    user.get("source"), user.get("source_path"),
                    user.get("timestamp", 0), user.get("url")
                )
                )
        db.commit()
    return analysis_id


@app.route("/api/analyze", methods=["POST"])
def analyze_api():
    try:
        if "file" not in request.files:
            return error_response("ZIP dosyası bulunamadı")
        uploaded = request.files["file"]
        filename = secure_filename(uploaded.filename)
        if not filename.lower().endswith(".zip"):
            return error_response("Sadece ZIP dosyası yükleyebilirsiniz")
        save_path = UPLOAD_DIR / (uuid.uuid4().hex + "_" + filename)
        uploaded.save(save_path)
        logger.info(f"Analiz başladı: {filename}")
        result, categories = process_zip(save_path)
        analysis_id = save_analysis_result(filename, result)
        result["analysis_id"] = analysis_id
        return success_response(result)
    except Exception as error:
        logger.exception(error)
        return error_response(str(error))


@app.route("/api/history", methods=["GET"])
def history():
    with get_db() as db:
        rows = db.execute("SELECT * FROM analyses ORDER BY created_at DESC").fetchall()
    return success_response([dict(row) for row in rows])


@app.route("/api/search", methods=["GET"])
def user_search():
    query = request.args.get("q", "")
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM discovered_users WHERE username LIKE ? LIMIT 500",
            ("%" + query + "%",)
        ).fetchall()
    return success_response([dict(row) for row in rows])


@app.route("/api/status", methods=["GET"])
def status():
    return success_response({"system": "iVerify", "status": "running", "time": int(time.time())})


if __name__ == "__main__":
    logger.info("iVerify FINAL ENGINE başlatıldı")
    app.run(host="127.0.0.1", port=5000, debug=False)
