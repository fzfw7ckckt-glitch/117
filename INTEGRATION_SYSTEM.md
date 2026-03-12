# 🔗 OSINT Platform 2026 - Webhooks, Chunking, Relations & Pathways

## 📌 СИСТЕМА ІНТЕГРАЦІЇ

Чотири ключові компоненти для зєднання всіх частин платформи:

### 1. **🪝 WEBHOOKS** (Вебхуки)
### 2. **📦 CHUNKING** (Розбиття на чанки)
### 3. **🔀 RELATIONS** (Зв'язки даних)
### 4. **🛣️ PATHWAYS** (Шляхи зєднань)

---

## 🪝 1. WEBHOOK SYSTEM

### Що таке webhook?
Веб-гачок - це автоматичне повідомлення коли сталася подія в розслідуванні.

### 5 Типів подій:

| Подія | Код | Опис |
|------|------|------|
| **INVESTIGATION_CREATED** | `investigation.created` | Розслідування створено |
| **INVESTIGATION_COMPLETED** | `investigation.completed` | Розслідування завершено |
| **EVIDENCE_FOUND** | `evidence.found` | Знайдено доказ |
| **THREAT_DETECTED** | `threat.detected` | Виявлена загроза |
| **REPORT_GENERATED** | `report.generated` | Звіт створено |
| **TOOL_EXECUTED** | `tool.executed` | Інструмент виконано |
| **ANALYSIS_COMPLETED** | `analysis.completed` | Аналіз завершено |

### API Endpoints:

```bash
# Зареєструвати вебхук
POST /integration/{investigation_id}/webhooks/register
{
  "url": "https://example.com/webhook",
  "events": ["evidence.found", "threat.detected"]
}

# Отримати вебхуки
GET /integration/{investigation_id}/webhooks

# Деактивувати вебхук
DELETE /integration/{investigation_id}/webhooks/{webhook_id}
```

### Приклад:
```bash
curl -X POST http://localhost:8000/integration/inv_001/webhooks/register \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://myservice.com/osint-webhook",
    "events": ["evidence.found", "analysis.completed"]
  }'
```

---

## 📦 2. CHUNKING SYSTEM

### Що таке чанк?
Чанк - це окремий шматок даних (одна знахідка від одного інструменту).

### 7 Типів чанків:

| Тип | Код | Приклад |
|-----|------|---------|
| **PROFILE_CHUNK** | `profile` | Профіль користувача на сайті |
| **INFRASTRUCTURE_CHUNK** | `infrastructure` | IP адреса сервера |
| **LOCATION_CHUNK** | `location` | Геолокаційні координати |
| **FINANCIAL_CHUNK** | `financial` | Інформація про компанію |
| **THREAT_CHUNK** | `threat` | Виявлена загроза |
| **EVIDENCE_CHUNK** | `evidence` | Загальний доказ |
| **RELATIONSHIP_CHUNK** | `relationship` | Зв'язок між сутностями |

### API Endpoints:

```bash
# Створити чанк
POST /integration/{investigation_id}/chunks
{
  "chunk_type": "profile",
  "data": {"username": "john_doe", "platform": "twitter"},
  "source_tool": "maigret"
}

# Отримати всі чанки
GET /integration/{investigation_id}/chunks

# Отримати чанки за типом
GET /integration/{investigation_id}/chunks?chunk_type=profile

# Отримати дерево чанків (ієрархія)
GET /integration/{investigation_id}/chunks/{chunk_id}/tree

# Об'єднати кілька чанків
POST /integration/{investigation_id}/chunks/merge
{
  "chunk_ids": ["chunk_1", "chunk_2", "chunk_3"]
}
```

### Структура чанку:
```json
{
  "id": "abc123def456",
  "type": "profile",
  "data": { "username": "john_doe", "platform": "twitter" },
  "source_tool": "maigret",
  "investigation_id": "inv_001",
  "created_at": "2026-03-10T21:45:00Z",
  "hash_sha256": "abc123...",
  "size_bytes": 1024,
  "parent_chunk_id": null
}
```

