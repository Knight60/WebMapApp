# WebMapApp

> ชุดตัวอย่าง Web Map API (Leaflet, MapLibre GL JS, CesiumJS) พร้อมรายงานสรุปโครงงาน Capstone
> ภายใต้การอบรม **GeoAI & GI Vibe Coding** — frontend เป็น Vite + TypeScript เสิร์ฟผ่าน GitHub Pages
> และ backend เป็น FastAPI (Python) สำหรับเสิร์ฟ API และไฟล์ static

[![Live Demo](https://img.shields.io/badge/demo-GitHub%20Pages-2ea44f)](https://knight60.github.io/WebMapApp/)
[![Frontend](https://img.shields.io/badge/frontend-Vite%20%2B%20TypeScript-646cff)](frontend/)
[![Backend](https://img.shields.io/badge/backend-FastAPI-009688)](backend/)

**🔗 Live:** https://knight60.github.io/WebMapApp/

---

## ✨ Features

- **Leaflet** — แผนที่ 2 มิติเบื้องต้น พร้อมชั้นข้อมูลขอบเขตจังหวัด (GeoJSON)
- **MapLibre GL JS** — แผนที่ vector tile แบบ WebGL
- **CesiumJS** — โลก 3 มิติ (globe)
- **รายงานสรุป Capstone** — อินโฟกราฟิก D3.js วิเคราะห์ข้อมูลผู้เข้าร่วมอบรม (โดนัท 2 ชั้น + กราฟแท่ง แยก ออนไซต์/ออนไลน์)
- **FastAPI backend** — REST API + เสิร์ฟ frontend ที่ build แล้ว (พร้อม CORS และ MIME type สำหรับ `.geojson`)

## 🛠 Tech Stack

| ส่วน | เทคโนโลยี |
|------|-----------|
| Frontend | Vite 8, TypeScript, Leaflet, MapLibre GL JS, CesiumJS, D3.js, Tailwind (CDN) |
| Backend | Python 3.11, FastAPI, Uvicorn |
| Deploy | GitHub Pages (frontend), Docker / Cloud Run (backend) |

## 📁 Project Structure

```
WebMapApp/
├── frontend/                 # Vite + TypeScript (multi-page)
│   ├── index.html            # หน้าแรก รวมลิงก์เดโม
│   ├── leaflet.html          # เดโม Leaflet
│   ├── maplibre.html         # เดโม MapLibre GL JS
│   ├── cesium.html           # เดโม CesiumJS
│   ├── capstone.html         # รายงานสรุป Capstone (D3.js)
│   ├── src/                  # โค้ด TypeScript ของแต่ละเดโม
│   ├── public/               # static assets (favicon, data, cesium runtime)
│   └── vite.config.ts        # multi-page input + publish dist → backend/static
└── backend/                  # FastAPI
    ├── app/main.py           # แอป, routes, mount static
    ├── app/config.py         # ตั้งค่าผ่าน environment variables
    ├── Dockerfile            # image สำหรับ Cloud Run / container ทั่วไป
    └── requirements.txt
```

## 🚀 Getting Started

### ข้อกำหนดเบื้องต้น (Prerequisites)

- Node.js ≥ 20
- Python ≥ 3.11

### Frontend

```bash
cd frontend
npm install            # ติดตั้ง dependencies (postinstall จะ copy Cesium assets ให้)
npm run dev            # dev server ที่ http://localhost:5173
npm run build          # build ไปที่ dist/ และ publish เข้า backend/static
npm run preview        # ดูตัวอย่างผลลัพธ์ที่ build แล้ว
```

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate           # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload    # http://localhost:8000
```

- API: http://localhost:8000/api
- เอกสาร (Swagger): http://localhost:8000/docs
- Health check: http://localhost:8000/api/health

> เมื่อรัน `npm run build` ในฝั่ง frontend แล้ว backend จะเสิร์ฟหน้าเว็บที่ build ไว้ที่ `/` โดยอัตโนมัติ

## ⚙️ Configuration (Backend)

ตั้งค่าผ่าน environment variables (ดูตัวอย่างที่ [backend/.env.example](backend/.env.example)):

| ตัวแปร | ค่าเริ่มต้น | คำอธิบาย |
|--------|-----------|----------|
| `CORS_ORIGINS` | `http://localhost:5173` | รายการ origin ที่อนุญาต (คั่นด้วย `,`) |
| `APP_NAME` | `WebMapApp API` | ชื่อแอปที่แสดงใน API/เอกสาร |
| `PORT` | `8080` | พอร์ต (Cloud Run กำหนดให้อัตโนมัติ) |

## 🌐 Deployment

### Frontend → GitHub Pages

frontend ถูก build ด้วย base path `/WebMapApp/` แล้ว push ไปยัง branch `gh-pages`:

```bash
cd frontend
npx vite build --base=/WebMapApp/
cd dist && touch .nojekyll
git init && git checkout -b gh-pages
git add -A && git commit -m "Deploy to GitHub Pages"
git push -f https://github.com/Knight60/WebMapApp.git gh-pages
```

จากนั้นเปิด **Settings → Pages → Source: `gh-pages` / (root)**
เว็บจะออนไลน์ที่ https://knight60.github.io/WebMapApp/

### Backend → Docker / Cloud Run

GitHub Pages รัน Python ไม่ได้ (static เท่านั้น) จึงต้อง deploy backend แยกไปยัง host ที่รองรับ Python:

```bash
cd backend
# build frontend ก่อนเพื่อให้ static/ เป็นเวอร์ชันล่าสุด (base เริ่มต้น = /)
docker build -t webmapapp .
docker run -p 8080:8080 -e CORS_ORIGINS="https://knight60.github.io" webmapapp
```

รองรับ **Google Cloud Run**, Render, Railway, Fly.io ฯลฯ (ใช้ [Dockerfile](backend/Dockerfile) ที่มีอยู่)
อย่าลืมตั้ง `CORS_ORIGINS` ให้ครอบคลุมโดเมน frontend

## 📡 API Endpoints

| Method | Path | คำอธิบาย |
|--------|------|----------|
| `GET` | `/api` | ข้อมูลแอปและลิงก์เอกสาร |
| `GET` | `/api/health` | health check |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/*` | เสิร์ฟ frontend ที่ build แล้ว (ถ้ามี `static/`) |

## 📄 License

จัดทำเพื่อการอบรม GeoAI & GI Vibe Coding (GISTDA)
