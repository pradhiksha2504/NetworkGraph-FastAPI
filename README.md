# 📊 Network Graph Visualization with FastAPI

This project enables users to upload CSV files, store them in a **PostgreSQL** database, and visualize them as interactive network graphs using **Highcharts**. The backend is powered by **FastAPI**, and the frontend is built with **HTML**, **CSS**, and **JavaScript**.

---

## 🚀 Features

* 📤 Upload CSV files via a user-friendly frontend
* 🗄 Store uploaded files securely in **PostgreSQL**
* 📂 Fetch and list stored CSVs dynamically
* 🌐 Generate interactive **Network Graphs** from selected CSV data

---

## 🧰 Tech Stack

| Layer        | Technology               |
| ------------ | ------------------------ |
| **Backend**  | FastAPI, PostgreSQL      |
| **Frontend** | HTML, CSS, JavaScript    |
| **Graph**    | Highcharts Network Graph |
| **Database** | PostgreSQL               |

> ⚠️ Note: The original README mentioned MySQL, but this project uses **PostgreSQL**.

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/pradhikshaks2504/NetworkGraph-FastAPI.git
cd NetworkGraph-FastAPI
```

---

### 2️⃣ Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ PostgreSQL Database Setup

1. Install and start PostgreSQL server.
2. Create a new database:

```sql
CREATE DATABASE network_graphs;
```

3. (Optional) Create a user and assign privileges:

```sql
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE network_graphs TO your_user;
```

4. Update your `main.py` with correct database credentials (connection string).

---

### 4️⃣ Run the Backend Server

```bash
uvicorn main:app --reload
```

API will be available at:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 5️⃣ Frontend Setup

The frontend is located in the `frontend/` folder. You have two options:

* **Option 1**: Serve it via FastAPI backend (already configured).
* **Option 2**: Open `frontend/index.html` directly in your browser.

---

### 6️⃣ API Endpoints

| Endpoint              | Method | Description                         |
| --------------------- | ------ | ----------------------------------- |
| `/upload-csv/`        | POST   | Upload CSV file                     |
| `/files/`             | GET    | List uploaded CSV file IDs          |
| `/csv-data/{file_id}` | GET    | Fetch CSV data by file ID           |
| `/test-db/`           | GET    | Test database connection (optional) |
| `/`                   | GET    | Serve `index.html` frontend page    |

---

### 7️⃣ Generating Network Graphs

1. Upload one or more CSV files through the frontend.
2. Select the desired files from the list.
3. Click **Generate Network Graph**.
4. Enjoy the interactive network visualization powered by **Highcharts**.

---

## 🌐 Deployment Options

### ✅ 1. Render (Recommended for FastAPI + PostgreSQL)

Render is an excellent platform for deploying full-stack Python apps with PostgreSQL support.

#### 🔧 Steps to Deploy on Render:

1. Push your project to GitHub (if not done already).

2. Sign in to [Render](https://render.com/).

3. Create a new **Web Service**:

   * Connect your GitHub repo.
   * Choose **Python** environment.
   * Use the following **Start Command**:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 10000
   ```

4. Set `requirements.txt` as the build command.

5. Add environment variables, for example:

   ```env
   DATABASE_URL=postgresql://user:password@hostname/dbname
   ```

6. Add a PostgreSQL database from Render's dashboard and connect it via the environment variable.

---

## 📁 Project Structure

```
📦 network-graph-visualization
│
├── 📂 frontend/                # Frontend files (HTML, CSS, JS)
│   ├── index.html             # Frontend entry point
│   └── styles.css             # Styling
│
├── 📂 sampleCSVData/          # Sample CSV files for testing
│
├── main.py                    # FastAPI backend implementation
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 🙋‍♀️ Contributing

Feel free to fork the repository, submit pull requests, or raise issues. Contributions and suggestions are always welcome!

---
