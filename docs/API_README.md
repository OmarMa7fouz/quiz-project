# Quiz System API

A comprehensive REST API for the Smart Quiz System built with Django REST Framework.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed Database
```bash
python scripts/seed_database.py
```

### 4. Start Server
```bash
python manage.py runserver
```

### 5. Test API
```bash
python test_api.py
```

## 📋 Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/` | Health check |
| GET | `/api/subjects/` | Get all subjects |
| GET | `/api/subjects/{code}/` | Get subject details |
| GET | `/api/questions/` | Get questions (with filters) |
| POST | `/api/quiz/generate/` | Generate random quiz |
| POST | `/api/quiz/submit/` | Submit quiz answers |
| GET | `/api/stats/` | Get system statistics |

## 🔧 Features

- ✅ **RESTful API** - Clean, consistent endpoints
- ✅ **JSON Responses** - Easy to parse and use
- ✅ **CORS Enabled** - Cross-origin requests supported
- ✅ **No Authentication** - Simple to use (development mode)
- ✅ **Random Questions** - Different questions each time
- ✅ **Comprehensive Stats** - Detailed system information
- ✅ **Error Handling** - Proper HTTP status codes
- ✅ **Documentation** - Complete API docs included

## 📖 Usage Examples

### Get All Subjects
```bash
curl http://127.0.0.1:8000/api/subjects/
```

### Generate Quiz
```bash
curl -X POST http://127.0.0.1:8000/api/quiz/generate/ \
  -H "Content-Type: application/json" \
  -d '{"subject_code": "CSW351-AI", "level": "easy", "num_questions": 10}'
```

### Submit Quiz
```bash
curl -X POST http://127.0.0.1:8000/api/quiz/submit/ \
  -H "Content-Type: application/json" \
  -d '{"answers": [{"question_id": 1, "selected_answer": "A"}]}'
```

## 🌐 Browseable API

Visit `http://127.0.0.1:8000/api/` for the interactive API browser.

## 📚 Documentation

- **Complete API Docs**: `API_DOCUMENTATION.md`
- **Test Script**: `test_api.py`
- **Django REST Framework**: https://www.django-rest-framework.org/

## 🎯 Use Cases

- **Mobile Apps** - Build iOS/Android quiz apps
- **Web Applications** - Integrate with React/Vue/Angular
- **Third-party Integration** - Connect with other systems
- **Data Analysis** - Extract quiz statistics
- **Automated Testing** - Programmatic quiz testing

## 🔒 Security Notes

- Currently configured for development (no authentication)
- CORS is enabled for all origins
- For production, add proper authentication and CORS restrictions

## 🐛 Troubleshooting

### Server Not Running
```bash
python manage.py runserver
```

### Database Issues
```bash
python manage.py makemigrations
python manage.py migrate
python scripts/seed_database.py
```

### API Not Working
```bash
python test_api.py
```

## 📞 Support

For issues or questions, check the API documentation or run the test script to verify functionality.
