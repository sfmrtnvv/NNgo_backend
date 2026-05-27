from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter(
    prefix="/alisa",
    tags=["Alisa"]
)


class AlisaRequest(BaseModel):
    command: str


places = {

    "центр": [

        {
            "name": "Нижегородский кремль",
            "map": "https://yandex.ru/maps/?text=Нижегородский+кремль"
        },

        {
            "name": "Чкаловская лестница",
            "map": "https://yandex.ru/maps/?text=Чкаловская+лестница"
        },

        {
            "name": "Большая Покровская",
            "map": "https://yandex.ru/maps/?text=Большая+Покровская"
        },

        {
            "name": "Рождественская улица",
            "map": "https://yandex.ru/maps/?text=Рождественская+улица+Нижний+Новгород"
        },

        {
            "name": "Верхне-Волжская набережная",
            "map": "https://yandex.ru/maps/?text=Верхне-Волжская+набережная"
        },

        {
            "name": "Нижне-Волжская набережная",
            "map": "https://yandex.ru/maps/?text=Нижне-Волжская+набережная"
        },

        {
            "name": "Стрелка",
            "map": "https://yandex.ru/maps/?text=Стрелка+Нижний+Новгород"
        },

        {
            "name": "Александровский сад",
            "map": "https://yandex.ru/maps/?text=Александровский+сад+Нижний+Новгород"
        }
    ],

    "парки": [

        {
            "name": "Парк Швейцария",
            "map": "https://yandex.ru/maps/?text=Парк+Швейцария+Нижний+Новгород"
        },

        {
            "name": "Парк Кулибина",
            "map": "https://yandex.ru/maps/?text=Парк+Кулибина"
        },

        {
            "name": "Автозаводский парк",
            "map": "https://yandex.ru/maps/?text=Автозаводский+парк"
        },

        {
            "name": "Сормовский парк",
            "map": "https://yandex.ru/maps/?text=Сормовский+парк"
        },

        {
            "name": "Парк Победы",
            "map": "https://yandex.ru/maps/?text=Парк+Победы+Нижний+Новгород"
        },

        {
            "name": "Щелоковский хутор",
            "map": "https://yandex.ru/maps/?text=Щелоковский+хутор"
        }
    ],

    "музеи": [

        {
            "name": "Музей ГАЗ",
            "map": "https://yandex.ru/maps/?text=Музей+ГАЗ"
        },

        {
            "name": "Русский музей фотографии",
            "map": "https://yandex.ru/maps/?text=Русский+музей+фотографии"
        },

        {
            "name": "Усадьба Рукавишниковых",
            "map": "https://yandex.ru/maps/?text=Усадьба+Рукавишниковых"
        },

        {
            "name": "Нижегородский художественный музей",
            "map": "https://yandex.ru/maps/?text=Нижегородский+художественный+музей"
        },

        {
            "name": "Технический музей",
            "map": "https://yandex.ru/maps/?text=Технический+музей+Нижний+Новгород"
        }
    ],

    "еда": [

        {
            "name": "Кафе Молоко",
            "map": "https://yandex.ru/maps/?text=Кафе+Молоко+Нижний+Новгород"
        },

        {
            "name": "Dodici Italy",
            "map": "https://yandex.ru/maps/?text=Dodici+Italy+Нижний+Новгород"
        },

        {
            "name": "Mitrich Steakhouse",
            "map": "https://yandex.ru/maps/?text=Mitrich+Steakhouse"
        },

        {
            "name": "Biblioteca",
            "map": "https://yandex.ru/maps/?text=Biblioteca+Нижний+Новгород"
        },

        {
            "name": "Безухов",
            "map": "https://yandex.ru/maps/?text=Безухов+Нижний+Новгород"
        },

        {
            "name": "Самурай",
            "map": "https://yandex.ru/maps/?text=Самурай+Нижний+Новгород"
        }
    ],

    "развлечения": [

        {
            "name": "Нижегородский цирк",
            "map": "https://yandex.ru/maps/?text=Нижегородский+цирк"
        },

        {
            "name": "Планетарий",
            "map": "https://yandex.ru/maps/?text=Планетарий+Нижний+Новгород"
        },

        {
            "name": "Аквапарк Океанис",
            "map": "https://yandex.ru/maps/?text=Океанис+Нижний+Новгород"
        },

        {
            "name": "Канатная дорога",
            "map": "https://yandex.ru/maps/?text=Канатная+дорога+Нижний+Новгород"
        }
    ]
}


def generate_route():

    route = []

    route.append(random.choice(places["центр"]))
    route.append(random.choice(places["парки"]))
    route.append(random.choice(places["музеи"]))
    route.append(random.choice(places["еда"]))
    route.append(random.choice(places["развлечения"]))

    return route


@router.post("/")
async def alisa_webhook(data: AlisaRequest):

    text = data.command.lower()

    # Генерация маршрута
    if "маршрут" in text or "прогул" in text:

        route = generate_route()

        answer = "Ваш туристический маршрут по Нижнему Новгороду:\n\n"

        for index, place in enumerate(route, start=1):

            answer += (
                f"{index}. {place['name']}\n"
                f"{place['map']}\n\n"
            )

    # Кремль
    elif "кремль" in text:

        answer = (
            "Нижегородский кремль:\n"
            "https://yandex.ru/maps/?text=Нижегородский+кремль"
        )

    # Парк
    elif "парк" in text:

        park = random.choice(places["парки"])

        answer = (
            f"{park['name']}\n"
            f"{park['map']}"
        )

    # Кафе
    elif "кафе" in text or "поесть" in text:

        cafe = random.choice(places["еда"])

        answer = (
            f"{cafe['name']}\n"
            f"{cafe['map']}"
        )

    # Музей
    elif "музей" in text:

        museum = random.choice(places["музеи"])

        answer = (
            f"{museum['name']}\n"
            f"{museum['map']}"
        )

    # Развлечения
    elif "развлеч" in text:

        fun = random.choice(places["развлечения"])

        answer = (
            f"{fun['name']}\n"
            f"{fun['map']}"
        )

    # Приветствие
    elif "привет" in text:

        answer = (
            "Привет! Я AI-гид по Нижнему Новгороду.\n"
            "Я могу построить туристический маршрут."
        )

    else:

        answer = (
            "Я могу:\n"
            "- построить маршрут\n"
            "- показать парк\n"
            "- найти музей\n"
            "- предложить кафе\n"
            "- показать развлечения"
        )

    return {
        "response": {
            "text": answer,
            "end_session": False
        }
    }