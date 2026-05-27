"""seed reference data and 15 spots

Revision ID: 20260525_0002
Revises: 20260525_0001
Create Date: 2026-05-25

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260525_0002"
down_revision: Union[str, None] = "20260525_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    def insert_ignore(table: str, rows: list[dict]) -> None:
        if not rows:
            return
        cols = list(rows[0].keys())
        placeholders = ", ".join(f":{c}" for c in cols)
        col_list = ", ".join(cols)
        for row in rows:
            conn.execute(
                sa.text(
                    f"INSERT IGNORE INTO {table} ({col_list}) VALUES ({placeholders})"
                ),
                row,
            )

    insert_ignore(
        "company_types",
        [
            {"name": "С семьей/ детьми"},
            {"name": "С друзьями"},
            {"name": "Со второй половинкой"},
            {"name": "С незнакомцем"},
            {"name": "Один"},
        ],
    )
    insert_ignore(
        "budget_types",
        [
            {"name": "до 1000 руб.", "min_price": 0, "max_price": 1000},
            {"name": "1000-4000 руб.", "min_price": 1000, "max_price": 4000},
            {"name": "от 5000 руб.", "min_price": 5000, "max_price": None},
        ],
    )
    insert_ignore("rest_types", [{"name": "Активный"}, {"name": "Спокойный"}])
    insert_ignore(
        "walk_statuses",
        [
            {"name": "Запланирована"},
            {"name": "В процессе"},
            {"name": "Завершена"},
            {"name": "Отменена"},
        ],
    )
    insert_ignore(
        "application_statuses",
        [
            {"name": "Одобрена"},
            {"name": "Отклонена"},
            {"name": "На рассмотрении"},
        ],
    )
    categories = [
        ("Движение к природе", "Парки, набережные, виды на Волгу и Оку"),
        ("Культурный код", "Музеи, театры, выставочные площадки"),
        ("Нижегородская классика", "Кремль, исторический центр, главные улицы"),
        ("Стрит-арт и дворики", "Неочевидные маршруты и городская среда"),
        ("Духовное наследие", "Храмы и места памяти"),
        ("Гастрономический Нижний", "Кафе, рынки, локальные вкусы"),
        ("Ритмы Нижнего: события города", "Площадки для прогулок с городскими событиями"),
        ("Индустриальный Нижний", "Постиндустриальные локации и архитектура"),
    ]
    for name, description in categories:
        conn.execute(
            sa.text(
                "INSERT IGNORE INTO categories (name, description) VALUES (:name, :description)"
            ),
            {"name": name, "description": description},
        )

    spots = [
        ("Нижегородский кремль", "Главная крепость города на высоком берегу Волги, музеи и панорамы.", 56.3281700, 43.9998300),
        ("Чкаловская лестница", "Монументальная лестница к Волге, символ Нижнего и вид на реку.", 56.3261000, 44.0052400),
        ("Улица Большая Покровская", "Пешеходная улица с кафе, театрами и городской атмосферой.", 56.3209000, 44.0019000),
        ("Усадьба Рукавишниковых", "Дворянская усадьба XIX века, музей и архитектурный ансамбль.", 56.3234000, 44.0061000),
        ("Строгановская (Рождественская) церковь", "Строгановское барокко на Рождественской улице.", 56.3280000, 44.0085000),
        ("Канатная дорога через Волгу", "Канатная дорога с видами на Волгу и город.", 56.3302000, 43.9981000),
        ("Нижегородская ярмарка", "Исторический комплекс ярмарки и выставочные пространства.", 56.3401000, 43.9542000),
        ("Стрелка (место слияния Оки и Волги)", "Смотровая площадка у слияния Оки и Волги.", 56.3362000, 43.9815000),
        ("Собор Александра Невского", "Купольный собор на Стрелке, один из символов города.", 56.3146000, 44.0528000),
        ("Пакгаузы (концертные залы)", "Культурный кластер на набережной, концерты и фестивали.", 56.3365000, 43.9770000),
        ("Здание Госбанка", "Архитектурный памятник конструктивизма на площади Минина.", 56.3265000, 44.0055000),
        ("Верхне-Волжская набережная", "Набережная с видами на Волгу, прогулочная зона.", 56.3340000, 43.9890000),
        ("Площадь Минина и Пожарского", "Главная площадь города у Кремля.", 56.3285000, 44.0020000),
        ("Пешеходный мост через Почаинский овраг", "Пешеходный мост и вид на исторический овраг.", 56.3250000, 44.0040000),
        ("Церковь Ильи Пророка", "Памятник древнерусского зодчества на Ильинской улице.", 56.3278000, 44.0095000),
    ]
    for name, description, lat, lon in spots:
        exists = conn.execute(
            sa.text("SELECT 1 FROM spots WHERE name = :name LIMIT 1"),
            {"name": name},
        ).scalar()
        if not exists:
            conn.execute(
                sa.text(
                    "INSERT INTO spots (name, description, latitude, longitude) "
                    "VALUES (:name, :description, :latitude, :longitude)"
                ),
                {
                    "name": name,
                    "description": description,
                    "latitude": lat,
                    "longitude": lon,
                },
            )


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM spots"))
    op.execute(sa.text("DELETE FROM categories"))
    op.execute(sa.text("DELETE FROM application_statuses"))
    op.execute(sa.text("DELETE FROM walk_statuses"))
    op.execute(sa.text("DELETE FROM rest_types"))
    op.execute(sa.text("DELETE FROM budget_types"))
    op.execute(sa.text("DELETE FROM company_types"))
