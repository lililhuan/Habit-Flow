# 🎯 HabitFlow - Habit Tracking Application

**Track your habits. Stay consistent. Build a better you.**

HabitFlow is a mobile-first habit tracking application built with Flet (Python).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flet](https://img.shields.io/badge/Flet-0.23+-green.svg)


---

## 📋 Table of Contents

- [Features](#-features)
- [Security Features](#-security-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Team Members](#-team-members)

---

## 🌟 Features

### Core Features
| Feature | Description |
|---------|-------------|
| 👤 **User Authentication** | Secure sign-up/sign-in with password validation |
| 📝 **Habit Management** | Create, edit, delete, and track daily/weekly habits |
| ✅ **Daily Tracking** | Mark habits complete with date navigation |
| 🔥 **Streak Building** | Track current and longest streaks |
| 📊 **Progress Analytics** | Visualize progress with charts and statistics |
| 💾 **Data Export/Import** | Backup and restore your data (JSON format) |
| 🎨 **Theme Support** | 8 color themes + dark/light mode |
| 🤖 **AI Categorization** | Automatic habit categorization using AI |
| 👨‍💼 **Admin Dashboard** | User management for administrators |

### Analytics & Visualization
- 📊 Completion rate tracking
- 🔥 Streak calculations (current & longest)
- 📈 Weekly pattern analysis
- 🏆 Habit performance ranking
- 📅 Monthly/yearly statistics
- 📊 Category distribution charts

---

## 🔐 Security Features

### Authentication & Authorization
- ✅ **Password Hashing** - bcrypt encryption for all passwords
- ✅ **Password Requirements** - Minimum 8 chars, uppercase, number
- ✅ **Account Lockout** - 5 failed attempts = 15 min lockout
- ✅ **Session Management** - Auto-logout after inactivity
- ✅ **Admin Access Control** - Role-based admin privileges

### Logging & Monitoring
- 📝 **Security Logs** - Track login attempts, password changes
- 📝 **Activity Logs** - Monitor user activity
- 📝 **Failed Login Tracking** - Detect brute force attempts

### Data Protection
- 🔒 Local SQLite database (no cloud transmission)
- 🔒 Thread-safe database connections
- 🔒 Input validation and sanitization

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/lililhuan/Habit-Flow.git
   cd Habit-Flow/app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   flet run
   ```
   
   Or using Flet CLI:
   ```bash
   flet run app/main.py
   ```

---

## 📱 Usage

### First Time Setup
1. Launch the app
2. Click "Create Account"
3. Enter email and password (must meet requirements)
4. Add your first habit with the + button
5. Start tracking daily!

### Navigation
| Icon | Tab | Description |
|------|-----|-------------|
| 🏠 | **Habits** | View and manage all habits |
| ✓ | **Today** | Track today's habits |
| ➕ | **Add** | Create a new habit |
| 📊 | **Stats** | View analytics and charts |
| ⚙️ | **Settings** | Account, themes, data management |

### Admin Access
- Admin emails are configured in the app
- Admins can: view all users, disable accounts, view security logs

---

## 📁 Project Structure

```
Habit-Flow/
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── pytest.ini             # Test configuration
│
├── app/
│   ├── __init__.py
│   ├── main.py            # Application entry point
│   │
│   ├── components/        # Reusable UI components
│   │   ├── add_habit_dialog.py
│   │   ├── bottom_nav.py
│   │   └── habit_card.py
│   │
│   ├── config/            # Configuration files
│   │   └── theme.py       # Color themes
│   │
│   ├── models/            # Data models
│   │   ├── habit.py
│   │   ├── completion.py
│   │   └── user.py
│   │
│   ├── services/          # Business logic
│   │   ├── auth_service.py
│   │   ├── habit_service.py
│   │   ├── analytics_service.py
│   │   ├── export_service.py
│   │   └── security_logger.py
│   │
│   ├── state/             # Application state
│   │   └── app_state.py
│   │
│   ├── storage/           # Database layer
│   │   └── database.py
│   │
│   ├── views/             # UI screens
│   │   ├── welcome_view.py
│   │   ├── auth_view.py
│   │   ├── habits_view.py
│   │   ├── today_view.py
│   │   ├── stats_view.py
│   │   ├── settings_view.py
│   │   └── admin_view.py
│   │
│   └── tests/             # Unit tests
│       ├── __init__.py
│       ├── test_auth_service.py
│       ├── test_database.py
│       ├── test_habit_service.py
│       └── test_analytics_service.py
│
├── storage/               # Runtime data
│   └── data/
│
└── assets/                # Static assets
```

---

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| **Framework** | Flet (Flutter for Python) |
| **Language** | Python 3.8+ |
| **Database** | SQLite |
| **Authentication** | bcrypt |
| **UI/UX** | Material Design 3 |
| **State Management** | Custom AppState |

---

## 👥 Team Members

| Name | Role | GitHub |
|------|------|--------|
| **Roinel (lililhuan)** | Lead Developer | [@lililhuan](https://github.com/lililhuan) |
| **Justine Aaron** | Developer | [@JustineAaron](https://github.com/JustineAaron) |
| **Titojek** | Developer | [@titojek](https://github.com/titojek) |

---

**Made with ❤️ for building better habits**
