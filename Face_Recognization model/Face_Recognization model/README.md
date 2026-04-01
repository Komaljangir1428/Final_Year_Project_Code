# Face Recognition API

A fully functional face recognition system with **FastAPI** backend and **MongoDB** storage. Uses the `face_recognition` library (dlib-based) for 128-dimensional face encodings.

## Features

- **Attendance System** – Mark attendance via webcam or image upload; one record per person per day
- **Excel Export** – Download attendance records as `.xlsx` file
- **Web UI** – Full HTML interface at `http://localhost:8000/` for marking attendance, viewing records, and registering people
- **Register faces** – Upload images to register people with their face encodings
- **Recognize faces** – Upload an image to identify a person from the database
- **MongoDB storage** – Persistent storage of face encodings and attendance records

## Prerequisites

1. **Python 3.9+**
2. **MongoDB** – Running locally or remotely
   - Local: `mongodb://localhost:27017`
   - Or use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) for a free cloud database
3. **CMake** – Required for `dlib` (used by `face_recognition`). Install via:
   - Windows: `winget install Kitware.CMake` or download from [cmake.org](https://cmake.org/)
   - macOS: `brew install cmake`

## Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (optional – defaults work for local MongoDB):
   ```bash
   copy .env.example .env   # Windows
   # cp .env.example .env   # macOS/Linux
   ```
   Edit `.env` if needed:
   ```
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB_NAME=face_recognition_db
   ```

## KisanSetu Integration

This project is linked to **KisanSetu_Backend** for MGNREGA worker attendance:

- `.env` uses the same MongoDB as KisanSetu (kisansetu database)
- KisanSetu admin dashboard **Take Attendance** → Start: opens webcam, captures frames every 3s, sends to this API
- Ensure both run: **KisanSetu** on port 5000, **Face Recognition** on port 8000

Register workers first at http://localhost:8000/ (Face Recognition UI), then use the admin dashboard to mark attendance.

## Run the API

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- **Web UI (Attendance):** http://localhost:8000/
- **API docs:** http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Register a new person (form: `name`, `image`) |
| POST | `/api/recognize` | Recognize a face from image |
| POST | `/api/attendance/mark` | Mark attendance (form: `image`) |
| GET | `/api/attendance/records` | List attendance (optional: `?date=YYYY-MM-DD`) |
| GET | `/api/attendance/export` | Download Excel (optional: `?date=YYYY-MM-DD`) |
| GET | `/api/persons` | List all registered persons |
| GET | `/api/persons/{id}` | Get person by ID |
| POST | `/api/persons/{id}/add-face` | Add another face image to a person |
| DELETE | `/api/persons/{id}` | Delete a person |

## Example Usage

### Register a person (cURL)
```bash
curl -X POST "http://localhost:8000/api/register" \
  -F "name=John Doe" \
  -F "image=@path/to/photo.jpg"
```

### Recognize a face
```bash
curl -X POST "http://localhost:8000/api/recognize" \
  -F "image=@path/to/unknown_face.jpg"
```

### Using the Swagger UI
1. Open http://localhost:8000/docs
2. Use **POST /api/register** – enter name, upload image
3. Use **POST /api/recognize** – upload image to identify

## Configuration

- **TOLERANCE** (in `config.py`): Matching strictness. Lower = stricter (default: 0.6)
- **MODEL**: `"small"` (5 points) or `"large"` (68 points, more accurate)

## Project Structure

```
Face_Recognization model/
├── main.py              # FastAPI app entry point
├── config.py            # Configuration
├── database.py          # MongoDB connection
├── models.py            # Pydantic schemas
├── requirements.txt
├── static/
│   ├── index.html       # Attendance UI
│   ├── css/style.css
│   └── js/app.js
├── routers/
│   ├── persons.py       # Person/face API
│   └── attendance.py    # Attendance API
├── services/
│   ├── face_service.py
│   ├── person_service.py
│   └── attendance_service.py  # Attendance + Excel export
└── .env.example
```
