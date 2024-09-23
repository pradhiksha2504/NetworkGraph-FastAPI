from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import mysql.connector
import pandas as pd
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_config = {
    'host': 'localhost',
    'user': 'your_username', 
    'password': 'your_password',  
    'database': 'your_database_name',  
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

@app.on_event("startup")
def startup():
    create_table()

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
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
        
        return {"message": "File uploaded and data insuccessfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/")
async def list_files():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, data FROM network")
        files = cursor.fetchall()
        cursor.close()
        conn.close()

        file_list = [{"id": row[0], "data": row[1]} for row in files]
        return {"files": file_list}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html") as f:
        return f.read()

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
