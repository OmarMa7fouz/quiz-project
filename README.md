# 🎓 نظام الاختبارات الذكي | My Quiz Project

مشروع Django متكامل لنظام اختبارات ذكي مع واجهة مستخدم حديثة وجميلة.

A comprehensive Django-based quiz application with a modern, beautiful user interface.

## ✨ المميزات | Features

- 🎨 **واجهة حديثة وجميلة** - Built with Bootstrap 5 RTL
- 🌙 **وضع ليلي** - Dark mode support
- 📊 **رسوم بيانية تفاعلية** - Interactive charts with Chart.js
- 💻 **تمييز الأكواد** - Syntax highlighting with Prism.js
- 📱 **تصميم متجاوب** - Fully responsive design
- 🔐 **نظام مستخدمين متكامل** - Complete authentication system
- 📈 **تتبع التقدم** - Progress tracking and analytics
- ⚡ **نتائج فورية** - Instant results with detailed analysis

## 🏗️ هيكل المشروع | Project Structure

```
quiz-project/
├── apps/                   # Custom Django applications
│   ├── quiz_app/          # Quiz functionality app
│   │   ├── templates/     # HTML templates
│   │   ├── static/        # CSS, JS, images
│   │   ├── models.py      # Database models
│   │   ├── views.py       # Views
│   │   ├── urls.py        # URL patterns
│   │   └── admin.py       # Admin configuration
│   └── users_app/         # User management app
├── assets/                # Static assets (CSS, JS, images)
├── logs/                  # Application logs
├── media/                 # User-uploaded files
├── my_quiz_project/       # Main project configuration
├── scripts/               # Utility scripts
│   └── seed_database.py  # Database seeding script
├── shared/                # Shared utilities and helpers
├── staticfiles/           # Collected static files (for production)
├── templates/             # Project-level templates
├── manage.py             # Django management script
├── README.md             # This file
└── PROJECT_SETUP.md      # Detailed setup guide (Arabic)
```

## 🚀 البدء السريع | Quick Start

### الخادم يعمل الآن! | Server is Running!

**🌐 الموقع الرئيسي | Main Site:**
```
http://127.0.0.1:8000/
```

**🔐 لوحة الإدارة | Admin Panel:**
```
http://127.0.0.1:8000/admin/
```

**بيانات الدخول | Login Credentials:**
- **Username:** admin
- **Password:** admin123

### إعداد جديد | Fresh Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd quiz-project
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Seed database with sample data**
   ```bash
   python scripts/seed_database.py
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - Login: admin / admin123

## 📚 المكونات الرئيسية | Main Components

### quiz_app - تطبيق الاختبارات
- ✅ إنشاء وإدارة الاختبارات
- ✅ أسئلة متعددة الأنواع (اختيار واحد، متعدد، صح/خطأ)
- ✅ دعم الأكواد البرمجية
- ✅ نظام نقاط مرن
- ✅ تتبع النتائج والتحليلات
- ✅ واجهة تفاعلية مع مؤقت

### users_app - تطبيق المستخدمين
- ✅ نظام مصادقة المستخدمين
- ✅ إدارة الملفات الشخصية
- ✅ تتبع تقدم المستخدم

### البيانات النموذجية | Sample Data
- 4 فئات (البرمجة، قواعد البيانات، تطوير الويب، الذكاء الاصطناعي)
- 3 اختبارات جاهزة
- 9 أسئلة مع إجابات
- مستخدم إداري جاهز

## Development

### Running Tests
```bash
python manage.py test
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Configuration

The project is configured to use:
- SQLite database (default)
- Static files in `assets/` directory
- Media files in `media/` directory
- Templates in `templates/` directory

Edit `my_quiz_project/settings.py` to customize these settings.

## 🎨 التقنيات المستخدمة | Technologies Used

### Backend
- Django 5.2.5
- Python 3.12
- SQLite (development) / PostgreSQL (production ready)

### Frontend
- Bootstrap 5 RTL
- Chart.js (رسوم بيانية)
- Prism.js (تمييز الأكواد)
- Animate.css (المؤثرات)
- Bootstrap Icons
- Vanilla JavaScript (ES6+)

## 📖 التوثيق | Documentation

للحصول على دليل إعداد مفصل بالعربية، راجع:
For detailed setup guide in Arabic, see:
**[PROJECT_SETUP.md](PROJECT_SETUP.md)**

## 🛠️ الأوامر المفيدة | Useful Commands

```bash
# تشغيل الخادم | Run server
python manage.py runserver

# إنشاء migrations | Create migrations
python manage.py makemigrations

# تطبيق migrations | Apply migrations
python manage.py migrate

# تعبئة قاعدة البيانات | Seed database
python scripts/seed_database.py

# جمع الملفات الثابتة | Collect static files
python manage.py collectstatic

# اختبار التطبيق | Run tests
python manage.py test
```

## 🤝 المساهمة | Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 الترخيص | License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 شكر وتقدير | Acknowledgments

Built with ❤️ using Django and Bootstrap

---

**استمتع بالتطوير! | Happy Coding!** 🚀

