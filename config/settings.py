from pathlib import Path
from typing import Literal
from datetime import datetime, timezone, timedelta

PAGE_TITLE = "Idea Finder"
LAYOUT: Literal["centered", "wide"] = "centered"
SIDEBAR_STATE: Literal["auto", "expanded", "collapsed"] = "expanded"

# Data
BASE_DIR = Path(__file__).resolve().parent.parent
Idea_Excel_File = BASE_DIR / "data" / "Idea.csv"

# Asset
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"
CSS_PATH = ASSETS_DIR / "style.css"

# API


# Cache
TTL_VALUES = {
    "TTL_5MIN": 300,       # 5 minutes
    "TTL_30MIN": 1800,     # 30 minutes
    "TTL_1HOUR": 3600,     # 1 hour
    "TTL_24HOUR": 86400,   # 24 hours
    "TTL_1WEEK": 604800    # 7 days
}

HEADERS = {
    'Host': 'www.singaporepools.com.sg',
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
}

sg_tz = timezone(timedelta(hours=8))
TIME_TABS = ["📊 All", "📅 6 Months", "📆 14 Days", "📆 1 Month", "📈 1 Year"]
TIME_DAYS = {"📅 6 Months": 180, "📆 14 Days": 14, "📆 1 Month": 30, "📈 1 Year": 365}
TREND_TABS = ["📅 2 Months", "📅 6 Months", "📅 14 Days", "📆 1 Month", "📈 1 Year"]
TREND_DAYS = {"📅 2 Months": 60, "📅 6 Months": 180, "📅 14 Days": 14, "📆 1 Month": 30, "📈 1 Year": 365}

MENU = {
    "Dashboard": {
        "icon": "house-heart-fill",
        "handler_name": "dashboard"
    },
    "About": {
        "icon": "info-circle-fill",
        "handler_name": "about"
    }
}