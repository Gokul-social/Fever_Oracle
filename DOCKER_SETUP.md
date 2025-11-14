# Docker Setup Instructions

## Important: Working Directory

If you're using a Git worktree, make sure to run `docker-compose` commands from the **worktree directory**, not the main git directory.

### Correct Location
```bash
cd /home/dijo404/.cursor/worktrees/Fever_Oracle/nEip0
docker-compose up -d
```

### Wrong Location (will fail)
```bash
cd /home/dijo404/git/Fever_Oracle  # ❌ Don't run from here
docker-compose up -d
```

## Building the Images

### Build all services
```bash
docker-compose build
```

### Build specific service
```bash
docker-compose build frontend
docker-compose build backend
```

### Build without cache (if having issues)
```bash
docker-compose build --no-cache
```

## Running the Services

### Start all services
```bash
docker-compose up -d
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f frontend
docker-compose logs -f backend
```

### Stop services
```bash
docker-compose down
```

### Stop and remove volumes
```bash
docker-compose down -v
```

## Troubleshooting

### Frontend Build Issues

If you get `npm ci` errors:

1. **Check you're in the right directory:**
   ```bash
   pwd
   # Should be: /home/dijo404/.cursor/worktrees/Fever_Oracle/nEip0
   ```

2. **Verify package-lock.json exists:**
   ```bash
   ls -la frontend/package-lock.json
   ```

3. **Rebuild without cache:**
   ```bash
   docker-compose build --no-cache frontend
   ```

4. **Check Docker build context:**
   The docker-compose.yml uses `context: ./frontend`, so make sure you're running from the project root.

### Backend Build Issues

1. **Check Python dependencies:**
   ```bash
   ls -la backend/requirements.txt
   ```

2. **Rebuild backend:**
   ```bash
   docker-compose build --no-cache backend
   ```

### Port Conflicts

If ports 5000, 8080, or 5432 are already in use:

1. **Modify docker-compose.yml:**
   ```yaml
   ports:
     - "5001:5000"  # Change host port
   ```

2. **Or stop conflicting services:**
   ```bash
   # Find process using port
   lsof -i :5000
   # Kill it
   kill <PID>
   ```

## Development Tips

- Use volumes for live code reloading (already configured)
- Check logs frequently: `docker-compose logs -f`
- Rebuild after dependency changes: `docker-compose build`
- Use `docker-compose exec` to run commands in containers:
  ```bash
  docker-compose exec frontend npm install
  docker-compose exec backend python app.py
  ```

