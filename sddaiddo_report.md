# Lab 5 Report
## TA Demo Steps

### Deliverable 1: Training Container

```bash
# Build and run everything
docker compose up --build
```

- Show training output: `Training complete. Test accuracy: 1.0000`
- Show model saved message: `Model saved to /app/models/wine_model.pkl`
- Explaination: Docker ensures reproducible training — same Python version, same dependencies, same results on any machine.

### Deliverable 2: Inference Container + Logs

```bash
# In a second terminal — restart inference so it picks up the trained model
docker compose restart inference

# Health check
curl http://localhost:8081/health
# Expected: {"model_loaded": true, "status": "healthy"}

# Send a prediction
curl -X POST http://localhost:8081/predict -H "Content-Type: application/json" -d "{\"input\": [13.2, 1.78, 2.14, 11.2, 100, 2.65, 2.76, 0.26, 1.28, 4.38, 1.05, 3.40, 1050]}"
# Expected: {"prediction": "class_0"}

# Test error handling
curl -X POST http://localhost:8081/predict -H "Content-Type: application/json" -d "{\"bad_key\": [1,2,3]}"
# Expected: 400 error

# Show the bind-mounted log file on the host
type .\logs\predictions.log
```

- Explaination: The Dockerfile defines the container image — base image, dependencies, code, and startup command.
- Show `predictions.log` on the host to demonstrate bind mounts in action.

### Deliverable 3: Volume Lifecycle

```bash
# Stop containers (keep the named volume)
docker compose down

# Restart only inference — model persists in named volume
docker compose up inference
curl http://localhost:8081/health
# Expected: {"model_loaded": true, "status": "healthy"}

# Stop and DESTROY the named volume
docker compose down -v

# Restart inference — model is gone
docker compose up inference
curl http://localhost:8081/health
# Expected: {"model_loaded": false, "status": "model not found"}
```

- Explaination of the difference:
  * **Named volume**: Docker-managed storage that persists across container restarts. Only removed with `docker compose down -v` or `docker volume rm`.
  * **Bind mount**: Direct mapping of a host folder into the container. Files persist on the host regardless of what happens to the container or volumes.

## Key Concepts

1. **Why Docker for ML?** — Reproducibility (same environment everywhere), portability (works on any machine with Docker), isolation (no dependency conflicts)
2. **What is a Dockerfile?** — A blueprint/recipe for building a container image. It specifies the base image, dependencies, code to copy, and the command to run.
3. **Named volumes vs bind mounts:**
   * **Named volume** (`wine_model_storage:/app/models`) — Docker-managed, persists after containers stop, good for sharing data between containers. Deleted only with `docker volume rm` or `-v` flag.
   * **Bind mount** (`./logs:/app/logs`) — Maps a host directory directly into the container. Changes appear immediately on both sides. Good for development and inspecting output from the host.

---