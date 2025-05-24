from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import psycopg2
import pandas as pd
import io
import os
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

# Database configuration from environment variables (for Render)
db_config = {
    'host': os.environ.get("DB_HOST"),
    'user': os.environ.get("DB_USER"),
    'password': os.environ.get("DB_PASSWORD"),
    'database': os.environ.get("DB_NAME"),
    'port': os.environ.get("DB_PORT", 5432)
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        logging.error("Database connection failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Database connection failed.")

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS network (
            id SERIAL PRIMARY KEY,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting app, creating table if not exists.")
    create_table()
    yield

app = FastAPI(lifespan=lifespan)

# Allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload CSV Endpoint
@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

        contents = await file.read()
        logging.info(f"Received file: {file.filename}, Size: {len(contents)} bytes")

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
        logging.error("Error during file upload: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# List Uploaded Files
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
        logging.error("Error listing files: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Get CSV data by file ID
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
        logging.error("Error fetching file ID %s: %s", file_id, str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Serve static frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Serve frontend index.html at root path
@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = "frontend/index.html"
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html not found")
    with open(index_path) as f:
        return f.read()

# Optional: DB connection test
@app.get("/test-db/")
async def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"message": "Connected to DB", "tables": tables}
    except Exception as e:
        return {"error": str(e)}
