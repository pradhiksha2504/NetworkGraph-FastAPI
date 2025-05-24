from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import mysql.connector
import pandas as pd
import io
import os

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'p1a2s3s4',
    'database': 'csv_network'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS network (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# --- Lifespan handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield

app = FastAPI(lifespan=lifespan)

# --- CORS setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Upload CSV ---
@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")

        data_string = df.to_csv(index=False)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO network (data) VALUES (%s)", (data_string,))
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "File uploaded and data inserted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- List Files ---
@app.get("/files/")
async def list_files():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM network")
        files = cursor.fetchall()
        cursor.close()
        conn.close()

        file_list = [{"id": row[0]} for row in files]
        return {"files": file_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Get CSV Data by ID ---
@app.get("/csv-data/{file_id}")
async def get_csv_data(file_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM network WHERE id = %s", (file_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result is None:
            raise HTTPException(status_code=404, detail="File not found")

        csv_data = pd.read_csv(io.StringIO(result[0]))
        return csv_data.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Serve index.html ---
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = "frontend/index.html"
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html not found")
    with open(index_path) as f:
        return f.read()

# --- Test DB Connection ---
@app.get("/test-db/")
async def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"message": "Connected to DB", "tables": tables}
    except Exception as e:
        return {"error": str(e)}
