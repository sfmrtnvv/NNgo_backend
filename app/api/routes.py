from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(
    prefix="/routes",
    tags=["routes"]
)


@router.get("/")
async def root():
    return {"message": "NNgo API работает"}


@router.get("/request")
async def request_route(text: str = Query(...)):

    text = text.lower()

    if "кофе" in text:
        theme = "cafe"

    elif "ресторан" in text:
        theme = "restaurant"

    elif "парк" in text:
        theme = "park"

    elif "музей" in text:
        theme = "museum"

    else:
        theme = "center"

    return RedirectResponse(
        url=f"/routes/route?theme={theme}"
    )


@router.get("/route", response_class=HTMLResponse)
async def build_route(theme: str = "center"):

    routes = {

        "cafe": [
            [56.3285, 44.0020],
            [56.3234, 44.0087],
            [56.3208, 44.0065],
            [56.3249, 44.0210]
        ],

        "restaurant": [
            [56.3270, 44.0040],
            [56.3290, 44.0100],
            [56.3250, 44.0180]
        ],

        "park": [
            [56.3260, 44.0050],
            [56.3190, 44.0150],
            [56.3150, 44.0200]
        ],

        "museum": [
            [56.3272, 44.0022],
            [56.3288, 44.0085],
            [56.3250, 44.0130]
        ],

        "center": [
            [56.3269, 44.0059],
            [56.3275, 44.0080]
        ]
    }

    points = routes.get(theme, routes["center"])

    return f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<title>NNgo Route</title>

<link
 rel="stylesheet"
 href="https://unpkg.com/leaflet/dist/leaflet.css"
/>

<link
 rel="stylesheet"
 href="https://unpkg.com/leaflet-routing-machine/dist/leaflet-routing-machine.css"
/>

<style>

html, body {{
    margin:0;
    width:100%;
    height:100%;
}}

#map {{
    width:100%;
    height:100vh;
}}

</style>

</head>

<body>

<div id="map"></div>

<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<script src="https://unpkg.com/leaflet-routing-machine/dist/leaflet-routing-machine.js"></script>

<script>

const points = {points};

const map = L.map('map').setView(
    [56.3269, 44.0059],
    13
);

L.tileLayer(
    'https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',
    {{
        attribution: 'OpenStreetMap'
    }}
).addTo(map);


L.Routing.control({{

    waypoints: points.map(
        p => L.latLng(p[0], p[1])
    ),

    routeWhileDragging: false,
    addWaypoints: false,
    draggableWaypoints: false,
    fitSelectedRoutes: true,
    show: false,

    lineOptions: {{
        styles: [
            {{
                color: 'red',
                opacity: 0.8,
                weight: 6
            }}
        ]
    }}

}}).addTo(map);

</script>

</body>
</html>
"""