# 🗺️ Uriel Mazabuel last 10 years Locations on business days

A data-driven dashboard to visualize and analyze Uriel Mazabuel's business day locations and routes over the last decade.

---

## ✨ Summary

This project provides an interactive web dashboard to explore, map, and analyze Uriel Mazabuel's business day visits using FastAPI (backend) and Streamlit + Folium (frontend). All you need is your data and a `.env` file—just clone, run, and explore!

---

## 👀 Overview

- **Backend:** FastAPI serves filtered visit data from CSV files.
- **Frontend:** Streamlit app with Folium maps for route visualization and statistics.
- **Deployment:** Easily run both services with Docker Compose.

---

## 🚀 Features

- 📅 **Date-based filtering**: Select a date to view all visits for that day.
- 🗺️ **Interactive map**: Visualize routes and locations with Folium/Leaflet.
- 📊 **Statistics**: See origin, destination, and duration for each visit.
- ⚡ **Fast**: Data is loaded once at startup for instant filtering.
- 🐳 **Easy deployment**: One command to run everything with Docker Compose.

---
```
## 📁 File System Format

project-root/
│
├── backend/
│ ├── data/ # CSV data files
│ ├── main.py # FastAPI entry point
│ ├── models/ # (if needed)
│ ├── services/
│ │ └── filtering_visits.py # Filtering service
│ └── settings.py # App settings
│
├── frontend/
│ ├── app.py # Streamlit app entry point
│ ├── components/ # UI components (map, stats, sidebar)
│ ├── services/ # API client for backend
│ └── utils/ # (optional) data helpers
│
├── docker/
│ ├── docker-compose.yml
│ ├── Dockerfile.backend
│ └── Dockerfile.frontend
│
├── requirements.txt # Shared dependencies
└── README.md # This file
```
---

## 🛠️ Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- Your CSV data file(s) in `backend/data/`
- A `.env` file with any required environment variables (see `settings.py` for details)

---

## 🚦 Getting Started

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Add your data:**
   - Place your CSV file(s) in `backend/data/`
   - Example: `backend/data/visitas_business_days.csv`

3. **Add your `.env` file:**
   - Copy or create a `.env` file in the project root or backend directory.

4. **Build and run the containers:**
   ```bash
   docker compose -f docker/docker-compose.yml up --build
   ```

5. **Access the app:**
   - Frontend: [http://localhost:8501](http://localhost:8501)
   - Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to open an issue or submit a pull request.

---

## 📬 Contact

- **Author:** Diego Lesmes
- **Email:** <dalejandro24203@gmail.com>
- **GitHub:** [your-github-profile]([https://github.com/your-github-profile](https://github.com/DLesmes))

---

> Made with ❤️, FastAPI, Streamlit, and Folium.

