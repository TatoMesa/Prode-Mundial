# Prode Mundial

Plataforma web de pronósticos deportivos desarrollada en Python/Django, diseñada para que grupos de personas compitan prediciendo resultados de partidos de fútbol en tiempo real.

## 🚀 Demo en producción

[https://prodemundial.nexusstudiocode.online](https://prodemundial.nexusstudiocode.online)

## 🛠️ Stack tecnológico

- **Backend:** Python 3.12 + Django 6.0
- **Frontend:** Bootstrap 5 + React 18 (componente de marcador en vivo)
- **API REST:** Django REST Framework
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Deploy:** DigitalOcean VPS + Nginx + Gunicorn
- **Email:** Resend API

## ✨ Funcionalidades principales

- Registro, login y recuperación de contraseña
- Ligas privadas con código de acceso
- Pronósticos bloqueados automáticamente 10 minutos antes del partido
- Sistema de puntuación automático (5 pts exacto / 2 pts ganador)
- Tabla de posiciones por grupo con estadísticas completas
- Bracket eliminatorio visual
- Marcador en vivo con actualización automática via React + API REST
- Panel de administración completo sin intervención técnica
- Soporte para penales en fase eliminatoria

## 📦 Instalación local

### Requisitos previos
- Python 3.11+
- Git

### Pasos

```bash
# Clonar el repositorio
git clone https://github.com/TatoMesa/Prode-Mundial.git
cd Prode-Mundial

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu SECRET_KEY

# Crear base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar fixture del torneo
python manage.py load_fixture

# Levantar servidor
python manage.py runserver
```

Accedé en `http://127.0.0.1:8000`

## ⚙️ Variables de entorno

| Variable | Descripción | Requerida en prod |
|---|---|---|
| `SECRET_KEY` | Clave secreta de Django | ✅ |
| `DEBUG` | True/False | ✅ |
| `ALLOWED_HOSTS` | Dominios permitidos | ✅ |
| `DB_NAME` | Nombre de la base PostgreSQL | ✅ |
| `DB_USER` | Usuario PostgreSQL | ✅ |
| `DB_PASSWORD` | Contraseña PostgreSQL | ✅ |
| `DB_HOST` | Host PostgreSQL | ✅ |
| `RESEND_API_KEY` | API key de Resend para emails | ✅ |
| `DEFAULT_FROM_EMAIL` | Email remitente | ✅ |

## 🧪 Tests

```bash
python manage.py test apps.predictions.tests
```

## 🏗️ Arquitectura

prode_mundial/
├── apps/
│   ├── accounts/      # Usuarios, perfiles, autenticación
│   ├── leagues/       # Ligas privadas con código de acceso
│   ├── matches/       # Equipos, partidos, API REST
│   ├── predictions/   # Pronósticos, puntuación, ranking
│   └── tournament/    # Grupos, tabla de posiciones, bracket
├── config/
│   └── settings.py    # Configuración con python-decouple
├── templates/         # Templates Bootstrap 5
└── static/            # CSS y assets estáticos

## 📡 API REST

| Endpoint | Descripción |
|---|---|
| `GET /matches/api/<pk>/` | Estado y resultado de un partido en JSON |

## 🔐 Decisiones técnicas

- **Señales Django** para recálculo automático de puntos al finalizar partidos
- **`PredictionLockMixin`** para bloqueo temporal reutilizable en vistas de pronósticos
- **`python-decouple`** para separación estricta de configuración y código
- **`bulk_update`** para recalcular múltiples pronósticos en una sola query
- **React embebido** para el marcador en vivo sin necesidad de un SPA completo
- **`F().desc(nulls_last=True)`** en rankings para manejar correctamente usuarios sin puntos

## 👤 Autor

Sebastián Mesa — Proyecto Final de Máster en Desarrollo Full Stack
