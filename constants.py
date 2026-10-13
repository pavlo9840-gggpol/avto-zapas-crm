# -*- coding: utf-8 -*-
"""
constants.py
------------
Довідкові дані (бренди, розміри, категорії) та функції розшифровки
LI/SI і DOT-коду. Веб-версія обліку шин, акумуляторів та мастил.
"""

import math

# ---------------------------------------------------------------
# Категорії
# ---------------------------------------------------------------

CATEGORY_CAR = "car"
CATEGORY_MOTO = "moto"
CATEGORY_BATTERY_CAR = "battery_car"
CATEGORY_BATTERY_MOTO = "battery_moto"
CATEGORY_OIL_CAR = "oil_car"
CATEGORY_OIL_MOTO = "oil_moto"
CATEGORY_OIL_TRANS = "oil_trans"
CATEGORY_OIL_SPECIAL = "oil_special"

ALL_CATEGORIES = (
    CATEGORY_CAR, CATEGORY_MOTO, CATEGORY_BATTERY_CAR, CATEGORY_BATTERY_MOTO,
    CATEGORY_OIL_CAR, CATEGORY_OIL_MOTO, CATEGORY_OIL_TRANS, CATEGORY_OIL_SPECIAL,
)

CATEGORY_LABELS = {
    CATEGORY_CAR: "Автомобільні шини",
    CATEGORY_MOTO: "Мотоциклетні шини",
    CATEGORY_BATTERY_CAR: "Автомобільні акумулятори",
    CATEGORY_BATTERY_MOTO: "Мотоциклетні акумулятори",
    CATEGORY_OIL_CAR: "Автомобільні масла",
    CATEGORY_OIL_MOTO: "Мото мастила (2T/4T)",
    CATEGORY_OIL_TRANS: "Трансмісійні масла",
    CATEGORY_OIL_SPECIAL: "Масла для генераторів та спецтехніки",
}

# 'tire' / 'battery' / 'oil' - визначає, які поля показувати у формах і таблицях
CATEGORY_TYPE = {
    CATEGORY_CAR: "tire",
    CATEGORY_MOTO: "tire",
    CATEGORY_BATTERY_CAR: "battery",
    CATEGORY_BATTERY_MOTO: "battery",
    CATEGORY_OIL_CAR: "oil",
    CATEGORY_OIL_MOTO: "oil",
    CATEGORY_OIL_TRANS: "oil",
    CATEGORY_OIL_SPECIAL: "oil",
}

CATEGORY_GROUPS = [
    ("Шини", [(CATEGORY_CAR, "Автошини"), (CATEGORY_MOTO, "Мотошини")]),
    ("Акумулятори", [(CATEGORY_BATTERY_CAR, "Авто АКБ"), (CATEGORY_BATTERY_MOTO, "Мото АКБ")]),
    ("Мастила", [
        (CATEGORY_OIL_CAR, "Автомасла"), (CATEGORY_OIL_MOTO, "Мотомасла"),
        (CATEGORY_OIL_TRANS, "Трансмісійні"), (CATEGORY_OIL_SPECIAL, "Для генераторів"),
    ]),
]

CATEGORY_ICONS = {
    CATEGORY_CAR: "🚗", CATEGORY_MOTO: "🏍️",
    CATEGORY_BATTERY_CAR: "🔋", CATEGORY_BATTERY_MOTO: "🔋",
    CATEGORY_OIL_CAR: "🛢️", CATEGORY_OIL_MOTO: "⛽",
    CATEGORY_OIL_TRANS: "⚙️", CATEGORY_OIL_SPECIAL: "🔧",
}
GROUP_ICONS = {"Шини": "🛞", "Акумулятори": "🔌", "Мастила": "🧴"}

# ---------------------------------------------------------------
# Шини
# ---------------------------------------------------------------

SEASONS = ["Літо", "Зима", "Всесезонна"]

