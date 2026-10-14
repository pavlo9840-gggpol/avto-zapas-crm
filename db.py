# -*- coding: utf-8 -*-
"""
db.py
-----
Робота з SQLite базою даних: підключення, створення схеми,
початкове заповнення (пароль за замовчуванням).
"""

import os
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import current_app, g, has_request_context, session
from werkzeug.security import generate_password_hash

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stock.db")
DEFAULT_PASSWORD = "admin123"  # ОБОВ'ЯЗКОВО поміняти після першого входу (сторінка "Налаштування")


def get_db():
    if "db" not in g:
        demo_mode = has_request_context() and session.get("demo_mode")
        database_path = current_app.config["DEMO_DB_PATH"] if demo_mode else current_app.config["DB_PATH"]
        if demo_mode:
            database_uri = f"{Path(database_path).resolve().as_uri()}?mode=ro"
            g.db = sqlite3.connect(
                database_uri,
                uri=True,
                detect_types=sqlite3.PARSE_DECLTYPES,
            )
            g.db.execute("PRAGMA query_only = ON")
        else:
            g.db = sqlite3.connect(
                database_path,
                detect_types=sqlite3.PARSE_DECLTYPES,
            )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


SCHEMA = """
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS thresholds (
    category TEXT PRIMARY KEY,
    min_qty INTEGER NOT NULL DEFAULT 3
);

CREATE TABLE IF NOT EXISTS stock_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    brand TEXT DEFAULT '',
    tread_model TEXT DEFAULT '',
    size TEXT DEFAULT '',
    season TEXT DEFAULT '',
    load_index TEXT DEFAULT '',
    speed_index TEXT DEFAULT '',
    dot_code TEXT DEFAULT '',
    transport_type TEXT DEFAULT '',
    capacity_ah REAL DEFAULT 0,
    cold_crank_amps REAL DEFAULT 0,
    polarity TEXT DEFAULT '',
    case_type TEXT DEFAULT '',
    title TEXT DEFAULT '',
    article TEXT DEFAULT '',
    description TEXT DEFAULT '',
    viscosity TEXT DEFAULT '',
    base_type TEXT DEFAULT '',
    volume TEXT DEFAULT '',
    color_tag TEXT DEFAULT '',
    cost_price REAL DEFAULT 0,
    price REAL DEFAULT 0,
    quantity INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS product_alternatives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    alternative_item_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL,
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL,
    UNIQUE(item_id, alternative_item_id),
    CHECK(item_id < alternative_item_id),
    FOREIGN KEY(item_id) REFERENCES stock_items(id) ON DELETE CASCADE,
    FOREIGN KEY(alternative_item_id) REFERENCES stock_items(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'seller',
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    customer TEXT DEFAULT '',
    phone TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    created_by TEXT DEFAULT '',
    sale_id TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id TEXT PRIMARY KEY,
    received REAL NOT NULL DEFAULT 0,
    change_amount REAL NOT NULL DEFAULT 0,
    reservation_id INTEGER DEFAULT NULL,
    canceled_at TEXT DEFAULT NULL,
    canceled_by TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS brand_icons (
    brand TEXT PRIMARY KEY,
    icon TEXT NOT NULL DEFAULT '',
    icon_file TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    operation TEXT NOT NULL,
    datetime TEXT NOT NULL,
    brand TEXT DEFAULT '',
    tread_model TEXT DEFAULT '',
    size TEXT DEFAULT '',
    season TEXT DEFAULT '',
    load_index TEXT DEFAULT '',
    speed_index TEXT DEFAULT '',
    dot_code TEXT DEFAULT '',
    transport_type TEXT DEFAULT '',
    capacity_ah REAL DEFAULT 0,
    cold_crank_amps REAL DEFAULT 0,
    polarity TEXT DEFAULT '',
    case_type TEXT DEFAULT '',
    title TEXT DEFAULT '',
    article TEXT DEFAULT '',
    description TEXT DEFAULT '',
    viscosity TEXT DEFAULT '',
    base_type TEXT DEFAULT '',
    volume TEXT DEFAULT '',
    cost_price REAL DEFAULT 0,
    price REAL DEFAULT 0,
    quantity INTEGER NOT NULL DEFAULT 0,
    customer TEXT DEFAULT '',
    customer_id INTEGER DEFAULT NULL,
    sale_id TEXT DEFAULT '',
    username TEXT DEFAULT ''
);
"""


def init_db(app):
    """Створює схему (якщо не існує) і заповнює пароль за замовчуванням."""
    db = sqlite3.connect(app.config["DB_PATH"])
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)

    # Міграція для баз, створених до появи кольорових міток
    existing_cols = {row[1] for row in db.execute("PRAGMA table_info(stock_items)")}
    if "color_tag" not in existing_cols:
        db.execute("ALTER TABLE stock_items ADD COLUMN color_tag TEXT DEFAULT ''")
    if "cost_price" not in existing_cols:
        db.execute("ALTER TABLE stock_items ADD COLUMN cost_price REAL DEFAULT 0")
    if "article" not in existing_cols:
        db.execute("ALTER TABLE stock_items ADD COLUMN article TEXT DEFAULT ''")
    if "description" not in existing_cols:
        db.execute("ALTER TABLE stock_items ADD COLUMN description TEXT DEFAULT ''")

    brand_icon_cols = {row[1] for row in db.execute("PRAGMA table_info(brand_icons)")}
    if "icon_file" not in brand_icon_cols:
        db.execute("ALTER TABLE brand_icons ADD COLUMN icon_file TEXT DEFAULT ''")

    history_cols = {row[1] for row in db.execute("PRAGMA table_info(history)")}
    if "cost_price" not in history_cols:
        db.execute("ALTER TABLE history ADD COLUMN cost_price REAL DEFAULT 0")
    if "customer_id" not in history_cols:
        db.execute("ALTER TABLE history ADD COLUMN customer_id INTEGER DEFAULT NULL")
    if "sale_id" not in history_cols:
        db.execute("ALTER TABLE history ADD COLUMN sale_id TEXT DEFAULT ''")
    if "username" not in history_cols:
        db.execute("ALTER TABLE history ADD COLUMN username TEXT DEFAULT ''")
    if "article" not in history_cols:
        db.execute("ALTER TABLE history ADD COLUMN article TEXT DEFAULT ''")
    if "description" not in history_cols:
        db.execute("ALTER TABLE history ADD COLUMN description TEXT DEFAULT ''")

    row = db.execute("SELECT value FROM settings WHERE key = 'password_hash'").fetchone()
    if row is None:
        db.execute(
            "INSERT INTO settings (key, value) VALUES ('password_hash', ?)",
            (generate_password_hash(DEFAULT_PASSWORD),),
        )
        row = db.execute("SELECT value FROM settings WHERE key = 'password_hash'").fetchone()

    # Перехід зі спільного пароля на акаунти: якщо користувачів ще немає,
    # створюємо адміністратора, зберігаючи вже встановлений пароль (щоб нікого
    # не "вибило" з системи при оновленні).
    user_count = db.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
    if user_count == 0:
        db.execute(
            "INSERT INTO users (username, password_hash, role, created_at) VALUES (?, ?, 'admin', ?)",
            ("admin", row["value"], now_str()),
        )

    db.commit()
    db.close()


def register(app):
    app.config.setdefault("DB_PATH", DEFAULT_DB_PATH)
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db(app)


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
