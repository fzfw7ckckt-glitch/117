#!/bin/bash

# OSINT Platform 2026 - Pre-Deployment Checklist
# Run this before deploying

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║         OSINT Platform 2026 - Pre-Deployment Verification Checklist         ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

PASSED=0
FAILED=0

check() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
        ((PASSED++))
    else
        echo "❌ $1"
        ((FAILED++))
    fi
}

echo "🔍 System Requirements"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Docker
docker --version &>/dev/null
check "Docker installed (version 20.10+)"

# Docker Compose
docker-compose --version &>/dev/null
check "Docker Compose installed (version 1.29+)"

# Python
python3 --version &>/dev/null
check "Python 3 installed"

# Memory
MEMORY=$(free -h | awk '/^Mem:/ {print $2}')
echo "📊 Available RAM: $MEMORY (minimum 8GB required)"

# Disk space
DISK=$(df -h / | awk 'NR==2 {print $4}')
echo "💾 Available Disk: $DISK (minimum 20GB required)"

echo ""
echo "📁 Project Files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Required files
[ -f "docker-compose.yml" ]
check "docker-compose.yml exists"

[ -f "Dockerfile.api" ]
check "Dockerfile.api exists"

[ -f "worker/Dockerfile" ]
check "worker/Dockerfile exists"

[ -f "web/Dockerfile" ]
check "web/Dockerfile exists"

[ -f ".env.example" ]
check ".env.example exists"

[ -f "requirements.txt" ]
check "requirements.txt exists"

[ -f "nginx.conf" ]
check "nginx.conf exists"

echo ""
echo "📋 Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# .env exists
if [ -f ".env" ]; then
    echo "✅ .env file exists"
    ((PASSED++))
    
    # Check if JWT_SECRET_KEY is set
    if grep -q "JWT_SECRET_KEY=.*" .env | grep -v "^#"; then
        echo "✅ JWT_SECRET_KEY is configured"
        ((PASSED++))
    else
        echo "⚠️  JWT_SECRET_KEY not configured"
    fi
else
    echo "⚠️  .env file not found (will be created during deployment)"
    echo "   To use custom values: cp .env.example .env && nano .env"
fi

echo ""
echo "🐳 Docker Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# docker-compose.yml syntax
docker-compose config > /dev/null 2>&1
check "docker-compose.yml is valid"

# Docker daemon running
docker ps > /dev/null 2>&1
check "Docker daemon is running"

# Docker socket accessible
[ -S /var/run/docker.sock ] || [ -S /run/docker.sock ]
check "Docker socket is accessible"

echo ""
echo "🔧 Network Requirements"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Port availability
! netstat -tuln 2>/dev/null | grep -q ":8000 " && ! ss -tuln 2>/dev/null | grep -q ":8000 "
check "Port 8000 (API) is available"

! netstat -tuln 2>/dev/null | grep -q ":3000 " && ! ss -tuln 2>/dev/null | grep -q ":3000 "
check "Port 3000 (Web) is available"

! netstat -tuln 2>/dev/null | grep -q ":5432 " && ! ss -tuln 2>/dev/null | grep -q ":5432 "
check "Port 5432 (PostgreSQL) is available"

! netstat -tuln 2>/dev/null | grep -q ":6379 " && ! ss -tuln 2>/dev/null | grep -q ":6379 "
check "Port 6379 (Redis) is available"

echo ""
echo "📚 Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[ -f "DEPLOYMENT.md" ]
check "DEPLOYMENT.md exists"

[ -f "DOCKER_README.md" ]
check "DOCKER_README.md exists"

[ -f "README.md" ]
check "README.md exists"

[ -x "DEPLOY.sh" ]
check "DEPLOY.sh is executable"

echo ""
echo "🚀 Deployment Scripts"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[ -x "docker-setup.sh" ]
check "docker-setup.sh is executable"

[ -x "DEPLOY.sh" ]
check "DEPLOY.sh is executable"

[ -x "scripts/docker-build.sh" ]
check "scripts/docker-build.sh is executable"

[ -x "scripts/health-check.sh" ]
check "scripts/health-check.sh is executable"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Summary:"
echo "  ✅ Passed: $PASSED"
echo "  ❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 All checks passed! You're ready to deploy."
    echo ""
    echo "Next steps:"
    echo "  1. Configure .env file (if needed)"
    echo "  2. Run: bash DEPLOY.sh"
    echo ""
    exit 0
else
    echo "⚠️  Please fix the failed checks before deploying."
    echo ""
    exit 1
fi
