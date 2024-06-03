# LiveDataStream

LiveDataStream is a project for real-time data streaming between a server and clients using FastAPI for the server and React with Vite for the client.

## Server

The `server` directory contains the server-side code written in FastAPI, a modern web framework for building APIs with Python.

### Features

- Provides REST API endpoints for adding values to the database and streaming real-time updates to clients.
- Utilizes Server-Sent Events (SSE) for real-time communication with clients.
- Uses SQLite database for storing data.

### Getting Started

To run the server:

1. Navigate to the `server` directory.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   On Windows:
   `bash
    .venv\Scripts\activate
    `

   On macOS and Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Install the dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the server by running:
   ```bash
   uvicorn main:app --reload
   ```

For more details on the server-side code and usage, see the [document.](server/README.md)

## Client
The `client` directory contains the client-side code written in React with Vite, a fast build tool that significantly improves the development experience.

### Features
- Built with React for a dynamic and interactive user interface.
- Utilizes Vite for fast and optimized development.
- Communicates with the server to display real-time updates.

### Getting Started
To run the client:
1. Navigate to the `client` directory.
2. Install the dependencies:
   - If using npm, run:
     ```bash
     npm install
     ```
   - If using Yarn, run:
     ```bash
     yarn install
     ```
3. Start the development server:
   - If using npm, run:
     ```bash
     npm run dev
     ```
   - If using Yarn, run:
     ```bash
     yarn run dev
     ```

For more details on the client-side code and usage, see the [document](client/README.md).

## Contribution
Contributions are welcome! If you have any suggestions, feature requests, or bug reports, feel free to open an issue or submit a pull request.


## Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance), web framework for building APIs with Python 3.10+.
- [React](https://reactjs.org/): A JavaScript library for building user interfaces.
- [Vite](https://vitejs.dev/): A fast build tool that significantly improves the development experience for modern web projects.

## About
This project is maintained by Azim Miah. Feel free to contact me at azimruet28@gmail.com for any inquiries or collaborations.