---

## 🔀 3. RELATION SYSTEM (Зв'язки)

### Що таке relation?
Зв'язок - це лінія між двома чанками даних (наприклад: "користувач OWNS компанія").

### 10 Типів зв'язків:

| Тип | Код | Приклад |
|-----|------|---------|
| **OWNS** | `owns` | Користувач OWNS компанія |
| **WORKS_FOR** | `works_for` | Працівник WORKS_FOR компанія |
| **LOCATED_IN** | `located_in` | Офіс LOCATED_IN країна |
| **REGISTERED_ON** | `registered_on` | Акаунт REGISTERED_ON платформа |
| **CONNECTED_TO** | `connected_to` | Гаджет CONNECTED_TO мережа |
| **MENTIONS** | `mentions` | Пост MENTIONS користувача |
| **FOLLOWS** | `follows` | Користувач FOLLOWS іншого |
| **FRIENDS_WITH** | `friends_with` | Користувач FRIENDS_WITH іншого |
| **SAME_AS** | `same_as` | Акаунт SAME_AS акаунт (одна особа) |
| **RELATED_TO** | `related_to` | Загальний зв'язок |

### API Endpoints:

```bash
# Створити зв'язок
POST /integration/{investigation_id}/relations
{
  "source_chunk_id": "chunk_1",
  "target_chunk_id": "chunk_2",
  "relation_type": "works_for",
  "weight": 0.9
}

# Знайти шлях між двома чанками
GET /integration/{investigation_id}/relations/path?start_chunk_id=chunk_1&end_chunk_id=chunk_3

# Отримати мережу сутностей (граф)
GET /integration/{investigation_id}/relations/network?entity_chunk_id=chunk_1&depth=2

# Отримати пов'язані компоненти
GET /integration/{investigation_id}/relations/components
```

### Приклад знаходження шляху:
```bash
# Запит
curl "http://localhost:8000/integration/inv_001/relations/path?start_chunk_id=user_123&end_chunk_id=company_456"

# Відповідь
{
  "start": "user_123",
  "end": "company_456",
  "path": ["user_123", "email_chunk", "company_chunk", "company_456"],
  "hops": 3
}
```

### Граф мережи сутностей:
```bash
curl "http://localhost:8000/integration/inv_001/relations/network?entity_chunk_id=user_123&depth=2"

# Відповідь - вся мережа на 2 рівні глибини
{
  "root": "user_123",
  "depth": 2,
  "nodes": {
    "user_123": {"type": "entity"},
    "email_chunk": {"type": "connected"},
    "company_456": {"type": "connected"}
  },
  "edges": [
    {
      "source": "user_123",
      "target": "email_chunk",
      "type": "registered_on",
      "weight": 0.95
    }
  ]
}
```

---

## 🛣️ 4. PATHWAY SYSTEM (Шляхи зєднань)

### Що таке pathway?
Шлях - це маршрут через кілька чанків та зв'язків, що розповідає історію розслідування.

### 5 Типів шляхів:

| Тип | Код | Опис |
|-----|------|------|
| **INVESTIGATION_FLOW** | `investigation_flow` | Потік розслідування |
| **DATA_FLOW** | `data_flow` | Потік даних |
| **EVIDENCE_CHAIN** | `evidence_chain` | Ланцюг доказів |
| **THREAT_PATH** | `threat_path` | Шлях загрози |
| **ENTITY_CONNECTION** | `entity_connection` | Зв'язок сутностей |

### API Endpoints:

```bash
# Створити шлях
POST /integration/{investigation_id}/pathways
{
  "pathway_type": "evidence_chain",
  "start_node": "chunk_1",
  "end_node": "chunk_5",
  "description": "Ланцюг доказів від користувача до компанії"
}

# Отримати всі шляхи
GET /integration/{investigation_id}/pathways

# Отримати найсильніші шляхи
GET /integration/{investigation_id}/pathways/strongest?limit=5

# Візуалізація шляху
GET /integration/{investigation_id}/pathways/{pathway_id}/visualize
```

