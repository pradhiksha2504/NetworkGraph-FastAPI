import os
import psycopg2
from fastapi import FastAPI, UploadFile, File, HTTPException


DATABASE_URL="postgresql://csv_network_user:znkQlDwPH0VR5voj7sfGLpQhHC4kHj4C@dpg-d0oqdu6mcj7s73df39p0-a.oregon-postgres.render.com/csv_network"


def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        # logging.error("Database connection failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Database connection failed.")
