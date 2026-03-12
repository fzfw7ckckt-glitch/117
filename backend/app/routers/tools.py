from fastapi import APIRouter, HTTPException
from app.data.tools_catalog import TOOLS_CATALOG, ALL_TOOLS_LIST, TOTAL_TOOLS
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def list_all_tools():
    """Отримати всі інструменти (57 total)"""
    return {
        "total_tools": TOTAL_TOOLS,
        "total_categories": len(TOOLS_CATALOG),
        "categories": {
            key: {
                "name": data["name"],
                "count": data["count"],
                "tools": [{"id": t["id"], "name": t["name"], "description": t["description"]} for t in data["tools"]]
            }
            for key, data in TOOLS_CATALOG.items()
        }
    }

@router.get("/category/{category_name}")
async def get_category(category_name: str):
    """Отримати інструменти за категорією"""
    category_upper = category_name.upper()
    if category_upper not in TOOLS_CATALOG:
        raise HTTPException(status_code=404, detail=f"Категорія '{category_name}' не знайдена")
    
    category = TOOLS_CATALOG[category_upper]
    return {
        "category": category_upper,
        "name": category["name"],
        "count": category["count"],
        "tools": category["tools"]
    }

@router.get("/search/{tool_name}")
async def search_tool(tool_name: str):
    """Пошук інструменту за назвою"""
    tool_lower = tool_name.lower()
    for tool in ALL_TOOLS_LIST:
        if tool_lower in tool["id"].lower() or tool_lower in tool["name"].lower():
            return tool
    raise HTTPException(status_code=404, detail=f"Інструмент '{tool_name}' не знайдений")

@router.get("/stats")
async def get_statistics():
    """Статистика інструментів за категоріями"""
    stats = {
        "total_tools": TOTAL_TOOLS,
        "total_categories": len(TOOLS_CATALOG),
        "by_category": {}
    }
    
    for cat_key, cat_data in TOOLS_CATALOG.items():
        has_api = sum(1 for t in cat_data["tools"] if t["api"] == "✓")
        stats["by_category"][cat_data["name"]] = {
            "count": cat_data["count"],
            "with_api": has_api,
            "without_api": cat_data["count"] - has_api
        }
    
    return stats

@router.get("/{tool_id}")
async def get_tool_detail(tool_id: str):
    """Отримати детальну інформацію про інструмент"""
    for tool in ALL_TOOLS_LIST:
        if tool["id"] == tool_id:
            return tool
    raise HTTPException(status_code=404, detail=f"Інструмент з ID '{tool_id}' не знайдений")

@router.post("/{tool_id}/run")
async def run_tool(tool_id: str, query: str = ""):
    """Запустити інструмент (queued for async processing)"""
    tool = None
    for t in ALL_TOOLS_LIST:
        if t["id"] == tool_id:
            tool = t
            break
    
    if not tool:
        raise HTTPException(status_code=404, detail=f"Інструмент не знайдений")
    
    # TODO: Integrate with Celery for async processing
    task_id = f"task_{tool_id}_{hash(query) % 100000}"
    logger.info(f"Запущено {tool['name']} з запитом: {query}")
    
    return {
        "task_id": task_id,
        "tool_id": tool_id,
        "tool_name": tool["name"],
        "status": "queued",
        "query": query
    }

@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """Отримати статус виконання задачі"""
    # TODO: Fetch from Celery result backend
    return {
        "task_id": task_id,
        "status": "completed",
        "result": {"data": "mock result"}
    }
