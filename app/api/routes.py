from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import requests
import json
import random

router = APIRouter(prefix="/routes", tags=["routes"])

DGIS_KEY = "5b115410-b4f3-4016-89b2-bea1b2f2bc00"

GIGACHAT_AUTH = "MDE5ZTZmNzgtMjk2NC03Mjc5LWE1YjktZjU2ZDc1ZGJmMjRlOjljNzI2OTA1LTYyNzYtNDZjMC04NDMxLWU1NGU2YTg5YjdiNw=="


# =========================
# GIGACHAT
# =========================

def giga_request(text: str):

    try:

        auth_response = requests.post(
            "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
            headers={
                "Authorization": f"Basic {GIGACHAT_AUTH}",
                "RqUID": "12345678-1234-1234-1234-123456789012",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={
                "scope": "GIGACHAT_API_PERS"
            },
            verify=False
        )

        access_token = auth_response.json()["access_token"]

        prompt = f"""
Ты AI ассистент маршрутов по Нижнему Новгороду.

Определи категорию маршрута.

Варианты:

cafe
restaurant
museum
walk
romantic
night
parks
history
viewpoints
shopping
fastfood
pizza
burger
coffee
bars
students
family
river
theater
architecture

Ответь только одним словом.

Запрос пользователя:
{text}
"""

        response = requests.post(
            "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json={
                "model": "GigaChat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3
            },
            verify=False
        )

        result = response.json()["choices"][0]["message"]["content"].lower()

        return result

    except Exception:
        return "all"


# =========================
# ROUTES
# =========================

routes = {

    "cafe": [

        [
            [44.0022,56.3231],
            [44.0035,56.3239],
            [44.0048,56.3247],
            [44.0060,56.3255],
            [44.0073,56.3263],
            [44.0085,56.3271],
            [44.0098,56.3278]
        ],

        [
            [44.0010,56.3220],
            [44.0028,56.3228],
            [44.0046,56.3236],
            [44.0064,56.3244],
            [44.0082,56.3252],
            [44.0100,56.3260]
        ]
    ],

    "restaurant": [

        [
            [44.0030,56.3220],
            [44.0045,56.3228],
            [44.0060,56.3236],
            [44.0075,56.3244],
            [44.0090,56.3252],
            [44.0105,56.3260]
        ],

        [
            [44.0040,56.3250],
            [44.0055,56.3258],
            [44.0070,56.3266],
            [44.0085,56.3274],
            [44.0100,56.3282]
        ]
    ],

    "museum": [

        [
            [44.0010,56.3270],
            [44.0025,56.3265],
            [44.0040,56.3260],
            [44.0055,56.3255],
            [44.0070,56.3250],
            [44.0085,56.3245]
        ]
    ],

    "walk": [

        [
            [44.0020,56.3280],
            [44.0035,56.3275],
            [44.0050,56.3270],
            [44.0065,56.3265],
            [44.0080,56.3260],
            [44.0095,56.3255],
            [44.0110,56.3250]
        ]
    ],

    "romantic": [

        [
            [44.0030,56.3290],
            [44.0045,56.3284],
            [44.0060,56.3278],
            [44.0075,56.3272],
            [44.0090,56.3266],
            [44.0105,56.3260]
        ]
    ],

    "night": [

        [
            [44.0040,56.3230],
            [44.0055,56.3226],
            [44.0070,56.3222],
            [44.0085,56.3218],
            [44.0100,56.3214],
            [44.0115,56.3210]
        ]
    ],

    "parks": [

        [
            [44.0010,56.3300],
            [44.0025,56.3295],
            [44.0040,56.3290],
            [44.0055,56.3285],
            [44.0070,56.3280],
            [44.0085,56.3275]
        ]
    ],

    "history": [

        [
            [44.0020,56.3275],
            [44.0035,56.3270],
            [44.0050,56.3265],
            [44.0065,56.3260],
            [44.0080,56.3255],
            [44.0095,56.3250]
        ]
    ],

    "viewpoints": [

        [
            [44.0015,56.3310],
            [44.0030,56.3304],
            [44.0045,56.3298],
            [44.0060,56.3292],
            [44.0075,56.3286],
            [44.0090,56.3280]
        ]
    ],

    "shopping": [

        [
            [44.0100,56.3230],
            [44.0115,56.3238],
            [44.0130,56.3246],
            [44.0145,56.3254],
            [44.0160,56.3262]
        ]
    ],

    "bars": [

        [
            [44.0060,56.3200],
            [44.0075,56.3206],
            [44.0090,56.3212],
            [44.0105,56.3218],
            [44.0120,56.3224]
        ]
    ],

    "river": [

        [
            [44.0005,56.3320],
            [44.0020,56.3314],
            [44.0035,56.3308],
            [44.0050,56.3302],
            [44.0065,56.3296],
            [44.0080,56.3290]
        ]
    ],

    "all": [

        [
            [44.0022,56.3231],
            [44.0035,56.3239],
            [44.0048,56.3247],
            [44.0060,56.3255],
            [44.0073,56.3263],
            [44.0085,56.3271],
            [44.0098,56.3278]
        ],

        [
            [44.0030,56.3220],
            [44.0045,56.3228],
            [44.0060,56.3236],
            [44.0075,56.3244],
            [44.0090,56.3252],
            [44.0105,56.3260]
        ]
    ]
}


