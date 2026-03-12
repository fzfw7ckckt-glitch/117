# 🚀 OSINT Platform 2026 - Build & Deploy Guide

## ⚡ One-Command Deployment

```bash
cd osint-platform-2026
bash DEPLOY.sh
```

This single command will:
1. ✅ Check Docker prerequisites
2. ✅ Generate environment configuration
3. ✅ Build all Docker images (API, Worker, Web)
4. ✅ Pull all base images
5. ✅ Start all 7 services
6. ✅ Run health checks
7. ✅ Display service URLs

---

## 📊 What Gets Built

### Docker Images (3)
```
osint-api:latest              FastAPI backend
osint-worker:latest           Celery workers with Chrome/Tor
osint-web:latest              Next.js frontend
```

### Services (7)
```
osint-postgres    PostgreSQL 15         Database
osint-redis       Redis 7               Cache/Message Broker
osint-tor         Tor Proxy             Anonymized requests
osint-api         FastAPI               REST API (8000)
osint-worker      Celery                Task processing
osint-web         Next.js               Frontend (3000)
osint-nginx       Nginx                 Reverse proxy (optional)
```

---

## 🎯 Access After Deployment

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | Main dashboard |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **API Schema** | http://localhost:8000/redoc | ReDoc |
| **API Health** | http://localhost:8000/health | Health check |
| **pgAdmin** | http://localhost:5050 | Database admin |
| **Redis Commander** | http://localhost:8081 | Cache admin |
| **Adminer** | http://localhost:8080 | DB inspector |

---

## 📋 Prerequisites Check

Before running `DEPLOY.sh`, ensure:

```bash
# Docker installed
docker --version
# Output: Docker version 20.10+

# Docker Compose installed
docker-compose --version
# Output: Docker Compose version 1.29+

# At least 8GB RAM available
free -h

# At least 20GB disk space
df -h

# Python 3 for JWT generation
python3 --version
```

---

## 🔧 Step-by-Step Deployment

If you prefer manual control:

### Step 1: Prepare Environment
```bash
cd osint-platform-2026
cp .env.example .env
# Edit .env and add API keys if needed
nano .env
```

### Step 2: Validate Configuration
```bash
docker-compose config
```

### Step 3: Build Images
```bash
docker-compose build
```

### Step 4: Start Services
```bash
docker-compose up -d
```

### Step 5: Wait for Health
```bash
sleep 30
docker-compose ps
```

### Step 6: Verify All Services
```bash
./scripts/health-check.sh
```

---

## ✅ Verification Checklist

After deployment, verify:

```bash
# 1. All containers running
docker-compose ps

# 2. API responding
curl http://localhost:8000/health

# 3. Frontend accessible
curl http://localhost:3000

# 4. Database ready
docker-compose exec postgres pg_isready -U osint

# 5. Redis responding
docker-compose exec redis redis-cli ping

# 6. Worker active
docker-compose exec worker celery -A app.tasks.celery_app inspect ping

# 7. Logs clean (no errors)
docker-compose logs --tail 20
```

---

## 🚨 Troubleshooting Deployment

### Build Fails
```bash
# Clear cache and rebuild
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

### Port Already in Use
```bash
# Find what's using the port
lsof -i :8000
lsof -i :3000
lsof -i :5432

# Kill the process
kill -9 <PID>

# Or change ports in .env
API_PORT=8001
WEB_PORT=3001
```

### Services Won't Start
```bash
# Check specific service logs
docker-compose logs postgres
docker-compose logs redis
docker-compose logs api

# View detailed error
docker-compose logs --tail 50 api
```

### Out of Memory
```bash
# Check resource usage
docker stats

# Reduce worker concurrency in docker-compose.yml
# Change: --concurrency=4 to --concurrency=2

# Restart
docker-compose restart worker
```

---

## 📊 Deployment Timeline

| Step | Duration | Notes |
|------|----------|-------|
| Prerequisites check | 1s | Fast |
| Environment setup | 2s | JWT generation |
| docker-compose validation | 3s | Config check |
| Image building | 3-5 min | CPU intensive |
| Base image pulling | 2-3 min | Network dependent |
| Service startup | 10s | All containers launch |
| Health stabilization | 30s | Services settle |
| Health checks | 5s | Verification |
| **Total** | **6-10 min** | First-time build |

**Subsequent deployments**: 1-2 minutes (images cached)

---

## 🎛️ Configuration Options

### Minimal Deployment (1 worker)
```bash
docker-compose up -d
# Uses: 1 API, 1 Worker, all databases
```

### Standard Deployment (3 workers)
```bash
docker-compose up -d --scale worker=3
# Uses: 1 API, 3 Workers (4 concurrent each = 12 parallel tasks)
```

### High-Load Deployment (8 workers)
```bash
docker-compose up -d --scale worker=8
# Uses: 1 API, 8 Workers (4 concurrent each = 32 parallel tasks)
```

### Development Deployment (with tools)
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
# Adds: pgAdmin, Redis Commander, Adminer
```

