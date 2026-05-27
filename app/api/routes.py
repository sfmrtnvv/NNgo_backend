from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

router = APIRouter()


# =========================
# МОДЕЛЬ ДАННЫХ
# =========================

class AlisaRequest(BaseModel):
    command: str


# =========================
# МАРШРУТЫ
# =========================

routes_data = {

    "центр": [
        [56.328674, 44.002018],  # Кремль
        [56.328072, 44.005517],  # Чкаловская лестница
        [56.324062, 44.000168],  # Покровская
        [56.321169, 43.999050],  # Рождественская
        [56.317500, 44.015000],  # Набережная
    ],

    "парки": [
        [56.296503, 43.936059],  # Швейцария
        [56.314839, 43.989769],  # Кулибина
        [56.329949, 44.024129],  # Александровский сад
    ],

    "музеи": [
        [56.325453, 44.006210],
        [56.321916, 44.001123],
        [56.327534, 44.011429],
    ]
}


# =========================
# ОСНОВНАЯ КАРТА
# =========================

@router.get("/map", response_class=HTMLResponse)
async def show_map():

    return create_map(routes_data["центр"])


# =========================
# ДИНАМИЧЕСКИЙ МАРШРУТ
# =========================

@router.get("/route/{route_name}", response_class=HTMLResponse)
async def dynamic_route(route_name: str):

    points = routes_data.get(route_name)

    if not points:
        return HTMLResponse("<h1>Маршрут не найден</h1>")

    return create_map(points)


# =========================
# ALISA AI
# =========================

@router.post("/alisa/")
async def alisa(data: AlisaRequest):

    command = data.command.lower()

    route_name = "центр"

    if "парк" in command:
        route_name = "парки"

    elif "музе" in command:
        route_name = "музеи"

    elif "центр" in command:
        route_name = "центр"

    map_url = f"http://localhost:8000/routes/route/{route_name}"

    return {
        "response": {
            "text": f"Маршрут построен: {map_url}",
            "end_session": False
        }
    }


# =========================
# СОЗДАНИЕ КАРТЫ
# =========================

def create_map(points):

    return f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<title>NNgo Route</title>

<script src="https://api-maps.yandex.ru/2.1/?lang=ru_RU"></script>

<style>

html, body, #map {{
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
}}

</style>

</head>

<body>

<div id="map"></div>

<script>

ymaps.ready(init);

function init() {{

    const map = new ymaps.Map("map", {{
        center: [56.326797, 44.006516],
        zoom: 13
    }});

    const points = {points};

    points.forEach(point => {{

        const placemark = new ymaps.Placemark(point);

        map.geoObjects.add(placemark);
    }});

    const routeLine = new ymaps.Polyline(
        points,
        {{}},
        {{
            strokeColor: "#ff0000",
            strokeWidth: 6,
            strokeOpacity: 0.9
        }}
    );

    map.geoObjects.add(routeLine);

    map.setBounds(routeLine.geometry.getBounds(), {{
        checkZoomRange: true
    }});
}}

</script>

</body>

</html>
"""