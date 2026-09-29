# Форма Studio — Custom Furniture Website

Преміальний сайт меблів на замовлення за макетом [Figma Make](https://www.figma.com/make/yZ79AFmfK8Z3kPMcwhqZJn/Custom-Furniture-Designer-Website).

## Стек

| Шар | Технології |
|---|---|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS 4 |
| Backend | Django 5, Django REST Framework |
| Admin | Jazzmin |
| DB | PostgreSQL 16 |
| Infra | Docker Compose, Nginx |

## Швидкий старт (Docker)

```bash
cp .env.example .env
docker compose up --build -d
```

Після запуску:

- Сайт: http://localhost
- API: http://localhost/api/home/
- Адмінка Jazzmin: http://localhost/admin/  
  Логін за замовчуванням: `admin` / `admin123`

## Локальний запуск (рекомендовано)

```bash
./run.sh
```

Скрипт:
- перевіряє зміни моделей і створює нові міграції за потреби;
- застосовує неприйняті міграції;
- піднімає Django (`:8000`) і Next.js (`:3000`).

Корисні прапорці:

```bash
./run.sh --seed          # також залити демо-дані
./run.sh --backend-only
./run.sh --frontend-only
```

Сайт: http://localhost:3000  
Адмінка: http://localhost:8000/admin/ (`admin` / `admin123` після seed)

### Backend (вручну)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver 8000
```

### Frontend (вручну)

```bash
cd frontend
npm install
echo 'NEXT_PUBLIC_API_URL=http://localhost:8000/api' > .env.local
npm run dev
```

## SEO

- `lang="uk"`, семантична розмітка секцій
- metadata / Open Graph у `layout.tsx`
- `sitemap.xml`, `robots.txt`
- JSON-LD LocalBusiness / FurnitureStore
- SSR контент з API (fallback на мокап-дані)

## Адмінка (повний CMS)

Через Jazzmin (`/admin/`) керується **весь контент** сайту:

- **Налаштування сайту** — бренд, header/hero тексти і CTA, SEO, контакти, форма, footer, drawing/before-after копірайт
- **Секції сторінки** — заголовки, підзаголовки, видимість, CTA кожної секції
- **Навігація** — пункти шапки та футера
- **Статистика героя** — цифри та підписи
- **Типи кімнат** — чіпи контактної форми
- **Проєкти** (+ етапи «щоденника»), матеріали, процес, майстерня
- **Заявки** з форми зворотного зв’язку

Після змін у адмінці оновіть сторінку — frontend бере дані з `GET /api/home/`.

## MCP

Локальний сервер [Model Context Protocol](https://modelcontextprotocol.io) віддає Cursor публічний контент сайту: налаштування, секції, проєкти, матеріали, процес і майстерню. Джерело — живий API (`GET /api/home/` та сусідні ендпоінти). Заявки клієнтів і секрети адмінки не віддаються.

Один раз:

```bash
python3 -m venv mcp/.venv
mcp/.venv/bin/pip install -r mcp/requirements.txt
```

Конфіг уже в `.cursor/mcp.json` (`luxmeb` → `http://127.0.0.1:8000/api`). Увімкніть сервер у Cursor: **Settings → MCP**. Бекенд має бути запущений (`./run.sh`). Для Docker змініть `LUXMEB_API_URL` на `http://127.0.0.1/api`.

## Структура

```
LuxMeb/
├── backend/          # Django + DRF + Jazzmin
├── frontend/         # Next.js
├── mcp/              # MCP-сервер публічного контенту
├── nginx/            # reverse proxy
├── docker-compose.yml
└── README.md
```