### Приклад шляху:
```bash
curl -X POST http://localhost:8000/integration/inv_001/pathways \
  -H "Content-Type: application/json" \
  -d '{
    "pathway_type": "evidence_chain",
    "start_node": "maigret_profile",
    "end_node": "company_sanction",
    "description": "Від профілю користувача до санкційної компанії"
  }'

# Відповідь
{
  "pathway_id": "pw_abc123",
  "type": "evidence_chain",
  "nodes_count": 4,
  "strength": 0.87,
  "description": "..."
}
```

### Візуалізація:
```bash
curl http://localhost:8000/integration/inv_001/pathways/pw_abc123/visualize

# Відповідь
{
  "id": "pw_abc123",
  "type": "evidence_chain",
  "strength": 0.87,
  "nodes": ["chunk_1", "chunk_2", "chunk_3", "chunk_4"],
  "connections": [
    {
      "source": "chunk_1",
      "target": "chunk_2",
      "type": "registered_on",
      "weight": 0.9
    }
  ]
}
```

---

## 🗺️ 5. INVESTIGATION MAP

### Повна карта розслідування

```bash
GET /integration/{investigation_id}/map

# Відповідь
{
  "investigation_id": "inv_001",
  "map": {
    "chunks": {
      "total": 45,
      "by_type": {
        "profile": 12,
        "infrastructure": 8,
        "location": 5,
        "financial": 10,
        "threat": 3,
        "evidence": 7
      }
    },
    "relations": {
      "total": 78
    },
    "pathways": {
      "total": 5,
      "by_type": {
        "evidence_chain": 3,
        "entity_connection": 2
      }
    }
  }
}
```

---

## 🎯 ТИПОВИЙ РОБОЧИЙ ПОТІК

### 1️⃣ Запустити інструмент
```
Maigret знайде профіли → Результат обробляється
```

### 2️⃣ Створити чанки
```
Кожен профіль → Чанк даних з хешем
```

### 3️⃣ Розпізнати зв'язки
```
Користувач X має email Y → Створити RELATION "registered_on"
```

### 4️⃣ Побудувати шляхи
```
start_node (профіль) → [email, компанія, санкція] → end_node
```

### 5️⃣ Генерувати звіт
```
Шляхи + Чанки + Відносини = Звіт з доказами
```

---

## 📊 ПРИКЛАД: РОЗПІЗНАВАННЯ ОСОБИ

### Крок 1: Інструменти знаходять
```
Maigret → 5 профілів
PhoneInfoga → Номер телефону
Geospy → Координати
```

### Крок 2: Чанки створюються
```
chunk_1: {platform: "twitter", username: "john_doe"}
chunk_2: {phone: "+38012345678"}
chunk_3: {latitude: 50.4501, longitude: 30.5234}
```

### Крок 3: Зв'язки встановлюються
```
chunk_1 REGISTERED_ON twitter
chunk_2 CONNECTED_TO john_doe
chunk_3 LOCATED_IN Ukraine
```

### Крок 4: Шляхи будуються
```
twitter_profile → phone_number → location → threat_assessment
```

### Крок 5: Звіт генерується
```
"Користувач john_doe зареєстрований на Twitter з телефоном 
+38012345678 та розташований у Києві (50.4501, 30.5234)"
```

---

## 🔐 БЕЗПЕКА

✅ SHA-256 хеші для кожного чанку
✅ Верифікація цілісності
✅ Часові мітки
✅ Метадані джерела
✅ Вага впевненості для кожного зв'язку

---

## 📈 РОЗШИРЕННЯ

### Додавання нового типу чанку:
```python
class ChunkType(str, Enum):
    MY_NEW_TYPE = "my_new_type"
```

### Додавання нового типу зв'язку:
```python
class RelationType(str, Enum):
    MY_RELATION = "my_relation"
```

### Додавання нового типу шляху:
```python
class PathwayType(str, Enum):
    MY_PATHWAY = "my_pathway"
```

---

**Всі компоненти повністю інтегровані та готові до використання!** 🚀
