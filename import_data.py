# -*- coding: utf-8 -*-
"""
import_data.py
---------------
Одноразовий імпорт бази з десктопної програми (tires_database.json)
у SQLite базу веб-версії.

Використання (у Bash-консолі PythonAnywhere, з папки webapp):
    python3 import_data.py tires_database.json

Скрипт можна запускати кілька разів безпечно - однакові позиції
(з однаковими ключовими атрибутами: бренд, розмір, DOT і т.д.)
не дублюються, а підсумовуються по кількості. Історія додається
завжди (як новий журнал операцій), тому історію імпортуйте один раз.
"""

import sys
import json

import app as flaskapp
import db as dbmod
from constants import ALL_CATEGORIES

ALL_FIELDS = flaskapp.ALL_FIELDS
NUMERIC_FIELDS = {"capacity_ah", "cold_crank_amps"}


def _extract(item, f):
    if f in NUMERIC_FIELDS:
        try:
            return float(item.get(f, 0) or 0)
        except (TypeError, ValueError):
            return 0.0
    return str(item.get(f, "") or "")


def import_file(json_path):
    with open(json_path, encoding="utf-8") as fh:
        data = json.load(fh)

    stock_added = 0
    stock_merged = 0
    history_added = 0

    with flaskapp.app.app_context():
        db = dbmod.get_db()

        for category in ALL_CATEGORIES:
            cat_data = data.get(category, {})

            for raw_item in cat_data.get("stock", []):
                values = {f: _extract(raw_item, f) for f in ALL_FIELDS}
                price = float(raw_item.get("price", 0) or 0)
                quantity = int(raw_item.get("quantity", 0) or 0)
                color_tag = str(raw_item.get("color_tag", "") or "")
                if quantity <= 0:
                    continue

                existing = flaskapp._find_matching_item(db, category, values)
                if existing:
                    db.execute(
                        "UPDATE stock_items SET quantity = quantity + ?, price = ? WHERE id = ?",
                        (quantity, price, existing["id"]),
                    )
                    stock_merged += 1
                else:
                    fields = ", ".join(ALL_FIELDS)
                    placeholders = ", ".join("?" for _ in ALL_FIELDS)
                    vals = [values[f] for f in ALL_FIELDS]
                    db.execute(
                        f"INSERT INTO stock_items (category, {fields}, color_tag, price, quantity) "
                        f"VALUES (?, {placeholders}, ?, ?, ?)",
                        [category] + vals + [color_tag, price, quantity],
                    )
                    stock_added += 1

            for raw_h in cat_data.get("history", []):
                values = {f: _extract(raw_h, f) for f in ALL_FIELDS}
                price = float(raw_h.get("price", 0) or 0)
                quantity = int(raw_h.get("quantity", 0) or 0)
                operation = str(raw_h.get("operation", "") or "")
                datetime_str = str(raw_h.get("datetime", "") or dbmod.now_str())
                customer = str(raw_h.get("customer", "") or "")

                fields = ", ".join(ALL_FIELDS)
                placeholders = ", ".join("?" for _ in ALL_FIELDS)
                vals = [values[f] for f in ALL_FIELDS]
                db.execute(
                    f"INSERT INTO history (category, operation, datetime, {fields}, price, quantity, customer) "
                    f"VALUES (?, ?, ?, {placeholders}, ?, ?, ?)",
                    [category, operation, datetime_str] + vals + [price, quantity, customer],
                )
                history_added += 1

        db.commit()

    print(f"Готово. Нових позицій на складі: {stock_added}, об'єднано з наявними: {stock_merged}, "
          f"записів історії додано: {history_added}.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання: python3 import_data.py шлях_до_файлу.json")
        sys.exit(1)
    import_file(sys.argv[1])
