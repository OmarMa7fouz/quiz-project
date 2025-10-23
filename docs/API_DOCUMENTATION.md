# Quiz System API Documentation

## Overview
This API provides endpoints for accessing quiz subjects, questions, and submitting quiz answers.

**Base URL:** `http://127.0.0.1:8000/api/`

---

## Endpoints

### 1. Get All Subjects
**GET** `/api/subjects/`

Returns all available subjects with their statistics.

**Response:**
```json
{
    "success": true,
    "count": 4,
    "subjects": [
        {
            "id": 1,
            "code": "CSW351-AI",
            "name": "Artificial Intelligence",
            "description": "AI concepts, machine learning, neural networks...",
            "total_questions": 90,
            "levels_available": [
                {
                    "level": "easy",
                    "count": 30,
                    "display": "Easy"
                },
                {
                    "level": "medium", 
                    "count": 30,
                    "display": "Medium"
                },
                {
                    "level": "hard",
                    "count": 30,
                    "display": "Hard"
                }
            ]
        }
    ]
}
```

### 2. Get Subject Details
**GET** `/api/subjects/{subject_code}/`

Returns detailed information about a specific subject.

**Example:** `/api/subjects/CSW351-AI/`

**Response:**
```json
{
    "success": true,
    "subject": {
        "id": 1,
        "code": "CSW351-AI",
        "name": "Artificial Intelligence",
        "description": "AI concepts, machine learning, neural networks...",
        "total_questions": 90,
        "levels_available": [...]
    }
}
```

### 3. Get Questions
**GET** `/api/questions/`

Returns questions with optional filtering.

**Query Parameters:**
- `subject_code` (optional): Filter by subject code
- `level` (optional): Filter by difficulty level (easy/medium/hard)
- `limit` (optional): Number of questions to return (default: 20)

**Examples:**
- `/api/questions/` - Get 20 random questions
- `/api/questions/?subject_code=CSW351-AI&level=easy&limit=10` - Get 10 easy AI questions

**Response:**
```json
{
    "success": true,
    "count": 10,
    "questions": [
        {
            "id": 1,
            "subject_code": "CSW351-AI",
            "subject_name": "Artificial Intelligence",
            "question_text": "What is machine learning?",
            "option_a": "A type of database",
            "option_b": "A subset of AI",
            "option_c": "A programming language",
            "option_d": "A web framework",
            "correct_answer": "B",
            "level": "easy",
            "explanation": "Machine learning is a subset of AI...",
            "created_at": "2025-01-17T10:30:00Z",
            "options": {
                "A": "A type of database",
                "B": "A subset of AI",
                "C": "A programming language",
                "D": "A web framework"
            }
        }
    ]
}
```

### 4. Generate Quiz
**POST** `/api/quiz/generate/`

Generates a random quiz with specified parameters.

**Request Body:**
```json
{
    "subject_code": "CSW351-AI",
    "level": "easy",
    "num_questions": 10
}
```

**Response:**
```json
{
    "success": true,
    "quiz": {
        "subject_code": "CSW351-AI",
        "level": "easy",
        "num_questions": 10,
        "questions": [
            {
                "id": 1,
                "subject_code": "CSW351-AI",
                "subject_name": "Artificial Intelligence",
                "question_text": "What is machine learning?",
                "option_a": "A type of database",
                "option_b": "A subset of AI",
                "option_c": "A programming language",
                "option_d": "A web framework",
                "correct_answer": "B",
                "level": "easy",
                "explanation": "Machine learning is a subset of AI...",
                "created_at": "2025-01-17T10:30:00Z",
                "options": {
                    "A": "A type of database",
                    "B": "A subset of AI",
                    "C": "A programming language",
                    "D": "A web framework"
                }
            }
        ]
    }
}
```

### 5. Submit Quiz
**POST** `/api/quiz/submit/`

Submits quiz answers and returns results.

**Request Body:**
```json
{
    "answers": [
        {
            "question_id": 1,
            "selected_answer": "B"
        },
        {
            "question_id": 2,
            "selected_answer": "A"
        }
    ]
}
```

**Response:**
```json
{
    "success": true,
    "quiz_result": {
        "total_questions": 2,
        "correct_count": 1,
        "incorrect_count": 1,
        "percentage": 50.0,
        "results": [
            {
                "question_id": 1,
                "question_text": "What is machine learning?",
                "selected_answer": "B",
                "correct_answer": "B",
                "is_correct": true,
                "explanation": "Machine learning is a subset of AI..."
            },
            {
                "question_id": 2,
                "question_text": "What is Python?",
                "selected_answer": "A",
                "correct_answer": "C",
                "is_correct": false,
                "explanation": "Python is a programming language..."
            }
        ]
    }
}
```

### 6. Get Statistics
**GET** `/api/stats/`

Returns overall quiz system statistics.

**Response:**
```json
{
    "success": true,
    "stats": {
        "total_subjects": 4,
        "total_questions": 360,
        "questions_by_level": {
            "easy": 120,
            "medium": 120,
            "hard": 120
        },
        "subjects": [
            {
                "code": "CSW351-AI",
                "name": "Artificial Intelligence",
                "total_questions": 90,
                "easy": 30,
                "medium": 30,
                "hard": 30
            }
        ]
    }
}
```

### 7. Health Check
**GET** `/api/health/`

Returns API health status.

**Response:**
```json
{
    "success": true,
    "status": "healthy",
    "timestamp": "2025-01-17T10:30:00Z",
    "version": "1.0.0"
}
```

---

## Error Responses

All endpoints return error responses in this format:

```json
{
    "success": false,
    "error": "Error message",
    "errors": {
        "field_name": ["Field-specific error message"]
    }
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Internal Server Error

---

## Usage Examples

### JavaScript/Fetch
```javascript
// Get all subjects
fetch('http://127.0.0.1:8000/api/subjects/')
    .then(response => response.json())
    .then(data => console.log(data));

// Generate a quiz
fetch('http://127.0.0.1:8000/api/quiz/generate/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        subject_code: 'CSW351-AI',
        level: 'easy',
        num_questions: 10
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Python/Requests
```python
import requests

# Get all subjects
response = requests.get('http://127.0.0.1:8000/api/subjects/')
data = response.json()
print(data)

# Generate a quiz
quiz_data = {
    'subject_code': 'CSW351-AI',
    'level': 'easy',
    'num_questions': 10
}
response = requests.post('http://127.0.0.1:8000/api/quiz/generate/', json=quiz_data)
data = response.json()
print(data)
```

### cURL
```bash
# Get all subjects
curl -X GET http://127.0.0.1:8000/api/subjects/

# Generate a quiz
curl -X POST http://127.0.0.1:8000/api/quiz/generate/ \
  -H "Content-Type: application/json" \
  -d '{"subject_code": "CSW351-AI", "level": "easy", "num_questions": 10}'
```

---

## Notes

- All endpoints return JSON responses
- No authentication required (for development)
- CORS is enabled for cross-origin requests
- Questions are returned in random order
- Quiz generation always returns different questions
- All timestamps are in ISO format
