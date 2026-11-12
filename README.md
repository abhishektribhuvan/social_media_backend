# Social Media REST API Backend

A production-ready, scalable RESTful API backend for a social media platform, built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. The application provides secure user authentication, post creation and management with strict ownership validation, an upvote/downvote system with vote aggregations, schema migrations via **Alembic**, and automated testing through **pytest**.

---

## Live Deployment

The API is currently live and accessible at:
- **Live URL**: [https://social-media-backend-0k4q.onrender.com]
- **Interactive API Documentation (Swagger UI)**: [https://social-media-backend-0k4q.onrender.com/docs]
- **Alternative Documentation (ReDoc)**: [https://social-media-backend-0k4q.onrender.com/redoc]

---

## Core Features

- **User Management**: User registration, profile retrieval, email uniqueness enforcement, and secure password hashing using `bcrypt`.
- **Authentication & Authorization**: OAuth2 with JWT (JSON Web Tokens) access tokens. Endpoints enforce token validation and scope permissions.
- **Posts Management (CRUD)**:
  - Create, read, update, and delete posts.
  - Ownership enforcement: users can only modify or delete their own posts.
  - Query parameters for server-side pagination (`limit`, `skip`) and title search filtering (`search`).
  - Automatic joins to calculate vote counts for each post.
- **Voting System**: Like/unlike toggle mechanism with duplicate vote prevention (409 Conflict) and cascade deletion.
- **Database Migrations**: Version-controlled database schema management using Alembic.
- **Data Validation & Serialization**: Robust schema validation using Pydantic v2.
- **Automated Testing**: Comprehensive test suite covering user flows, posts, authentication, and voting logic using `pytest`.
- **Containerization & CI/CD**: Ready-to-run `Dockerfile` and `docker-compose.yml` for multi-container orchestration, plus GitHub Actions CI pipeline configuration.

---

## Tech Stack

| Component | Technology |
|---|---|
| **Language** | Python 3.13 |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **ASGI Server** | [Uvicorn](https://www.uvicorn.org/) |
| **Database** | [PostgreSQL](https://www.postgresql.org/) |
| **ORM** | [SQLAlchemy](https://www.sqlalchemy.org/) |
| **Database Migrations** | [Alembic](https://alembic.sqlalchemy.org/) |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/) & `pydantic-settings` |
| **Security & Auth** | `python-jose` (JWT), `passlib` / `bcrypt` |
| **Containerization** | Docker, Docker Compose |
| **Testing** | `pytest`, `httpx` |
| **CI/CD** | GitHub Actions |

---

## Project Structure

```text
fastapi_backend/
├── .github/
│   └── workflows/
│       └── main.yml           # CI/CD workflow (build, test, deploy pipeline)
├── alembic/
│   ├── versions/              # Database migration revision scripts
│   ├── env.py                 # Alembic environment and metadata configuration
│   └── script.py.mako         # Migration script template
├── app/
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints (JSON & OAuth2 form login)
│   │   ├── posts.py           # Posts CRUD, search filtering, and pagination
│   │   ├── users.py           # User registration and profile lookup
│   │   └── votes.py           # Voting / like system endpoints
│   ├── config.py              # Application settings and environment validation
│   ├── database.py            # SQLAlchemy database engine and session setup
│   ├── main.py                # FastAPI entry point and CORS middleware configuration
│   ├── model.py               # Database ORM models (User, Post, Votes)
│   ├── oauth2.py              # JWT generation, token verification, and route dependencies
│   ├── schemas.py             # Pydantic request and response schemas
│   └── utils.py               # Password hashing and verification utilities
├── postman/                   # Postman collection and environment definitions
├── tests/
│   ├── conftest.py            # Pytest fixtures and test database setup
│   ├── database.py            # Test database connection configuration
│   ├── test_calculations.py   # Unit test examples
│   ├── test_posts.py          # Integration tests for posts router
│   ├── test_users.py          # Integration tests for users and auth routers
│   └── test_votes.py          # Integration tests for vote router
├── .env                       # Local environment variables (do not commit secrets)
├── .gitignore                 # Files and directories ignored by Git
├── alembic.ini                # Alembic CLI configuration
├── docker-compose.yml         # Container orchestration for API and PostgreSQL
├── Dockerfile                 # Container image build specifications
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

---

## Getting Started

### Prerequisites

- **Python**: Version 3.10+ (recommended: 3.13)
- **PostgreSQL**: Version 14+ or Docker installed
- **Git**

---

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd fastapi_backend
   ```

2. **Create and activate a virtual environment:**
   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

### Environment Configuration

Create a `.env` file in the project root directory with the following variables:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_postgres_password
DATABASE_USERNAME=postgres
DATABASE=your_postgres_db_name
SECRET_KEY=your_super_secret_jwt_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> **Note**: You can generate a secure `SECRET_KEY` using:
> ```bash
> openssl rand -hex 32
> ```

---

### Database Migrations

Apply database migrations to set up required tables and relations:

```bash
alembic upgrade head
```

To roll back a single revision:
```bash
alembic downgrade -1
```

---

### Running the Application

Start the local development server with auto-reload:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Once started, the API is accessible at:
- **Root Endpoint**: `http://127.0.0.1:8000/`
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## Running with Docker Compose

You can spin up both the FastAPI application and PostgreSQL database with one command:

```bash
docker-compose up --build
```

- The API will be accessible on `http://localhost:8001`.
- The PostgreSQL service runs in a dedicated container with automated health checks and persistent volume storage.

To stop the containers:
```bash
docker-compose down
```

---

## API Endpoints Reference

### Authentication

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/login` | Authenticate using JSON payload (`email`, `password`) | No |
| `POST` | `/token` | Authenticate using OAuth2 Password Request Form (Swagger UI compatible) | No |

### Users

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/user/` | Register a new user account | No |
| `GET` | `/user/{id}` | Retrieve public user information by ID | No |

### Posts

All posts endpoints require a valid Bearer token in the `Authorization` header.

| Method | Endpoint | Description | Query Parameters |
|---|---|---|---|
| `POST` | `/posts/` | Create a new post | None |
| `GET` | `/posts/` | Retrieve all posts with aggregated vote count | `limit` (default 10), `skip` (default 0), `search` (string) |
| `GET` | `/posts/{id}` | Retrieve a specific post by ID | None |
| `PUT` | `/posts/{id}` | Update a post (author only) | None |
| `DELETE` | `/posts/{id}` | Delete a post (author only) | None |

### Votes

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/vote/` | Upvote (`vote=1`) or remove vote (`vote=0`) on a post | Yes |

---

## Testing

The project uses `pytest` for unit and integration testing. Tests utilize an isolated PostgreSQL test database to prevent polluting development or production data.

Run all tests:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v -s
```

Run a specific test module:
```bash
pytest tests/test_posts.py
```

---

## CI/CD Pipeline

A continuous integration workflow is configured via `.github/workflows/main.yml`. On every `push` and `pull_request`, GitHub Actions:
1. Spins up a PostgreSQL service container.
2. Checks out the code and installs Python 3.13 with dependencies.
3. Executes the full test suite with `pytest`.
4. Prepares deployment steps upon successful test completion.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

