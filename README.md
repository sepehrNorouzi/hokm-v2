# 🃏 Hokm V2

> A modern Django-based card game platform with social features.

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/django-5.2.4-green.svg)](https://djangoproject.com)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://docker.com)

## ✨ Features

- 🎮 **Match System** - Create and join game matches with entry costs and rewards
- 👥 **Social Network** - Friend requests, friendships, and player profiles  
- 🏪 **In-Game Shop** - Virtual currencies, assets, and package purchases
- 🎁 **Reward System** - Daily rewards, lucky wheel, and level progression
- 🏆 **Leaderboards** - Competitive rankings with automated tournaments
- 📊 **Player Statistics** - XP, levels, cups, and detailed game analytics
- 🔐 **Dual Authentication** - Support for both registered users and guest players

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+ (for local development)

### Run with Docker
```bash
git clone https://github.com/yourusername/hokm-v2.git
cd hokm-v2
cp .env.sample .env  # Configure your environment
docker compose up -d
```

Visit `http://localhost:8000` to access the application.

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## 🏗️ Architecture

```
hokm-v2/
├── user/           # User management & authentication
├── match/          # Game matching & results
├── shop/           # Virtual economy & purchases
├── player_shop/    # Player wallets & transactions
├── social/         # Friend system & interactions
├── leaderboard/    # Rankings & competitions
├── player_statistic/ # Player progression & stats
└── common/         # Shared utilities & config
```

## 🐳 Services

- **Web** - Django application server
- **Database** - PostgreSQL for data persistence
- **Cache** - Redis for sessions & caching
- **Storage** - MinIO for file storage
- **Queue** - Celery for background tasks
- **Search** - MongoDB for analytics

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run manage.py test
coverage report
```

## 📝 API Documentation

The API follows REST principles with Django REST Framework:

- **Authentication**: JWT tokens
- **User Management**: `/api/user/`
- **Match System**: `/api/match_type/`
- **Shop & Economy**: `/api/shop/`
- **Social Features**: `/api/social/`
- **Statistics**: `/api/player_statistic/`

## 🔧 Configuration

Key environment variables:
```bash
DEBUG=False
SECRET_KEY=your-secret-key
POSTGRES_DB=hokm
REDIS_URI=redis://localhost:6379/0
EMAIL_HOST=smtp.gmail.com
GAME_SERVER_KEY=your-game-server-key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <strong>Built with ❤️ using Django</strong>
</div>
