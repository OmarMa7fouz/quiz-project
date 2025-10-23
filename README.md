# Smart Quiz System

A comprehensive quiz application built with Django and Django REST Framework, featuring a chatbot interface and RESTful API.

## 🚀 Features

- **Interactive Quiz System** - Multiple subjects and difficulty levels
- **Chatbot Interface** - Guided quiz selection
- **RESTful API** - Complete API for integration
- **Random Questions** - Different questions each time
- **Instant Results** - Immediate feedback and scoring
- **Professional UI** - Modern, responsive design
- **LTR Layout** - Left-to-right layout (English)

## 📁 Project Structure

```
quiz-project/
├── apps/
│   └── quiz_app/
│       ├── models.py          # Database models
│       ├── views.py           # Web views
│       ├── api_views.py       # API endpoints
│       ├── serializers.py     # API serializers
│       ├── urls.py            # Web URLs
│       ├── api_urls.py        # API URLs
│       ├── admin.py           # Admin interface
│       ├── chatbot_views.py   # Chatbot views
│       ├── templates/         # HTML templates
│       │   ├── base.html
│       │   ├── home.html
│       │   ├── quiz.html
│       │   ├── quiz_list.html
│       │   ├── results.html
│       │   └── chatbot/
│       │       ├── home.html
│       │       ├── select_subject.html
│       │       ├── select_difficulty.html
│       │       └── error.html
│       └── static/            # Static files
│           ├── css/
│           ├── js/
│           └── images/
├── my_quiz_project/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── scripts/                   # Utility scripts
│   ├── seed_database.py
│   ├── manage_questions.py
│   ├── import_questions.py
│   ├── view_database.py
│   ├── quiz_database.py
│   ├── sql_queries.sql
│   └── test_api.py
├── docs/                      # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── API_README.md
│   └── HOW_TO_ADD_QUESTIONS.md
├── static/                    # Static files
├── media/                     # Media files
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd quiz-project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed the database
```bash
python scripts/seed_database.py
```

### 5. Start the server
```bash
python manage.py runserver
```

## 🌐 Usage

### Web Interface
- **Home**: http://127.0.0.1:8000/
- **Quiz List**: http://127.0.0.1:8000/quizzes/
- **Chatbot**: http://127.0.0.1:8000/chatbot/

### API Endpoints
- **API Root**: http://127.0.0.1:8000/api/
- **Subjects**: http://127.0.0.1:8000/api/subjects/
- **Questions**: http://127.0.0.1:8000/api/questions/
- **Health Check**: http://127.0.0.1:8000/api/health/

## 📚 Documentation

- **API Documentation**: `docs/API_DOCUMENTATION.md`
- **API README**: `docs/API_README.md`
- **Question Management**: `docs/HOW_TO_ADD_QUESTIONS.md`

## 🧪 Testing

### Test the API
```bash
python scripts/test_api.py
```

### Test the Web Interface
Visit the URLs above in your browser.

## 📊 Database

The system uses SQLite with the following models:
- **Subject**: Quiz subjects (CSW351-AI, INT353-MULTIMEDIA, etc.)
- **Question**: Quiz questions with multiple choice answers

## 🔧 Configuration

### Settings
- **Database**: SQLite (development)
- **Language**: English only
- **Layout**: LTR (Left-to-Right)
- **API**: RESTful with JSON responses

### Environment Variables
- `DEBUG`: Set to `True` for development
- `SECRET_KEY`: Django secret key

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure proper database
3. Set up static file serving
4. Configure CORS settings
5. Set up authentication if needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the documentation in `docs/`
2. Run the test script: `python scripts/test_api.py`
3. Check the API health: http://127.0.0.1:8000/api/health/

## 🎯 Features Overview

- ✅ **4 Subjects** - AI, Multimedia, Web Technology, Parallel Processing
- ✅ **3 Difficulty Levels** - Easy, Medium, Hard
- ✅ **360 Questions** - 30 per level per subject
- ✅ **Random Selection** - 10 questions per quiz
- ✅ **Instant Results** - Immediate feedback
- ✅ **API Integration** - RESTful API
- ✅ **Chatbot Interface** - Guided selection
- ✅ **Professional Design** - Modern UI
- ✅ **LTR Layout** - English interface
- ✅ **No Authentication** - Simple to use