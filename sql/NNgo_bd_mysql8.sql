-- =============================================================================
-- NNgo — production schema (MySQL 8.0+)
-- Charset: utf8mb4 | Engine: InnoDB | No circular FK (routes <-> walks)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS nngo_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE nngo_db;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- -----------------------------------------------------------------------------
-- Reference / lookup tables (no dependencies on domain entities)
-- -----------------------------------------------------------------------------

CREATE TABLE company_types (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_company_types_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE budget_types (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    min_price   INT UNSIGNED NULL,
    max_price   INT UNSIGNED NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_budget_types_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE rest_types (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_rest_types_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE categories (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    description TEXT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_categories_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE walk_statuses (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_walk_statuses_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE application_statuses (
    id          TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(50) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_application_statuses_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- Users
-- -----------------------------------------------------------------------------

CREATE TABLE users (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    vk_id           BIGINT UNSIGNED NULL,
    email           VARCHAR(255) NULL,
    password_hash   VARCHAR(255) NULL,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    birth_date      DATE NULL,
    age_verified    TINYINT(1) NOT NULL DEFAULT 0,
    avatar_url      TEXT NULL,
    bio             TEXT NULL,
    city            VARCHAR(100) NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_vk_id (vk_id),
    UNIQUE KEY uq_users_email (email),
    CONSTRAINT chk_users_auth CHECK (
        vk_id IS NOT NULL
        OR (email IS NOT NULL AND password_hash IS NOT NULL)
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- Routes & spots (routes do NOT reference walks — no cycle)
-- -----------------------------------------------------------------------------

CREATE TABLE spots (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name            VARCHAR(255) NOT NULL,
    description     TEXT NULL,
    latitude        DECIMAL(10, 7) NULL,
    longitude       DECIMAL(10, 7) NULL,
    image_url       TEXT NULL,
    external_url    TEXT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_spots_geo (latitude, longitude)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE routes (
    id                      BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name                    VARCHAR(255) NOT NULL,
    description             TEXT NOT NULL,
    estimated_time_minutes  INT UNSIGNED NULL,
    category_id             INT UNSIGNED NULL,
    budget_type_id          INT UNSIGNED NULL,
    rest_type_id            INT UNSIGNED NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_routes_category (category_id),
    KEY idx_routes_budget (budget_type_id),
    CONSTRAINT fk_routes_category
        FOREIGN KEY (category_id) REFERENCES categories (id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_routes_budget_type
        FOREIGN KEY (budget_type_id) REFERENCES budget_types (id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_routes_rest_type
        FOREIGN KEY (rest_type_id) REFERENCES rest_types (id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE route_spots (
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    route_id    BIGINT UNSIGNED NOT NULL,
    spot_id     BIGINT UNSIGNED NOT NULL,
    spot_order  INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_route_spots_route_spot (route_id, spot_id),
    UNIQUE KEY uq_route_spots_route_order (route_id, spot_order),
    CONSTRAINT fk_route_spots_route
        FOREIGN KEY (route_id) REFERENCES routes (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_route_spots_spot
        FOREIGN KEY (spot_id) REFERENCES spots (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- Walks (only walks -> routes, never routes -> walks)
-- -----------------------------------------------------------------------------

CREATE TABLE walks (
    id                  BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    route_id            BIGINT UNSIGNED NULL,
    first_user_id       BIGINT UNSIGNED NOT NULL,
    second_user_id      BIGINT UNSIGNED NULL,
    company_type_id     INT UNSIGNED NOT NULL,
    status_id           INT UNSIGNED NOT NULL,
    started_at          DATETIME NULL,
    ended_at            DATETIME NULL,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_walks_first_user (first_user_id),
    KEY idx_walks_second_user (second_user_id),
    KEY idx_walks_status (status_id),
    KEY idx_walks_route (route_id),
    CONSTRAINT fk_walks_route
        FOREIGN KEY (route_id) REFERENCES routes (id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_walks_first_user
        FOREIGN KEY (first_user_id) REFERENCES users (id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_walks_second_user
        FOREIGN KEY (second_user_id) REFERENCES users (id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_walks_company_type
        FOREIGN KEY (company_type_id) REFERENCES company_types (id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_walks_status
        FOREIGN KEY (status_id) REFERENCES walk_statuses (id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_walks_different_users CHECK (
        second_user_id IS NULL OR first_user_id <> second_user_id
    ),
    CONSTRAINT chk_walks_time_range CHECK (
        ended_at IS NULL OR started_at IS NULL OR ended_at >= started_at
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE walk_applications (
    id                      BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    walk_id                 BIGINT UNSIGNED NOT NULL,
    applicant_user_id       BIGINT UNSIGNED NOT NULL,
    application_status_id   TINYINT UNSIGNED NOT NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_walk_applications_walk_user (walk_id, applicant_user_id),
    KEY idx_walk_applications_status (application_status_id),
    CONSTRAINT fk_walk_applications_walk
        FOREIGN KEY (walk_id) REFERENCES walks (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_walk_applications_user
        FOREIGN KEY (applicant_user_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_walk_applications_status
        FOREIGN KEY (application_status_id) REFERENCES application_statuses (id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- Social: matches, chats, messages
-- -----------------------------------------------------------------------------

CREATE TABLE matches (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    first_user_id   BIGINT UNSIGNED NOT NULL,
    second_user_id  BIGINT UNSIGNED NOT NULL,
    is_mutual       TINYINT(1) NOT NULL DEFAULT 0,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_matches_users (first_user_id, second_user_id),
    KEY idx_matches_second_user (second_user_id),
    CONSTRAINT fk_matches_first_user
        FOREIGN KEY (first_user_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_matches_second_user
        FOREIGN KEY (second_user_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_matches_user_order CHECK (first_user_id < second_user_id),
    CONSTRAINT chk_matches_different_users CHECK (first_user_id <> second_user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE chats (
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    match_id    BIGINT UNSIGNED NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_chats_match_id (match_id),
    CONSTRAINT fk_chats_match
        FOREIGN KEY (match_id) REFERENCES matches (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE chat_participants (
    chat_id     BIGINT UNSIGNED NOT NULL,
    user_id     BIGINT UNSIGNED NOT NULL,
    joined_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (chat_id, user_id),
    CONSTRAINT fk_chat_participants_chat
        FOREIGN KEY (chat_id) REFERENCES chats (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_chat_participants_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE messages (
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    chat_id     BIGINT UNSIGNED NOT NULL,
    sender_id   BIGINT UNSIGNED NOT NULL,
    body        TEXT NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_messages_chat_created (chat_id, created_at DESC),
    KEY idx_messages_sender (sender_id),
    CONSTRAINT fk_messages_chat
        FOREIGN KEY (chat_id) REFERENCES chats (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_messages_sender
        FOREIGN KEY (sender_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- Friends, likes, preferences, notifications
-- -----------------------------------------------------------------------------

CREATE TABLE friends (
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id     BIGINT UNSIGNED NOT NULL,
    friend_id   BIGINT UNSIGNED NOT NULL,
    status      ENUM('pending', 'accepted', 'blocked') NOT NULL DEFAULT 'pending',
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_friends_pair (user_id, friend_id),
    CONSTRAINT fk_friends_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_friends_friend
        FOREIGN KEY (friend_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_friends_different_users CHECK (user_id <> friend_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE liked_routes (
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id     BIGINT UNSIGNED NOT NULL,
    route_id    BIGINT UNSIGNED NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_liked_routes_user_route (user_id, route_id),
    KEY idx_liked_routes_route (route_id),
    CONSTRAINT fk_liked_routes_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_liked_routes_route
        FOREIGN KEY (route_id) REFERENCES routes (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE user_preferences (
    id                      BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id                 BIGINT UNSIGNED NOT NULL,
    preferred_budget_id     INT UNSIGNED NULL,
    preferred_rest_type_id  INT UNSIGNED NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_user_preferences_user (user_id),
    CONSTRAINT fk_user_preferences_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_user_preferences_budget
        FOREIGN KEY (preferred_budget_id) REFERENCES budget_types (id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_user_preferences_rest
        FOREIGN KEY (preferred_rest_type_id) REFERENCES rest_types (id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE notifications (
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id     BIGINT UNSIGNED NOT NULL,
    title       VARCHAR(255) NULL,
    content     TEXT NULL,
    is_read     TINYINT(1) NOT NULL DEFAULT 0,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_notifications_user_read_created (user_id, is_read, created_at DESC),
    CONSTRAINT fk_notifications_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================================
-- Seed data
-- =============================================================================

INSERT INTO company_types (name) VALUES
    ('С семьей/ детьми'),
    ('С друзьями'),
    ('Со второй половинкой'),
    ('С незнакомцем'),
    ('Один')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO budget_types (name, min_price, max_price) VALUES
    ('до 1000 руб.', 0, 1000),
    ('1000-4000 руб.', 1000, 4000),
    ('от 5000 руб.', 5000, NULL)
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO rest_types (name) VALUES
    ('Активный'),
    ('Спокойный')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO walk_statuses (name) VALUES
    ('Запланирована'),
    ('В процессе'),
    ('Завершена'),
    ('Отменена')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO application_statuses (name) VALUES
    ('Одобрена'),
    ('Отклонена'),
    ('На рассмотрении')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO categories (name, description) VALUES
    ('Движение к природе', 'Парки, набережные, виды на Волгу и Оку'),
    ('Культурный код', 'Музеи, театры, выставочные площадки'),
    ('Нижегородская классика', 'Кремль, исторический центр, главные улицы'),
    ('Стрит-арт и дворики', 'Неочевидные маршруты и городская среда'),
    ('Духовное наследие', 'Храмы и места памяти'),
    ('Гастрономический Нижний', 'Кафе, рынки, локальные вкусы'),
    ('Ритмы Нижнего: события города', 'Площадки для прогулок с городскими событиями'),
    ('Индустриальный Нижний', 'Постиндустриальные локации и архитектура')
ON DUPLICATE KEY UPDATE description = VALUES(description);

INSERT INTO spots (name, description, latitude, longitude) VALUES
    ('Нижегородский кремль', 'Главная крепость города на высоком берегу Волги, музеи и панорамы.', 56.3281700, 43.9998300),
    ('Чкаловская лестница', 'Монументальная лестница к Волге, символ Нижнего и вид на реку.', 56.3261000, 44.0052400),
    ('Улица Большая Покровская', 'Пешеходная улица с кафе, театрами и городской атмосферой.', 56.3209000, 44.0019000),
    ('Усадьба Рукавишниковых', 'Дворянская усадьба XIX века, музей и архитектурный ансамбль.', 56.3234000, 44.0061000),
    ('Строгановская (Рождественская) церковь', 'Строгановское барокко на Рождественской улице.', 56.3280000, 44.0085000),
    ('Канатная дорога через Волгу', 'Канатная дорога с видами на Волгу и город.', 56.3302000, 43.9981000),
    ('Нижегородская ярмарка', 'Исторический комплекс ярмарки и выставочные пространства.', 56.3401000, 43.9542000),
    ('Стрелка (место слияния Оки и Волги)', 'Смотровая площадка у слияния Оки и Волги.', 56.3362000, 43.9815000),
    ('Собор Александра Невского', 'Купольный собор на Стрелке, один из символов города.', 56.3146000, 44.0528000),
    ('Пакгаузы (концертные залы)', 'Культурный кластер на набережной, концерты и фестивали.', 56.3365000, 43.9770000),
    ('Здание Госбанка', 'Архитектурный памятник конструктивизма на площади Минина.', 56.3265000, 44.0055000),
    ('Верхне-Волжская набережная', 'Набережная с видами на Волгу, прогулочная зона.', 56.3340000, 43.9890000),
    ('Площадь Минина и Пожарского', 'Главная площадь города у Кремля.', 56.3285000, 44.0020000),
    ('Пешеходный мост через Почаинский овраг', 'Пешеходный мост и вид на исторический овраг.', 56.3250000, 44.0040000),
    ('Церковь Ильи Пророка', 'Памятник древнерусского зодчества на Ильинской улице.', 56.3278000, 44.0095000);
