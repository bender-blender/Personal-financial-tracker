-- ============================================================
-- Personal Financial Tracker — Telegram Bot
-- SQLite схема базы данных
-- Суммы: INTEGER в копейках (1500 = 15.00)
-- Даты:  INTEGER Unix timestamp
-- ============================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- ============================================================
-- users — пользователи бота
-- Авторизация через Telegram, пароль не нужен
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id      INTEGER NOT NULL UNIQUE,   -- ID пользователя в Telegram
    username         TEXT,                       -- @username (может быть NULL)
    first_name       TEXT    NOT NULL,           -- имя из Telegram
    default_currency TEXT    NOT NULL DEFAULT 'UAH',
    notifications    INTEGER NOT NULL DEFAULT 1, -- 0/1
    created_at       INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_users_telegram_id
    ON users(telegram_id);

-- ============================================================
-- households — семейные группы
-- ============================================================
CREATE TABLE IF NOT EXISTS households (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    invite_code TEXT    NOT NULL UNIQUE,  -- код для вступления (напр. "ABC1-XY23")
    created_by  INTEGER NOT NULL REFERENCES users(id),
    created_at  INTEGER NOT NULL
);

-- ============================================================
-- household_members — кто в какой группе
-- ============================================================
CREATE TABLE IF NOT EXISTS household_members (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    user_id      INTEGER NOT NULL REFERENCES users(id)      ON DELETE CASCADE,
    role         TEXT    NOT NULL DEFAULT 'member'
                 CHECK (role IN ('owner', 'member')),
    joined_at    INTEGER NOT NULL,
    UNIQUE (household_id, user_id)  -- один пользователь — одна запись в группе
);

CREATE INDEX IF NOT EXISTS idx_members_user
    ON household_members(user_id);

CREATE INDEX IF NOT EXISTS idx_members_household
    ON household_members(household_id);

-- ============================================================
-- currencies — справочник валют
-- ============================================================
CREATE TABLE IF NOT EXISTS currencies (
    code           TEXT PRIMARY KEY,  -- 'UAH', 'USD', 'EUR'
    symbol         TEXT NOT NULL,     -- '₴', '$', '€'
    decimal_places INTEGER NOT NULL DEFAULT 2
);

INSERT OR IGNORE INTO currencies (code, symbol, decimal_places) VALUES
    ('UAH', '₴', 2),
    ('USD', '$', 2),
    ('EUR', '€', 2),
    ('RUB', '₽', 2),
    ('GBP', '£', 2);

-- ============================================================
-- categories — категории доходов и расходов
-- ============================================================
CREATE TABLE IF NOT EXISTS categories (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL UNIQUE,
    type       TEXT NOT NULL CHECK (type IN ('income', 'expense')),
    color      TEXT NOT NULL DEFAULT '#607D8B',
    icon       TEXT NOT NULL DEFAULT 'tag',
    is_default INTEGER NOT NULL DEFAULT 0  -- 1 = встроенная, нельзя удалить
);

INSERT OR IGNORE INTO categories (name, type, color, icon, is_default) VALUES
    ('Еда',          'expense', '#EF5350', 'food',          1),
    ('Транспорт',    'expense', '#42A5F5', 'transport',     1),
    ('Жильё',        'expense', '#AB47BC', 'home',          1),
    ('Здоровье',     'expense', '#26C6DA', 'health',        1),
    ('Развлечения',  'expense', '#FFA726', 'entertainment', 1),
    ('Одежда',       'expense', '#EC407A', 'clothes',       1),
    ('Образование',  'expense', '#66BB6A', 'education',     1),
    ('Прочее',       'expense', '#78909C', 'other',         1),
    ('Зарплата',     'income',  '#66BB6A', 'salary',        1),
    ('Фриланс',      'income',  '#29B6F6', 'freelance',     1),
    ('Подарок',      'income',  '#FFCA28', 'gift',          1),
    ('Прочий доход', 'income',  '#78909C', 'other_income',  1);

-- ============================================================
-- transactions — все финансовые записи
-- household_id = NULL → личная запись
-- household_id = N    → запись семейного бюджета группы N
-- ============================================================
CREATE TABLE IF NOT EXISTS transactions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    household_id INTEGER REFERENCES households(id),  -- NULL если личная
    amount       INTEGER NOT NULL CHECK (amount > 0), -- в копейках
    currency     TEXT    NOT NULL DEFAULT 'UAH' REFERENCES currencies(code),
    category_id  INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    type         TEXT    NOT NULL CHECK (type IN ('income', 'expense')),
    date         INTEGER NOT NULL,    -- Unix timestamp
    note         TEXT,
    created_at   INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_transactions_user
    ON transactions(user_id);

CREATE INDEX IF NOT EXISTS idx_transactions_date
    ON transactions(date);

CREATE INDEX IF NOT EXISTS idx_transactions_user_date
    ON transactions(user_id, date);

CREATE INDEX IF NOT EXISTS idx_transactions_household
    ON transactions(household_id);

-- ============================================================
-- budgets — лимиты расходов по категориям на месяц
-- ============================================================
CREATE TABLE IF NOT EXISTS budgets (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    household_id INTEGER REFERENCES households(id),
    category_id  INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    year_month   TEXT    NOT NULL,           -- формат 'YYYY-MM'
    limit_amount INTEGER NOT NULL CHECK (limit_amount > 0),
    currency     TEXT    NOT NULL DEFAULT 'UAH' REFERENCES currencies(code),
    UNIQUE (user_id, category_id, year_month)
);

-- ============================================================
-- recurring — повторяющиеся операции
-- ============================================================
CREATE TABLE IF NOT EXISTS recurring (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    household_id INTEGER REFERENCES households(id),
    amount       INTEGER NOT NULL CHECK (amount > 0),
    currency     TEXT    NOT NULL DEFAULT 'UAH' REFERENCES currencies(code),
    category_id  INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    type         TEXT    NOT NULL CHECK (type IN ('income', 'expense')),
    interval     TEXT    NOT NULL CHECK (interval IN ('daily', 'weekly', 'monthly', 'yearly')),
    next_date    INTEGER NOT NULL,
    note         TEXT,
    is_active    INTEGER NOT NULL DEFAULT 1
);
