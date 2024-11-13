from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

COUNTRY_FLAGS = {
    "Australia": "🇦🇺",
    "Brazil": "🇧🇷",
    "Egypt": "🇪🇬",
    "France": "🇫🇷",
    "Germany": "🇩🇪",
    "Malaysia": "🇲🇾",
    "Russia": "🇷🇺",
    "South Africa": "🇿🇦",
    "Thailand": "🇹🇭",
    "Turkey": "🇹🇷",
    "USA": "🇺🇸"
}