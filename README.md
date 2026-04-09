# 🍳 AI Chef - Evde Ne Var?

> 🤖 Evindeki malzemelere göre yapay zeka destekli tarif önerisi al. Akıllı mutfak asistanın.

---

## 📌 Proje Hakkında

**"Evde malzeme var ama ne yapacağımı bilmiyorum."**

Bu çok gerçek bir problemi çözen AI destekli bir yemek öneri platformudur. Sistem yalnızca tarif listelemekle kalmaz; eksik malzemeleri tespit eder, tarifleri kullanıcı tercihlerine göre kişiselleştirir ve etkileşimli mutfak asistanı olarak çalışır.

---

## ✨ Özellikler

| Özellik | Açıklama |
|---------|----------|
| 🧊 **Dolap Yönetimi** | Evdeki malzemeleri ekle, sil, listele |
| 🤖 **AI Tarif Önerisi** | Gemini AI ile akıllı tarif önerileri |
| ❌ **Eksik Malzeme Tespiti** | Tarif için eksik malzemeleri göster |
| 🎯 **Kişiselleştirme** | Hızlı, ucuz, sağlıklı, vegan gibi filtreler |
| 💬 **Mutfak Asistanı** | Pişirme sırasında AI ile sohbet |
| ♻️ **İsraf Azaltma** | Bozulmak üzere olan malzemeleri önce kullandır |
| ⭐ **Favori Tarifler** | Beğendiğin tarifleri kaydet |
| 📊 **Kalori Tahmini** | Her tarif için kalori bilgisi |

---

## 🛠️ Teknolojiler

### Backend
| Teknoloji | Kullanım |
|-----------|----------|
| 🐍 Python 3.12 | Ana dil |
| ⚡ FastAPI | REST API framework |
| 🗃️ SQLAlchemy + SQLite | Veritabanı |
| 🤖 Gemini AI (OpenRouter) | Yapay zeka motoru |
| 🔐 JWT Authentication | Kullanıcı kimlik doğrulama |

### Frontend
| Teknoloji | Kullanım |
|-----------|----------|
| ⚛️ Next.js 15 | React framework |
| 📘 TypeScript | Tip güvenliği |
| 🎨 Tailwind CSS | Stil ve tasarım |
| 📡 Axios | API iletişimi |

---

## 🚀 Kurulum

### 📋 Gereksinimler
- Python 3.11+
- Node.js 18+
- npm

### 🔧 Backend Kurulumu

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

`.env` dosyası oluştur:

```env
OPENROUTER_API_KEY=your_api_key
DATABASE_URL=sqlite:///./aichef.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

Backend başlatma:

```bash
uvicorn app.main:app --reload --port 8000
```

### 🎨 Frontend Kurulumu

```bash
cd frontend
npm install
```

`.env.local` dosyası oluştur:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Frontend başlatma:

```bash
npm run dev
```

---

## 📖 Kullanım

1. 🌐 `http://localhost:3000` adresine git
2. 📝 Kayıt ol ve giriş yap
3. 🧊 Dolabındaki malzemeleri ekle
4. ⚙️ Tercihlerini seç (hızlı, ucuz, sağlıklı vb.)
5. 🍳 "Tarif Öner" butonuna bas
6. 📖 AI tarafından önerilen tarifleri incele
7. 💬 Mutfak Asistanı ile sohbet et

---

## 📡 API Dokümantasyonu

Backend çalışırken: `http://localhost:8000/docs`

### Ana Endpointler

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| 📝 POST | `/api/auth/register` | Kullanıcı kayıt |
| 🔑 POST | `/api/auth/login` | Kullanıcı giriş |
| 🧊 POST | `/api/ingredients/bulk-add` | Malzeme ekle |
| 📋 GET | `/api/ingredients/my-ingredients` | Malzemeleri listele |
| 🍳 POST | `/api/recipes/generate` | Tarif üret |
| 💬 POST | `/api/chat/message` | AI ile sohbet |

---

## 🖥️ Ekran Görüntüleri

### 🏠 Ana Sayfa
- Modern landing page tasarımı
- Kayıt ve giriş modalları

### 🧊 Dolabım
- Malzeme ekleme arayüzü
- Tercih seçimi (hızlı, ucuz, sağlıklı, vegan)
- Mutfak türü ve porsiyon seçimi

