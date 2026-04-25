

# 📚 StudyKu

**StudyKu** is a Django-based platform that helps students and teachers manage study resources in one place.
It includes features like **Google OAuth login**, **PDF uploads**, **search with Redis caching**, **bookmarking**, and **mobile-responsive UI**.

---

## 🚀 KEY Features

* 🔐 **Google Authentication (OAuth 2.0)**
* 📂 **Upload & manage study PDFs**
* 🔎 **Fast search powered by Redis cache**
* 📑 **Bookmark resources with a one-click system**
* ⚡ **High performance with Django + Redis**
* 📝 **Session-based user management**

---

## 🛠 Tech Stack

* **Backend**: Django 5.x, Django REST Framework
* **Frontend**: HTML5, CSS3, Bootstrap 5, JS
* **Database**: SQLite / PostgreSQL (configurable)
* **Cache**: Redis
* **Authentication**: Google OAuth 2.0
* **Deployment**: Ngrok (for localhost tunneling), can be hosted on Railway/Heroku/AWS

---

## 📂 Project Structure

```
StudyKu/
│── manage.py
│── StudyKu/               # Main Django settings
│── accounts/              # Authentication app (Google OAuth)
│── resources/             # PDFs, bookmarks, search
│── templates/             # HTML templates
│── static/                # CSS, JS, images
│── media/                 # Uploaded files
```

---

## ⚙️ Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-username/studyku.git
   cd studyku
   ```

2. **Create a virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows

   pip install -r requirements.txt
   ```

3. **Run migrations**

   ```bash
   python manage.py migrate
   ```

4. **Set up Google OAuth**

   * Go to [Google Cloud Console](https://console.cloud.google.com/)
   * Create OAuth credentials
   * Add `http://127.0.0.1:8000/` and your ngrok link as **Authorized Redirect URIs**
   * Add client ID & secret in `settings.py`

5. **Run Redis locally** (make sure Redis server is running)

6. **Start server**

   ```bash
   python manage.py runserver
   ```

---

## 🖼 Screenshots

* 🔐 **Google Login**
* 📂 **Upload & Search PDFs**
* 📑 **Bookmark Popup**
* 📱 **Mobile Responsive UI**

*(Add screenshots here — `/static/screenshots` folder recommended)*

---

## 🚧 Roadmap

* [ ] Dark mode support
* [ ] Real-time collaboration (chat & notes)
* [ ] AI-powered document summarizer
* [ ] Docker setup for production

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature-name`)
5. Create a Pull Request

---



## 🙌 Acknowledgements

* [Django](https://www.djangoproject.com/)
* [Redis](https://redis.io/)
* [Google OAuth](https://developers.google.com/identity)
* Bootstrap 5

---