# =========================
# POINT GENERATOR
# =========================

def generate_points(theme_routes, hours=1):

    count = 5

    if hours >= 2:
        count = 7

    if hours >= 3:
        count = 10

    all_points = []

    for route in theme_routes:
        all_points.extend(route)

    random.shuffle(all_points)

    return all_points[:count]


# =========================
# HOME
# =========================

@router.get("/", response_class=HTMLResponse)
async def home():

    return """
    <html>

    <head>

        <title>NNgo AI</title>

        <style>

            body{
                background:#07132b;
                font-family:Arial;
                color:white;
                padding:50px;
            }

            h1{
                font-size:72px;
            }

            input{
                width:500px;
                padding:20px;
                border-radius:15px;
                border:none;
                font-size:24px;
            }

            button{
                padding:20px 40px;
                border:none;
                border-radius:15px;
                background:#2563eb;
                color:white;
                font-size:24px;
                cursor:pointer;
                margin-left:15px;
            }

        </style>

    </head>

    <body>

        <h1>NNgo AI Route</h1>

        <form action="/routes/request">

            <input
                type="text"
                name="text"
                placeholder="Куда хочешь пойти?"
            >

            <button type="submit">
                Найти маршрут
            </button>

        </form>

    </body>

    </html>
    """


# =========================
# REQUEST
# =========================

@router.get("/request", response_class=HTMLResponse)
async def request_route(text: str):

    result = giga_request(text)

    hours = 1

    if "2 час" in text:
        hours = 2

    elif "3 час" in text:
        hours = 3

    elif "вечер" in text:
        hours = 2

    elif "долго" in text:
        hours = 3


    if "cafe" in result:
        theme = "cafe"

    elif "restaurant" in result:
        theme = "restaurant"

    elif "museum" in result:
        theme = "museum"

    elif "walk" in result:
        theme = "walk"

    elif "romantic" in result:
        theme = "romantic"

    elif "night" in result:
        theme = "night"

    elif "parks" in result:
        theme = "parks"

    elif "history" in result:
        theme = "history"

    elif "viewpoints" in result:
        theme = "viewpoints"

    elif "shopping" in result:
        theme = "shopping"

    elif "bars" in result:
        theme = "bars"

    elif "river" in result:
        theme = "river"

    else:
        theme = "all"

    return await build_route(theme, hours)


# =========================
# MAP
# =========================

@router.get("/route", response_class=HTMLResponse)
async def build_route(theme: str = "all", hours: int = 1):

    theme_routes = routes.get(theme, routes["all"])

    points = generate_points(theme_routes, hours)

    return f"""

    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="utf-8">

        <title>NNgo Route</title>

        <script src="https://mapgl.2gis.com/api/js/v1"></script>

        <script src="https://unpkg.com/@2gis/mapgl-directions@^1/dist/directions.js"></script>

        <style>

            html, body, #map {{
                margin:0;
                width:100%;
                height:100%;
            }}

        </style>

    </head>

    <body>

        <div id="map"></div>

        <script>

            const map = new mapgl.Map('map', {{
                center: [44.0059,56.3269],
                zoom: 13,
                key: '{DGIS_KEY}'
            }});

            const points = {json.dumps(points)};

            points.forEach(point => {{

                new mapgl.Marker(map, {{
                    coordinates: point
                }});

            }});

            const directions = new window.Directions(map, {{

                directionsApiKey: '{DGIS_KEY}'

            }});

            directions.carRoute({{

                points: points

            }});

        </script>

    </body>

    </html>

    """