CAR_WIDTHS = [155, 165, 175, 185, 195, 205, 215, 225, 235, 245, 255, 265, 275, 285, 315]
CAR_PROFILES = [30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
CAR_DIAMETERS = []
for d in range(13, 21):
    CAR_DIAMETERS.append(f"R{d}")
    CAR_DIAMETERS.append(f"R{d}C")

MOTO_SIZES = [
    "70/100 R19", "80/90 R21", "90/90 R21", "100/90 R19",
    "110/70 R17", "120/70 ZR17", "120/70 R17", "130/70 R17",
    "140/70 R17", "150/60 R17", "160/60 R17", "180/55 ZR17",
    "190/50 ZR17", "190/55 ZR17", "200/55 ZR17", "60/100 R14",
]

TIRE_BRANDS = sorted([
    "Michelin", "Bridgestone", "Continental", "Pirelli", "Goodyear",
    "Dunlop", "Hankook", "Yokohama", "Nokian", "Toyo", "Kumho", "Nexen",
    "Triangle", "Linglong", "Sailun", "Zeetex", "Doublestar", "Chengshan",
    "Aplus", "Powertrac", "Compasal", "Windforce", "Habilead", "RoadX",
    "Fullrun", "Landsail", "Westlake", "Ovation", "Headway", "Kapsen",
    "Mirage", "Leao", "Double Coin", "Rosava", "Premiorri", "Lassa",
    "Petlas", "Fulda", "Sava", "Gislaved", "Matador", "Maxxis", "Nankang",
    "Kenda", "Federal", "GT Radial", "Achilles", "Deestone", "Apollo",
    "MRF", "CEAT", "JK Tyre",
])

LOAD_INDEX_TABLE = {
    "70": 335, "71": 345, "72": 355, "73": 365, "74": 375, "75": 387, "76": 400, "77": 412,
    "78": 425, "79": 437, "80": 450, "81": 462, "82": 475, "83": 487, "84": 500, "85": 515,
    "86": 530, "87": 545, "88": 560, "89": 580, "90": 600, "91": 615, "92": 630, "93": 670,
    "94": 670, "95": 690, "96": 710, "97": 730, "98": 750, "99": 775, "100": 800, "101": 825,
    "102": 850, "103": 875, "104": 900, "105": 925, "106": 950, "107": 975, "108": 1000,
    "109": 1030, "110": 1060, "111": 1090, "112": 1120, "113": 1150, "114": 1180, "115": 1215,
    "116": 1250, "117": 1285, "118": 1320, "119": 1360, "120": 1400,
}
SPEED_INDEX_TABLE = {
    "L": 120, "M": 130, "N": 140, "P": 150, "Q": 160, "R": 170, "S": 180,
    "T": 190, "H": 210, "V": 240, "W": 270, "Y": 300, "ZR": 240,
}
LOAD_INDEXES = list(LOAD_INDEX_TABLE.keys())
SPEED_INDEXES = list(SPEED_INDEX_TABLE.keys())

# ---------------------------------------------------------------
# Акумулятори
# ---------------------------------------------------------------

BATTERY_BRANDS = sorted([
    "A-MEGA", "Westa", "Ista", "Forse", "SADA", "Feon", "Starta", "Electroistok", "Amper", "Volt",
    "Varta", "Bosch", "Topla", "TAB", "Exide", "Fiamm", "Moll", "Banner", "Centra", "Zubr",
    "Mutlu", "Platin", "Inci Aku", "Blizzaro", "Hugel", "President",
    "Rocket", "Medalist", "Hankook", "Solite", "Delkor", "Sebang",
    "Maxion", "Outdo", "Dynavolt", "Skyrich", "Leoch", "Challenger",
    "Yuasa", "FB (Furukawa Battery)", "GS Yuasa",
])

BATTERY_TRANSPORT_TYPES = ["Легковий", "Вантажний", "Мото", "Тяговий/AGM"]
BATTERY_POLARITY_OPTIONS = ["Пряма (R+/1)", "Зворотна (L+/0)"]
BATTERY_CASE_TYPES = ["Європейський (клеми втоплені)", "Азійський (клеми виступають над кришкою)"]

# ---------------------------------------------------------------
# Мастила
# ---------------------------------------------------------------

OIL_BRANDS = sorted([
    "Motul", "Mobil 1", "Shell", "Liqui Moly", "Castrol", "TotalEnergies", "Elf", "Ravenol",
    "Valvoline", "Mannol", "Kroon-Oil", "Total", "ZIC", "Eneos", "Comma", "Aral", "Fuchs",
    "Yukoil", "VAMP", "FanFaro", "Azelit", "Pemco", "Luxe",
])

OIL_VISCOSITY_TYPES = [
    "0W-20", "0W-30", "5W-20", "5W-30", "5W-40", "10W-30", "10W-40",
    "15W-40", "20W-50", "75W-80", "75W-90", "80W-90", "SAE 30", "Інша / Моноград",
]
OIL_BASE_TYPES = ["Синтетичне", "Напівсинтетичне", "Мінеральне", "НС-Синтетика (Гідрокрекінг)"]
OIL_VOLUMES = ["1 л", "4 л", "5 л", "10 л", "20 л", "60 л (Бочка)", "208 л (Бочка)"]

# ---------------------------------------------------------------
# Кольорові мітки позицій
# ---------------------------------------------------------------

# (код, назва, hex-колір)
COLOR_TAGS = [
    ("red", "Червона", "#E5534B"),
    ("orange", "Помаранчева", "#E5883B"),
    ("yellow", "Жовта", "#D9B341"),
    ("green", "Зелена", "#3E9B5C"),
    ("blue", "Синя", "#3E7BD9"),
    ("purple", "Фіолетова", "#9B59D9"),
    ("gray", "Сіра", "#8A8D93"),
]
COLOR_TAG_HEX = {code: hexval for code, _label, hexval in COLOR_TAGS}

# ---------------------------------------------------------------
# Розшифровки
# ---------------------------------------------------------------

def is_valid_dot_code(value: str) -> bool:
    value = (value or "").strip()
    if value == "":
        return True
    return value.isdigit() and len(value) in (3, 4)


def decode_dot_code(dot_code: str) -> str:
    """Розшифровує DOT-код - тиждень і рік виготовлення шини."""
    code = (dot_code or "").strip()
    if not code or not code.isdigit():
        return ""
    if len(code) == 4:
        week, year = int(code[:2]), int(code[2:])
        if 1 <= week <= 53:
            return f"{week}-й тиждень {2000 + year} року"
        return "формат не розпізнано"
    if len(code) == 3:
        week = int(code[:2])
        if 1 <= week <= 53:
            return f"{week}-й тиждень, 199{code[2]} рік (старий формат)"
        return "формат не розпізнано"
    return "формат не розпізнано"


def decode_li_si(load_index: str, speed_index: str) -> str:
    """Розшифровує індекси навантаження (LI) і швидкості (SI)."""
    parts = []
    kg = LOAD_INDEX_TABLE.get((load_index or "").strip())
    kmh = SPEED_INDEX_TABLE.get((speed_index or "").strip())
    if kg:
        parts.append(f"до {kg} кг/колесо")
    if kmh:
        parts.append(f"до {kmh} км/год")
    return " · ".join(parts)


def format_number(value) -> str:
    try:
        num = float(value)
    except (TypeError, ValueError):
        return str(value)
    if num == int(num):
        return str(int(num))
    return f"{num:.2f}".rstrip("0").rstrip(".")


ALL_KNOWN_BRANDS = sorted(set(TIRE_BRANDS) | set(BATTERY_BRANDS) | set(OIL_BRANDS))


# ---------------------------------------------------------------
# Друковані шаблони (чек / товарна та розрахункова накладні)
# ---------------------------------------------------------------
# Прості плейсхолдери у форматі {{ім'я}} - підставляються звичайною заміною
# тексту (без виконання коду), тому їх можна безпечно редагувати в налаштуваннях.

DOC_PLACEHOLDERS_HELP = [
    ("{{company_name}}", "Назва компанії"),
    ("{{company_address}}", "Адреса компанії"),
    ("{{company_phone}}", "Телефон компанії"),
    ("{{company_edrpou}}", "ЄДРПОУ / ІПН"),
    ("{{doc_number}}", "Номер документа"),
    ("{{date}}", "Дата і час"),
    ("{{customer}}", "Ім'я клієнта"),
    ("{{category_label}}", "Категорія товару"),
    ("{{items_table}}", "Таблиця позицій (генерується автоматично)"),
    ("{{total_qty}}", "Загальна кількість, шт"),
    ("{{total_sum}}", "Загальна сума, ₴"),
    ("{{amount_received}}", "Отримано від клієнта, ₴"),
    ("{{change_amount}}", "Решта, ₴"),
]

DEFAULT_RECEIPT_TEMPLATE = """<div class="receipt-header">
  <div class="receipt-company">{{company_name}}</div>
  <div class="muted">{{company_address}}</div>
  <div class="muted">{{company_phone}}</div>
  <h1 class="page-title" style="margin-top:14px;">Чек продажу</h1>
  <div class="muted">№ {{doc_number}} · {{date}} · {{category_label}}</div>
  <div class="muted">Клієнт: {{customer}}</div>
</div>
{{items_table}}
<div class="receipt-total">
  <span>Разом: {{total_qty}} шт.</span>
  <span class="receipt-total-sum">{{total_sum}}</span>
</div>
<div>Отримано: {{amount_received}} ₴ · Решта: {{change_amount}} ₴</div>
<div class="receipt-footer muted">Дякуємо за покупку!</div>"""

DEFAULT_GOODS_INVOICE_TEMPLATE = """<div class="receipt-header" style="text-align:left;">
  <div class="receipt-company">{{company_name}}</div>
  <div class="muted">{{company_address}} · {{company_phone}}</div>
  <div class="muted">ЄДРПОУ / ІПН: {{company_edrpou}}</div>
</div>
<h1 class="page-title" style="margin:16px 0 4px;">Товарна накладна № {{doc_number}}</h1>
<div class="muted" style="margin-bottom:14px;">від {{date}}</div>
<div style="margin-bottom:6px;"><b>Постачальник:</b> {{company_name}}</div>
<div style="margin-bottom:16px;"><b>Отримувач:</b> {{customer}}</div>
{{items_table}}
<div class="receipt-total">
  <span>Разом: {{total_qty}} шт.</span>
  <span class="receipt-total-sum">{{total_sum}}</span>
</div>
<div style="margin-top:12px;">Отримано: {{amount_received}} ₴ · Решта: {{change_amount}} ₴</div>
<div style="margin-top:40px;display:flex;justify-content:space-between;gap:24px;">
  <div style="flex:1;">Відпустив: _____________________</div>
  <div style="flex:1;">Отримав: _____________________</div>
</div>"""

DEFAULT_INVOICE_TEMPLATE = """<div class="receipt-header" style="text-align:left;">
  <div class="receipt-company">{{company_name}}</div>
  <div class="muted">{{company_address}} · {{company_phone}}</div>
  <div class="muted">ЄДРПОУ / ІПН: {{company_edrpou}}</div>
</div>
<h1 class="page-title" style="margin:16px 0 4px;">Розрахункова накладна № {{doc_number}}</h1>
<div class="muted" style="margin-bottom:14px;">від {{date}}</div>
<div style="margin-bottom:6px;"><b>Постачальник:</b> {{company_name}}</div>
<div style="margin-bottom:16px;"><b>Платник / отримувач:</b> {{customer}}</div>
{{items_table}}
<div class="receipt-total">
  <span>До сплати: {{total_qty}} шт.</span>
  <span class="receipt-total-sum">{{total_sum}}</span>
</div>
<div style="margin-top:12px;">Отримано: {{amount_received}} ₴ · Решта: {{change_amount}} ₴</div>
<div style="margin-top:40px;display:flex;justify-content:space-between;gap:24px;">
  <div style="flex:1;">Оплату прийняв: _____________________</div>
  <div style="flex:1;">Платник: ____________________________</div>
</div>"""

# ---------------------------------------------------------------
# Калькулятор перевзування (порівняння розмірів шин)
# ---------------------------------------------------------------

def tire_diameter_mm(width, profile, diameter_in):
    """Загальний зовнішній діаметр шини в мм (ширина W, профіль P%, посадковий діаметр в дюймах)."""
    sidewall = width * (profile / 100.0)
    return diameter_in * 25.4 + 2 * sidewall


def compare_tire_sizes(w1, p1, d1, w2, p2, d2):
    """Порівнює два розміри шин: діаметри, довжину кола, різницю у % і безпечність заміни."""
    dia1 = tire_diameter_mm(w1, p1, d1)
    dia2 = tire_diameter_mm(w2, p2, d2)
    circ1 = dia1 * math.pi
    circ2 = dia2 * math.pi
    diff_percent = (dia2 - dia1) / dia1 * 100
    rev_per_km1 = 1_000_000 / circ1
    rev_per_km2 = 1_000_000 / circ2
    # За загальноприйнятим правилом шинних майстерень безпечна різниця - до ±3%
    is_safe = abs(diff_percent) <= 3.0
    return {
        "diameter1": round(dia1, 1), "diameter2": round(dia2, 1),
        "circumference1": round(circ1, 1), "circumference2": round(circ2, 1),
        "rev_per_km1": round(rev_per_km1, 1), "rev_per_km2": round(rev_per_km2, 1),
        "diff_percent": round(diff_percent, 2),
        "speedo_error_percent": round(-diff_percent, 2),
        "is_safe": is_safe,
    }
