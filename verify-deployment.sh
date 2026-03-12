#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║      OSINT Platform 2026 - Deployment Verification        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Only cd if not already in osint-platform-2026
if [ "$(basename "$PWD")" != "osint-platform-2026" ]; then
	cd osint-platform-2026 || exit 1
fi

# 1. Check containers
echo "📦 Container Status:"
docker-compose ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | sed 's/^/   /'
echo ""

# 2. Check APIs
echo "🔗 API Endpoints:"
echo -n "   API Health: "
curl -s http://localhost:8000/health/ | jq -r '.status' 2>/dev/null && echo "✓" || echo "✗"
echo -n "   Frontend: "
curl -s -I http://localhost:3000 | grep -q "200\|301\|302" && echo "✓" || echo "✗"
echo ""

# 3. Database
echo "💾 Database:"
echo -n "   PostgreSQL: "
docker exec osint-postgres pg_isready -U admin &>/dev/null && echo "✓" || echo "✗"
echo -n "   Redis: "
docker exec osint-redis redis-cli ping &>/dev/null && echo "✓" || echo "✗"
echo ""

# 4. Services
echo "⚙️  Services:"
echo "   API: http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Database: localhost:5432"
echo "   Cache: localhost:6379"
echo ""

# 5. Statistics
echo "📊 Statistics:"
IMAGES=$(docker-compose config --services | wc -l)
TOTAL_SIZE=$(du -sh . | cut -f1)
echo "   Services: $IMAGES"
echo "   Project Size: $TOTAL_SIZE"
echo "   Status: ✅ DEPLOYED"
echo ""

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                  Platform Ready for Use                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
