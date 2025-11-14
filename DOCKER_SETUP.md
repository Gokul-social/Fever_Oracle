# Docker Setup Guide

## Quick Start

1. **Build and start all services:**
   ```bash
   docker-compose up -d --build
   ```

2. **Check service status:**
   ```bash
   docker-compose ps
   ```

3. **View logs:**
   ```bash
   # All services
   docker-compose logs -f
   
   # Specific service
   docker-compose logs -f backend
   docker-compose logs -f kafka-producer
   ```

4. **Access the application:**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5000
   - Kafka Monitor: http://localhost:8080/kafka-monitor

## Services

### Backend
- **Port**: 5000
- **Health Check**: http://localhost:5000/api/health
- **Dependencies**: PostgreSQL, Kafka

### Frontend
- **Port**: 8080
- **Dependencies**: Backend

### PostgreSQL
- **Port**: 5432
- **Database**: fever_oracle
- **User**: fever_user
- **Password**: fever_password

### Zookeeper
- **Port**: 2181
- **Dependencies**: None

### Kafka
- **Ports**: 9092 (external), 9093 (internal)
- **Dependencies**: Zookeeper

### Kafka Producer
- **Dependencies**: Kafka, Backend
- **Function**: Generates mock data and publishes to Kafka topics

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs

# Restart specific service
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build --force-recreate backend
```

### Kafka connection issues
```bash
# Check Kafka is healthy
docker-compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9093

# Check topics
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9093
```

### Backend can't connect to Kafka
- Ensure Kafka health check passes
- Check KAFKA_BOOTSTRAP_SERVERS environment variable
- Verify network connectivity: `docker-compose exec backend ping kafka`

### Frontend can't connect to backend
- Check backend is healthy: `curl http://localhost:5000/api/health`
- Verify VITE_API_URL environment variable
- Check browser console for CORS errors

### Reset everything
```bash
# Stop and remove all containers, networks, and volumes
docker-compose down -v

# Rebuild and start
docker-compose up -d --build
```

## Development Mode

For development with hot-reload:

1. Services use volume mounts for code
2. Changes to code are reflected immediately
3. Use `docker-compose logs -f` to see changes

## Production Considerations

For production deployment:

1. Remove volume mounts for code
2. Use gunicorn instead of Flask dev server
3. Set proper environment variables
4. Use secrets management
5. Enable SSL/TLS
6. Configure proper logging
7. Set resource limits

## Environment Variables

Key environment variables:

- `FLASK_ENV`: development or production
- `PORT`: Backend port (default: 5000)
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka connection string
- `VITE_API_URL`: Backend API URL for frontend
- `POSTGRES_*`: Database configuration
