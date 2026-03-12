#!/bin/bash

# OSINT Platform 2026 - Complete Deployment Script
# Production-ready deployment with all checks

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_section() { echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n${BLUE}$1${NC}\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"; }

log_section "OSINT Platform 2026 - Full Deployment"

# 1. Check prerequisites
log_section "1. Checking Prerequisites"

if ! command -v docker &> /dev/null; then
    log_error "Docker not installed"
    exit 1
fi
log_info "✓ Docker found: $(docker --version)"

if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose not installed"
    exit 1
fi
log_info "✓ Docker Compose found: $(docker-compose --version)"

# 2. Create environment
log_section "2. Configuring Environment"

if [ ! -f .env ]; then
    log_info "Creating .env from template..."
    cp .env.example .env
    
    # Generate JWT secret
    JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/JWT_SECRET_KEY=.*/JWT_SECRET_KEY=$JWT_SECRET/" .env
    else
        sed -i "s/JWT_SECRET_KEY=.*/JWT_SECRET_KEY=$JWT_SECRET/" .env
    fi
    log_info "✓ Generated JWT secret"
else
    log_warn ".env already exists, skipping creation"
fi

# 3. Create required directories
log_section "3. Creating Directory Structure"

mkdir -p reports ssl .github/workflows
chmod 755 reports
log_info "✓ Directories created"

# 4. Verify docker-compose.yml
log_section "4. Validating docker-compose.yml"

if docker-compose config > /dev/null 2>&1; then
    log_info "✓ docker-compose.yml is valid"
else
    log_error "docker-compose.yml validation failed"
    docker-compose config
    exit 1
fi

# 5. Build images
log_section "5. Building Docker Images"

log_info "Building API image..."
docker-compose build api
log_info "✓ API image built"

log_info "Building Worker image..."
docker-compose build worker
log_info "✓ Worker image built"

log_info "Building Web image..."
docker-compose build web
log_info "✓ Web image built"

# 6. Pull other images
log_section "6. Pulling Base Images"

log_info "Pulling PostgreSQL..."
docker pull postgres:15-alpine

log_info "Pulling Redis..."
docker pull redis:7-alpine

log_info "Pulling Tor..."
docker pull osminogin/tor-simple:latest

log_info "✓ All base images ready"

# 7. Start services
log_section "7. Starting Services"

log_info "Starting all services..."
docker-compose up -d

log_info "Waiting for services to be healthy (30 seconds)..."
sleep 30

# 8. Verify services
log_section "8. Verifying Services"

if docker-compose ps | grep -q "osint-postgres.*Up"; then
    log_info "✓ PostgreSQL is running"
else
    log_error "PostgreSQL failed to start"
    docker-compose logs postgres
    exit 1
fi

if docker-compose ps | grep -q "osint-redis.*Up"; then
    log_info "✓ Redis is running"
else
    log_error "Redis failed to start"
    docker-compose logs redis
    exit 1
fi

if docker-compose ps | grep -q "osint-api.*Up"; then
    log_info "✓ API is running"
else
    log_error "API failed to start"
    docker-compose logs api
    exit 1
fi

if docker-compose ps | grep -q "osint-web.*Up"; then
    log_info "✓ Web is running"
else
    log_error "Web failed to start"
    docker-compose logs web
    exit 1
fi

# 9. Health checks
log_section "9. Running Health Checks"

log_info "Checking API health..."
if curl -s http://localhost:8000/health | grep -q "ok"; then
    log_info "✓ API health check passed"
else
    log_warn "API health check failed - may need more time"
fi

log_info "Checking PostgreSQL..."
if docker-compose exec -T postgres pg_isready -U osint &>/dev/null; then
    log_info "✓ PostgreSQL is responding"
else
    log_warn "PostgreSQL not yet ready"
fi

log_info "Checking Redis..."
if docker-compose exec -T redis redis-cli ping &>/dev/null; then
    log_info "✓ Redis is responding"
else
    log_warn "Redis not yet ready"
fi

# 10. Display status
log_section "10. Deployment Complete!"

log_info "All services are running"
log_info ""
log_info "Service URLs:"
log_info "  📱 Frontend:    http://localhost:3000"
log_info "  📚 API Docs:    http://localhost:8000/docs"
log_info "  🔄 API Swagger: http://localhost:8000/redoc"
log_info ""
log_info "Administrative URLs (if dev mode):"
log_info "  🗄️  pgAdmin:         http://localhost:5050"
log_info "  🔴 Redis Commander: http://localhost:8081"
log_info "  💾 Adminer:         http://localhost:8080"
log_info ""

docker-compose ps

log_info ""
log_info "Configuration:"
docker-compose config --services

log_info ""
log_section "Next Steps"

log_info "1. Configure API keys:"
log_info "   $ nano .env"
log_info ""
log_info "2. View logs:"
log_info "   $ docker-compose logs -f api"
log_info ""
log_info "3. Run health checks:"
log_info "   $ ./scripts/health-check.sh"
log_info ""
log_info "4. Access frontend:"
log_info "   Open browser to http://localhost:3000"
log_info ""
log_info "5. For detailed operations:"
log_info "   $ cat DEPLOYMENT.md"
log_info ""

log_section "🎉 Deployment Successful!"

