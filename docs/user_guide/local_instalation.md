# Local Deployment Using Docker Compose

This section explains how to set up and run FireFly locally using Docker Compose.

---

## 🐳 Prerequisites

1. Install Docker Desktop:  
   [https://docs.docker.com/desktop](https://docs.docker.com/desktop)

---

## ⚙️ Build and Start

### 1. Build the project:

```bash
docker-compose build
```

### 2. Review environment variables:

Open the `.env` file in the root directory and adjust the default configuration if needed.  
This file contains settings like database credentials, ports, and environment names.

### 3. Start the services:

```bash
docker-compose up -d
```

---

## 🌐 Service URLs

Once the services are running, you can access the system at the following URLs:

| Service | URL |
|--------|-----|
| **Frontend** | [http://localhost](http://localhost) |
| **Backend API** | [http://localhost/api/](http://localhost/api/) |
| **Swagger UI** (interactive OpenAPI docs) | [http://localhost/docs](http://localhost/docs) |
| **ReDoc** (alternative OpenAPI docs) | [http://localhost/redoc](http://localhost/redoc) |
| **Celery Admin (Flower)** | [http://localhost:5555](http://localhost:5555) |
| **Traefik Dashboard** | [http://localhost:8090](http://localhost:8090) |

---

## 🗃️ Database Access

You can connect to the MySQL database locally at:

```
Host: localhost  
Port: 3306
```

Use any database client such as **HeidiSQL** or **DataGrip**.  
Credentials can be found in the `.env` file at the root of the project.

---

## ✅ That's it!

Your FireFly instance should now be running locally.  
You can start developing, launching tests, or working with scripts immediately.

---
