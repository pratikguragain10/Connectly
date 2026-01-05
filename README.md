# 🌐 Connectly — Social Networking Platform

Connectly is a modern social networking web application built using **Django**.  
It allows users to connect with friends, share posts, like and comment on content, and manage their profiles — inspired by platforms like Facebook.

---

## 🚀 Features

### 🔐 Authentication
- User signup & login (Django Allauth)
- Google OAuth login
- Secure authentication & session handling

### 👤 User Profiles
- Profile & cover photo upload (Cloudinary)
- Bio, education, work & location
- Edit profile functionality

### 📰 Posts
- Create text, image & video posts
- Edit & delete posts
- Like & comment on posts
- Nested replies (threaded comments)

### 🤝 Friends System
- Send, cancel, accept & reject friend requests
- Friends list & count
- View friend profiles

### 🔍 Search
- Search users by username
- Send friend requests from search results

### 🎨 UI / UX
- Clean Facebook-inspired UI
- Responsive layout
- Sticky navigation bar
- Profile previews (friends & photos)

---

## 🛠 Tech Stack

### Backend
- Django
- Django Allauth
- Django REST Framework
- Django Channels (optional)

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript

### Storage
- Cloudinary (images & videos)

### Database
- SQLite (development)
- PostgreSQL (production)

### Deployment
- Render

---

## 📁 Project Structure

```text
connectly/
│
├── accounts/
├── posts/
├── friends/
├── notifications/
├── templates/
├── static/
├── connectly/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── manage.py
├── requirements.txt
├── build.sh
├── README.md
└── .gitignore
```

---

## ⚙️ Setup Instructions (Local)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/connectly.git
cd connectly
```

### 2️⃣ Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your_secret_key

CLOUDINARY_CLOUD_NAME=xxx
CLOUDINARY_API_KEY=xxx
CLOUDINARY_API_SECRET=xxx
```

### 5️⃣ Run migrations
```bash
python manage.py migrate
```

### 6️⃣ Create superuser
```bash
python manage.py createsuperuser
```

### 7️⃣ Run development server
```bash
python manage.py runserver
```

---

## 🌍 Deployment (Render)

- Uses **Gunicorn**
- Static files served via **WhiteNoise**
- **PostgreSQL** database
- **Cloudinary** for media storage

---

## 📌 Future Enhancements
- Notifications system
- Real-time chat
- Infinite scrolling feed
- Stories feature
- Mobile-first improvements

---