### 📖 Tarifler
- AI tarafından önerilen 3 tarif
- Eksik malzeme uyarısı
- Kalori ve süre bilgisi
- Adım adım yapılış

### 💬 AI Asistan
- Gerçek zamanlı sohbet
- Tarif hakkında soru sorma
- Alternatif öneriler

---

## 📁 Proje Yapısı

```
ai-chef/
├── 🔙 backend/
│   ├── app/
│   │   ├── main.py              # Ana uygulama
│   │   ├── config.py            # Ayarlar
│   │   ├── database.py          # Veritabanı bağlantısı
│   │   ├── models.py            # Veritabanı modelleri
│   │   ├── schemas.py           # Pydantic şemaları
│   │   ├── routers/
│   │   │   ├── auth.py          # Kimlik doğrulama
│   │   │   ├── ingredients.py   # Malzeme işlemleri
│   │   │   ├── recipes.py       # Tarif işlemleri
│   │   │   └── chat.py          # AI sohbet
│   │   ├── services/
│   │   │   └── gemini_service.py # AI servisi
│   │   └── utils/
│   │       └── auth_utils.py    # JWT işlemleri
│   ├── .env                     # Ortam değişkenleri
│   └── requirements.txt         # Python bağımlılıkları
├── 🎨 frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx         # Ana sayfa
│   │   │   ├── layout.tsx       # Layout
│   │   │   ├── globals.css      # Global stiller
│   │   │   └── dashboard/
│   │   │       └── page.tsx     # Dashboard
│   │   └── lib/
│   │       └── api.ts           # API helper
│   ├── .env.local               # Frontend ortam değişkenleri
│   └── package.json             # Node bağımlılıkları
├── 🤗 huggingface-deploy/
│   ├── app.py                   # Gradio uygulaması
│   └── requirements.txt         # Deploy bağımlılıkları
└── 📄 README.md
```

---

## 🎯 Gelecek Özellikler

- [ ] 📸 Fotoğraftan malzeme tanıma
- [ ] 📅 Haftalık yemek planlayıcı
- [ ] 🛒 Alışveriş listesi oluşturma
- [ ] 🔥 Kalori/makro detaylı hesabı
- [ ] 🗣️ Sesli mutfak asistanı
- [ ] 👨‍👩‍👧‍👦 Aile profili desteği
- [ ] 📱 Mobil uygulama

---
## 🎨 Projeye Ait Fotoğraflar
<img width="3420" height="1898" alt="image" src="https://github.com/user-attachments/assets/650ddd70-d3c6-4c1d-badf-e02a1d3c29d7" />
<img width="3420" height="1898" alt="image" src="https://github.com/user-attachments/assets/8ea6487a-2235-47c4-a09c-26a9da8033c0" />
<img width="3420" height="1898" alt="image" src="https://github.com/user-attachments/assets/e18b304c-b0f4-4c87-98e9-b86fc0fcb3f8" />
<img width="3420" height="1898" alt="image" src="https://github.com/user-attachments/assets/b7bbd5e0-0ceb-4502-93cc-aae98b9467de" />
<img width="3420" height="1898" alt="image" src="https://github.com/user-attachments/assets/6360a5ea-2934-415f-aef9-9307ff357bf9" />
<img width="3420" height="1898" alt="image" src="https://github.com/user-attachments/assets/b08797cd-a056-40a1-ad8d-0dfc262789ab" />
<img width="3420" height="1898" alt="image" src="https://github.com/user-attachments/assets/bacf8801-235a-47e1-a4b1-e1bb751c6de8" />
<img width="3420" height="1898" alt="image" src="https://github.com/user-attachments/assets/0bfbb128-f545-4f4c-8cd0-a4d1483d4219" />
<img width="3420" height="1898" alt="image" src="https://github.com/user-attachments/assets/9161c42b-fa04-4b96-935c-ce6f21fed885" />
<img width="3420" height="1898" alt="image" src="https://github.com/user-attachments/assets/1dcb058d-eec1-42fa-aff6-1c945dbaaa0d" />
<img width="3420" height="1898" alt="image" src="https://github.com/user-attachments/assets/8f89b50d-57bb-4a18-afeb-86d109c43972" />

---

## 👩‍💻 Geliştirici

**Esra Koç**

---

## 📄 Lisans

MIT License

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