### Production Deployment (with reverse proxy)
```bash
# Generate SSL certificates first
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes

# Start with production profile
docker-compose --profile prod up -d
# Adds: Nginx reverse proxy on 80/443
```

---

## 🔐 Security After Deployment

1. **Change Default Passwords**
   ```bash
   # Edit .env with strong passwords
   DB_PASSWORD=<new_strong_password>
   REDIS_PASSWORD=<new_strong_password>
   JWT_SECRET_KEY=<32_char_minimum>
   ```

2. **Add API Keys**
   ```bash
   nano .env
   # Fill in OSINT tool API keys
   SHODAN_API_KEY=xxx
   OPENAI_API_KEY=xxx
   GEOSPY_API_KEY=xxx
   ```

3. **Enable HTTPS (Production)**
   ```bash
   # Use SSL certificates and Nginx
   docker-compose --profile prod up -d
   ```

4. **Set Resource Limits**
   - Edit docker-compose.yml
   - Adjust `deploy.resources.limits`

5. **Configure Backups**
   - Set up automated PostgreSQL backups
   - Schedule with cron

---

## 📈 Performance After Deployment

### Monitor in Real-Time
```bash
docker stats
```

### Check Service Metrics
```bash
# CPU and memory per container
docker stats --no-stream

# Network usage
docker stats --format "table {{.Container}}\t{{.NetIO}}"
```

### Database Performance
```bash
docker-compose exec postgres psql -U osint -c "\du"
docker-compose exec postgres psql -U osint -c "SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database;"
```

### Redis Memory
```bash
docker-compose exec redis redis-cli info memory
```

### Celery Task Status
```bash
docker-compose exec worker celery -A app.tasks.celery_app inspect active
docker-compose exec worker celery -A app.tasks.celery_app inspect stats
```

---

## 🔄 Common Operations

### View Live Logs
```bash
docker-compose logs -f api
docker-compose logs -f worker
docker-compose logs -f web
```

### SSH Into Container
```bash
docker-compose exec api bash
docker-compose exec worker bash
docker-compose exec postgres bash
```

### Run Tests
```bash
docker-compose run --rm api pytest tests/ -v --cov=app
```

### Database Backup
```bash
docker-compose exec -T postgres pg_dump -U osint osint | gzip > backup.sql.gz
```

### Database Restore
```bash
gunzip < backup.sql.gz | docker-compose exec -T postgres psql -U osint osint
```

### Restart Services
```bash
# Single service
docker-compose restart api

# All services
docker-compose restart
```

### Scale Workers
```bash
docker-compose up -d --scale worker=5
```

### Update Configuration
```bash
nano .env
docker-compose restart
```

---

## 📚 What's Next?

### After Successful Deployment

1. **Verify Everything Works**
   ```bash
   ./scripts/health-check.sh
   ```

2. **Configure API Keys** (optional)
   ```bash
   nano .env
   docker-compose restart
   ```

3. **Create Your First Investigation**
   - Open http://localhost:3000
   - Create test investigation
   - Run reconnaissance

4. **Check API Documentation**
   - Visit http://localhost:8000/docs
   - Try sample requests

5. **Review Logs**
   ```bash
   docker-compose logs --tail 100 api
   ```

6. **Set Up Monitoring** (production)
   - Configure alerts
   - Set up log aggregation

---

## 📖 Full Documentation

- **Quick Reference**: `./QUICK_REFERENCE.sh`
- **Complete Guide**: `./DEPLOYMENT.md`
- **File Index**: `./INDEX.md`
- **Docker Overview**: `./DOCKER_README.md`

---

## 🎯 Success Indicators

✅ All 7 services running (`docker-compose ps`)
✅ API responding at port 8000
✅ Frontend accessible at port 3000
✅ PostgreSQL database initialized
✅ Redis cache operational
✅ Workers processing tasks
✅ No error logs in docker-compose logs

---

## 🆘 Emergency Rollback

If something goes wrong:

```bash
# Stop everything
docker-compose down

# Remove volumes (WARNING: deletes data!)
docker-compose down -v

# Clean up everything
docker system prune -a

# Start fresh
bash DEPLOY.sh
```

---

## 📞 Get Help

| Issue | Command |
|-------|---------|
| View all logs | `docker-compose logs --tail 100` |
| Check specific service | `docker-compose logs api` |
| See service status | `docker-compose ps` |
| Health check | `./scripts/health-check.sh` |
| Config validation | `docker-compose config` |
| Resource usage | `docker stats` |

---

**🚀 Ready to deploy? Run:** `bash DEPLOY.sh`

**Questions? See:** `DEPLOYMENT.md` or `QUICK_REFERENCE.sh`
