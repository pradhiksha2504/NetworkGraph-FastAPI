# Network Graph Visualization with FastAPI and MySQL

This project allows users to upload CSV files, fetch them from a MySQL database, and generate network graphs based on the CSV data. The frontend is built with HTML, CSS, and JavaScript, while the backend uses FastAPI to handle CSV uploads, serve the stored CSV files, and generate dynamic network graphs using Highcharts.

## Features

- Upload CSV files from the frontend to the backend.
- Store uploaded CSV files in a MySQL database.
- Fetch CSV files from the database and display them on the frontend.
- Generate network graphs from selected CSV files.

## Technologies Used

- **Backend**: FastAPI, MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/pradhikshaks2504/network-graph-visualization.git
cd network-graph-visualization
```

### 2. Install Backend Dependencies

Install the required Python dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Database Setup

1. Install and configure MySQL server.
2. Create a database for storing CSV files.
3. Create a table to store file metadata and data as needed.

For example:

```sql
CREATE DATABASE network_graphs;
USE network_graphs;

CREATE TABLE csv_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_data LONGBLOB
);
```
### 5. Run the Application

To start the FastAPI server, run:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

### 6. Frontend Setup

The frontend is located in the same directory and will interact with the FastAPI backend via API endpoints. Ensure that your frontend files (HTML, CSS, and JS) are served correctly, or open the `index.html` directly in your browser for testing.

### 7. API Endpoints

#### Upload CSV
- **POST** `/upload-csv/`
- Upload a CSV file to the backend and store it in the MySQL database.

#### Fetch CSV Files
- **GET** `/files/`
- Retrieve a list of uploaded CSV files.

#### Get CSV Data
- **GET** `/csv-data/{file_id}`
- Retrieve CSV data for a specific file.

### 8. Generating Network Graphs

Once CSV files are uploaded and stored, you can:
- Select files from the list.
- Click "Generate Network Graph" to visualize the network graph.

## Project Structure

```
📦 network-graph-visualization
│
├── 📂 static               # Contains static frontend files (HTML, CSS, JS)
│   ├── index.html          # Frontend entry point
│   └── styles.css          # Styling for the frontend
│
├── 📂 sampleCSVData              # Contains sample csv data files
│
├── main.py                 # FastAPI backend implementation
│
├── requirements.txt        # Python dependencies
│
└── README.md               # Project documentation
```



