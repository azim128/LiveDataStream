# Project Documentation

## Overview
This project is a FastAPI application that supports adding values to an SQLite database and notifying connected clients via Server-Sent Events (SSE). The project is organized into several modules for better modularity and maintainability.

## Project Structure
```
LiveDataStream/
│
├── config/
│   ├── db_config.py
│   └── logging_config.py
├── utils/
│   └── db_utils.py
├── services/
│   └── sse_service.py
├── routers/
│   └── router.py
├── main.py
├── requirements.txt
├── readme.md
└── logs/
    └── app.log
```

### Modules Overview

1. **config/db_config.py**: Manages the database connection and ensures the database table is created.
2. **config/logging_config.py**: Configures logging settings.
3. **utils/db_utils.py**: Contains utility functions for database operations.
4. **routers/routes.py**: Defines the API endpoints.
5. **servies/sse_service.py**: Manages the Server-Sent Events (SSE) clients and notification system.
6. **main.py**: Initializes the FastAPI application, sets up middleware, and includes routes.

## Module Descriptions

### config/db_config.py
Handles database configuration.

```python
import sqlite3

def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.
    Ensures the 'data_values' table is created if it does not exist.
    """
    conn = sqlite3.connect("test.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS data_values (id INTEGER PRIMARY KEY, value TEXT)"
    )
    return conn
```

### config/logging_config.py
Configures logging for the application.

```python
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    """
    Sets up logging with a TimedRotatingFileHandler.
    Logs are stored in 'logs/app.log' and rotate at midnight.
    """
    logger = logging.getLogger("uvicorn.error")
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(
        "logs/app.log", when="midnight", interval=1, backupCount=10
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
```

### utils/db_utils.py
Contains utility functions for database operations.

```python
from config.db_config import get_db_connection

def add_value_to_db(value):
    """
    Adds a new value to the 'data_values' table in the database.
    
    Parameters:
    value (str): The value to be inserted into the database.
    """
    conn = get_db_connection()
    conn.execute("INSERT INTO data_values (value) VALUES (?)", (value,))
    conn.commit()
    conn.close()
```

### routers/router.py
Defines the API endpoints.

```python
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from utils.db_utils import add_value_to_db
from sse import notify_clients

router = APIRouter()

class ValueModel(BaseModel):
    value: str

@router.post("/add-value/")
async def add_value(data: ValueModel, background_tasks: BackgroundTasks):
    """
    Adds a new value to the database and notifies all connected SSE clients.
    
    Parameters:
    data (ValueModel): The data containing the value to be added.
    background_tasks (BackgroundTasks): FastAPI BackgroundTasks instance for background processing.
    
    Returns:
    dict: A success message.
    """
    add_value_to_db(data.value)
    background_tasks.add_task(notify_clients, f"{data.value}")
    return {"message": "Value added successfully"}

@router.get("/events/")
async def events():
    """
    Endpoint for clients to connect and receive server-sent events (SSE).
    
    Returns:
    StreamingResponse: A streaming response to send SSE to clients.
    """
    from fastapi.responses import StreamingResponse
    import asyncio
    from sse import clients

    async def event_generator():
        queue = asyncio.Queue()
        clients.append(queue)
        try:
            while True:
                message = await queue.get()
                yield f"data: {message}\n\n"
        except asyncio.CancelledError:
            clients.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

### service/sse_service.py
Manages Server-Sent Events (SSE) clients and notifications.

```python
import asyncio

clients = []

async def notify_clients(message: str):
    """
    Notifies all connected SSE clients with a given message.
    
    Parameters:
    message (str): The message to send to clients.
    """
    for client in clients:
        await client.put(message)
```

### main.py
Initializes the FastAPI application, sets up middleware, and includes routes.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from config import logging_config

app = FastAPI()

# Configure logging
logging_config.setup_logging()

allowed_origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## How to Run the Application
1. **Install dependencies**:
    ```bash
    pip install fastapi uvicorn pydantic
    ```

2. **Run the application**:
    ```bash
    python main.py
    ```

3. **Access the application**:
    Open your browser and navigate to `http://localhost:8000`.

## API Endpoints

### POST /add-value/
Adds a new value to the database and notifies all connected SSE clients.

**Request Body**:
```json
{
  "value": "your_value"
}
```

**Response**:
```json
{
  "message": "Value added successfully"
}
```

### GET /events/
Connects clients to receive server-sent events (SSE).

**Response**:
- `StreamingResponse`: Streams messages to connected clients.

## Logging
Logs are stored in the `logs/app.log` file and rotate at midnight, keeping the last 10 logs.

## SSE (Server-Sent Events)
Clients can connect to the `/events/` endpoint to receive real-time notifications when a new value is added to the database.

## Database
An SQLite database (`test.db`) is used to store the values. The database and the table (`data_values`) are created if they do not exist.

## Conclusion
This documentation covers the structure, modules, and usage of the FastAPI application. The modular design enhances readability, maintainability, and scalability.