"""
OSINT Tools Catalog - 57 інструментів за категоріями розвідки
"""

TOOLS_CATALOG = {
    # GEOINT / IMINT - 8 інструментів
    "GEOINT": {
        "name": "Геолокація та Космічна розвідка (GEOINT)",
        "count": 8,
        "tools": [
            {
                "id": "geospy",
                "name": "GeoSpy.ai",
                "description": "Пікселева геолокація за фотографіями (AI)",
                "category": "GEOINT",
                "type": "Геолокація",
                "api": "✓"
            },
            {
                "id": "picarta",
                "name": "Picarta",
                "description": "AI-геолокація фотографій за архітектурою",
                "category": "GEOINT",
                "type": "AI Аналіз",
                "api": "✓"
            },
            {
                "id": "earthkit",
                "name": "EarthKit",
                "description": "Геолокація за архітектурними ознаками",
                "category": "GEOINT",
                "type": "Візуальний аналіз",
                "api": "✓"
            },
            {
                "id": "google_earth_pro",
                "name": "Google Earth Pro",
                "description": "Історичні супутникові знімки та таймлайн",
                "category": "GEOINT",
                "type": "Супутникові дані",
                "api": "✗"
            },
            {
                "id": "sentinel_hub",
                "name": "Sentinel Hub (Copernicus)",
                "description": "Актуальні супутникові знімки ESA",
                "category": "GEOINT",
                "type": "Супутникові дані",
                "api": "✓"
            },
            {
                "id": "suncalc",
                "name": "SunCalc",
                "description": "Аналіз тіней та позиції сонця",
                "category": "GEOINT",
                "type": "Тіньовий аналіз",
                "api": "✓"
            },
            {
                "id": "overpass_turbo",
                "name": "Overpass Turbo",
                "description": "Запити до OpenStreetMap геоданих",
                "category": "GEOINT",
                "type": "Геоданні",
                "api": "✓"
            },
            {
                "id": "wikimapia",
                "name": "Wikimapia",
                "description": "Спільна географічна база даних місцевостей",
                "category": "GEOINT",
                "type": "Геовіки",
                "api": "✓"
            }
        ]
    },

    # SIGINT / Інфраструктура - 10 інструментів
    "SIGINT": {
        "name": "Сигналізація та Інфраструктурна розвідка (SIGINT)",
        "count": 10,
        "tools": [
            {
                "id": "shodan",
                "name": "Shodan",
                "description": "Пошук IoT пристроїв та мережевої інфраструктури",
                "category": "SIGINT",
                "type": "Мережа",
                "api": "✓"
            },
            {
                "id": "censys",
                "name": "Censys",
                "description": "TLS сертифікати, хости та мережева інфраструктура",
                "category": "SIGINT",
                "type": "Мережа",
                "api": "✓"
            },
            {
                "id": "fofa",
                "name": "FOFA",
                "description": "Китайський аналог Shodan (китайські пристрої)",
                "category": "SIGINT",
                "type": "Мережа",
                "api": "✓"
            },
            {
                "id": "zoomeye",
                "name": "ZoomEye",
                "description": "Сканування та пошук мережевих пристроїв",
                "category": "SIGINT",
                "type": "Мережа",
                "api": "✓"
            },
            {
                "id": "securitytrails",
                "name": "SecurityTrails",
                "description": "Історичні DNS записи та WHOIS дані",
                "category": "SIGINT",
                "type": "DNS/WHOIS",
                "api": "✓"
            },
            {
                "id": "virustotal",
                "name": "VirusTotal",
                "description": "Аналіз файлів, URL та хешів (антивіруси)",
                "category": "SIGINT",
                "type": "Малвер-аналіз",
                "api": "✓"
            },
            {
                "id": "nmap",
                "name": "Nmap",
                "description": "Сканування портів та операційних систем",
                "category": "SIGINT",
                "type": "Мережа",
                "api": "✗"
            },
            {
                "id": "masscan",
                "name": "Masscan",
                "description": "Масштабне сканування портів (мільйони за хвилину)",
                "category": "SIGINT",
                "type": "Мережа",
                "api": "✗"
            },
            {
                "id": "dnsdumpster",
                "name": "DNSDumpster",
                "description": "Пошук поддоменів та DNS записів",
                "category": "SIGINT",
                "type": "DNS",
                "api": "✓"
            },
            {
                "id": "bgp_looking_glass",
                "name": "BGP Looking Glass",
                "description": "Аналіз BGP маршрутизації та AS номерів",
                "category": "SIGINT",
                "type": "BGP/AS",
                "api": "✓"
            }
        ]
    },

    # SOCMINT / HUMINT - 12 інструментів
    "SOCMINT": {
        "name": "Соціальна та Людська розвідка (SOCMINT/HUMINT)",
        "count": 12,
        "tools": [
            {
                "id": "maigret",
                "name": "Maigret",
                "description": "Пошук нікнейму на 3000+ веб-сайтах",
                "category": "SOCMINT",
                "type": "Нікнейм",
                "api": "✗"
            },
            {
                "id": "sherlock",
                "name": "Sherlock",
                "description": "Швидкий пошук нікнейму на 400+ сайтах",
                "category": "SOCMINT",
                "type": "Нікнейм",
                "api": "✗"
            },
            {
                "id": "whatsmyname",
                "name": "WhatsMyName",
                "description": "JSON база профілів для пошуку нікнеймів",
                "category": "SOCMINT",
                "type": "Нікнейм",
                "api": "✓"
            },
            {
                "id": "social_links",
                "name": "Social Links",
                "description": "Комерційна платформа для соціальної розвідки",
                "category": "SOCMINT",
                "type": "Платформа",
                "api": "✓"
            },
            {
                "id": "babel_x",
                "name": "Babel X",
                "description": "Мультимовний моніторинг соціальних мереж",
                "category": "SOCMINT",
                "type": "Моніторинг",
                "api": "✓"
            },
            {
                "id": "talkwalker",
                "name": "Talkwalker",
                "description": "Соціальне слухання та моніторинг брендів",
                "category": "SOCMINT",
                "type": "Моніторинг",
                "api": "✓"
            },
            {
                "id": "hunchly",
                "name": "Hunchly",
                "description": "Розширення для Firefox - збереження доказів OSINT",
                "category": "SOCMINT",
                "type": "Інструмент",
                "api": "✗"
            },
            {
                "id": "telegago",
                "name": "Telegago",
                "description": "Пошук повідомлень у Telegram каналах",
                "category": "SOCMINT",
                "type": "Telegram",
                "api": "✓"
            },
            {
                "id": "osint_industries",
                "name": "OSINT Industries",
                "description": "API з Anti-False Positive для соціальної розвідки",
                "category": "SOCMINT",
                "type": "Платформа",
                "api": "✓"
            },
            {
                "id": "reddit_search",
                "name": "Reddit Search",
                "description": "Пошук постів на Reddit за вмістом",
                "category": "SOCMINT",
                "type": "Reddit",
                "api": "✓"
            },
            {
                "id": "youtube_search",
                "name": "YouTube Search",
                "description": "Пошук відео та каналів на YouTube",
                "category": "SOCMINT",
                "type": "YouTube",
                "api": "✓"
            },
            {
                "id": "instagram_osint",
                "name": "Instagram OSINT",
                "description": "Аналіз Instagram профілів без API",
                "category": "SOCMINT",
                "type": "Instagram",
                "api": "✗"
            }
        ]
    },

    # FININT - Фінансова розвідка - 8 інструментів
    "FININT": {
        "name": "Фінансова розвідка (FININT)",
        "count": 8,
        "tools": [
            {
                "id": "opensanctions",
                "name": "OpenSanctions",
                "description": "Глобальні санкційні списки (2.1 млн сутностей)",
                "category": "FININT",
                "type": "Санкції",
                "api": "✓"
            },
            {
                "id": "castellum_ai",
                "name": "Castellum.AI",
                "description": "AI-AML та санкційні списки для KYC",
                "category": "FININT",
                "type": "AML/KYC",
                "api": "✓"
            },
            {
                "id": "rupep",
                "name": "RuPEP",
                "description": "База PEP Російської Федерації та Білорусі (16000+)",
                "category": "FININT",
                "type": "PEP",
                "api": "✓"
            },
            {
                "id": "youcontrol",
                "name": "YouControl",
                "description": "Українські компанії, зв'язки, PEP та санкції",
                "category": "FININT",
                "type": "Українське",
                "api": "✓"
            },
            {
                "id": "kharon",
                "name": "Kharon",
                "description": "Розкриття прихованих корпоративних мереж",
                "category": "FININT",
                "type": "Корпоративні мережі",
                "api": "✓"
            },
            {
                "id": "occrp_aleph",
                "name": "OCCRP Aleph",
                "description": "Глобальні витоки та розслідування корупції",
                "category": "FININT",
                "type": "Витоки",
                "api": "✓"
            },
            {
                "id": "dun_bradstreet",
                "name": "Dun & Bradstreet",
                "description": "Комерційні дані про компанії та їхні фінанси",
                "category": "FININT",
                "type": "Комерційні дані",
                "api": "✓"
            },
            {
                "id": "forbes_list",
                "name": "Forbes Billionaires",
                "description": "База багатіїв та їхніх активів",
                "category": "FININT",
                "type": "Багатство",
                "api": "✓"
            }
        ]
    },

    # Dark Web / Leaks - 10 інструментів
    "DARKWEB": {
        "name": "Dark Web та Витоки (DARKWEB)",
        "count": 10,
        "tools": [
            {
                "id": "ahmia",
                "name": "Ahmia",
                "description": "Пошуковик для .onion сайтів (Tor)",
                "category": "DARKWEB",
                "type": "Tor Search",
                "api": "✓"
            },
            {
                "id": "onionland",
                "name": "OnionLand",
                "description": "Індекс та пошук Tor мережі",
                "category": "DARKWEB",
                "type": "Tor Search",
                "api": "✓"
            },
            {
                "id": "darksearch",
                "name": "DarkSearch.io",
                "description": "Пошук у dark web paste сайтах",
                "category": "DARKWEB",
                "type": "Paste Search",
                "api": "✓"
            },
            {
                "id": "hudson_rock",
                "name": "Hudson Rock",
                "description": "Витоки облікових даних від взлому",
                "category": "DARKWEB",
                "type": "Leaks",
                "api": "✓"
            },
            {
                "id": "intelligence_x",
                "name": "Intelligence X",
                "description": "Архів deep/dark web та витоків",
                "category": "DARKWEB",
                "type": "Archive",
                "api": "✓"
            },
            {
                "id": "dehashed",
                "name": "Dehashed",
                "description": "База даних скомпрометованих облікових даних",
                "category": "DARKWEB",
                "type": "Leaks",
                "api": "✓"
            },
            {
                "id": "haveibeenpwned",
                "name": "Have I Been Pwned",
                "description": "Перевірка email на витоки паролів",
                "category": "DARKWEB",
                "type": "Leaks",
                "api": "✓"
            },
            {
                "id": "spycloud",
                "name": "SpyCloud",
                "description": "Пост-інфекційна розвідка та витоки",
                "category": "DARKWEB",
                "type": "Leaks",
                "api": "✓"
            },
            {
                "id": "pastebin_search",
                "name": "Pastebin Search",
                "description": "Пошук утікань на Pastebin",
                "category": "DARKWEB",
                "type": "Paste",
                "api": "✓"
            },
            {
                "id": "wastebin",
                "name": "WasteBin",
                "description": "Ще один пошук paste сайтів",
                "category": "DARKWEB",
                "type": "Paste",
                "api": "✓"
            }
        ]
    },

    # Email & Телефони - 4 інструменти
    "CONTACT": {
        "name": "Email та Контактна розвідка (CONTACT)",
        "count": 4,
        "tools": [
            {
                "id": "hunter_io",
                "name": "Hunter.io",
                "description": "Пошук email адрес за доменом компанії",
                "category": "CONTACT",
                "type": "Email",
                "api": "✓"
            },
            {
                "id": "phoneinfoga",
                "name": "PhoneInfoga v2",
                "description": "Розвідка за номером телефону (Go)",
                "category": "CONTACT",
                "type": "Телефон",
                "api": "✓"
            },
            {
                "id": "pipl",
                "name": "Pipl",
                "description": "Пошук людей за email, телефоном, іменем",
                "category": "CONTACT",
                "type": "Люди",
                "api": "✓"
            },
            {
                "id": "reverse_phone",
                "name": "ReversePhoneLookup",
                "description": "Зворотний пошук за номером телефону",
                "category": "CONTACT",
                "type": "Телефон",
                "api": "✓"
            }
        ]
    },

    # AI Платформи - 4 інструменти
    "AI": {
        "name": "AI та Агентні платформи (AI)",
        "count": 4,
        "tools": [
            {
                "id": "minimax_m2_5",
                "name": "MiniMax-M2.5",
                "description": "Агентний оркестратор (197k контекст)",
                "category": "AI",
                "type": "LLM",
                "api": "✓"
            },
            {
                "id": "blacksmith_ai",
                "name": "BlacksmithAI",
                "description": "Багатоагентний пентест та розвідка",
                "category": "AI",
                "type": "AgentAI",
                "api": "✓"
            },
            {
                "id": "perplexity",
                "name": "Perplexity Computer",
                "description": "AI координатор для OSINT завдань",
                "category": "AI",
                "type": "LLM",
                "api": "✓"
            },
            {
                "id": "deepface",
                "name": "DeepFace",
                "description": "Розпізнавання та порівняння облич",
                "category": "AI",
                "type": "CV",
                "api": "✗"
            }
        ]
    },

    # Транспорт & Трекування - 5 інструментів
    "TRANSPORT": {
        "name": "Транспорт та Трекування (TRANSPORT)",
        "count": 5,
        "tools": [
            {
                "id": "adsb_exchange",
                "name": "ADS-B Exchange",
                "description": "Нецензурований авіатрекінг в реальному часі",
                "category": "TRANSPORT",
                "type": "Авіація",
                "api": "✓"
            },
            {
                "id": "marinetraffic",
                "name": "MarineTraffic",
                "description": "AIS трекування суден у реальному часі",
                "category": "TRANSPORT",
                "type": "Морський",
                "api": "✓"
            },
            {
                "id": "vesselfinder",
                "name": "VesselFinder",
                "description": "Альтернативний трекер суден",
                "category": "TRANSPORT",
                "type": "Морський",
                "api": "✓"
            },
            {
                "id": "openrailway",
                "name": "OpenRailwayMap",
                "description": "Дані про залізничні мережі",
                "category": "TRANSPORT",
                "type": "Залізниця",
                "api": "✓"
            },
            {
                "id": "flightaware",
                "name": "FlightAware",
                "description": "Історія рейсів та трекування літаків",
                "category": "TRANSPORT",
                "type": "Авіація",
                "api": "✓"
            }
        ]
    },

    # Українські спеціалізовані - 3 інструменти
    "UKRAINE": {
        "name": "Українські спеціалізовані інструменти (UKRAINE)",
        "count": 3,
        "tools": [
            {
                "id": "ce_poshuk_bot",
                "name": "CE Poshuk Bot",
                "description": "Telegram бот для українських реєстрів",
                "category": "UKRAINE",
                "type": "Telegram",
                "api": "✓"
            },
            {
                "id": "warspy",
                "name": "WarSpy",
                "description": "Військова телеметрія та розвідка",
                "category": "UKRAINE",
                "type": "Військова",
                "api": "✓"
            },
            {
                "id": "nazk_sanctions",
                "name": "НАЗК War & Sanctions",
                "description": "Санкційний портал України та МТБІ",
                "category": "UKRAINE",
                "type": "Санкції",
                "api": "✓"
            }
        ]
    }
}

# Загальна статистика
TOTAL_TOOLS = 57
TOTAL_CATEGORIES = len(TOOLS_CATALOG)

# Лист всіх інструментів для швидкого пошуку
ALL_TOOLS_LIST = []
for category_key, category_data in TOOLS_CATALOG.items():
    for tool in category_data["tools"]:
        ALL_TOOLS_LIST.append(tool)
