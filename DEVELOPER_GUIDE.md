# TechTots LMS - Developer Guide

## Quick Reference

### Environment Variables

Create `.env` files in both directories:

**Backend (.env)**
```
FLASK_ENV=development
FLASK_DEBUG=1
MONGODB_URI=mongodb://localhost:27017/techtots_lms
JWT_SECRET_KEY=your-secret-key-here
JWT_EXPIRATION=3600
CORS_ORIGINS=http://localhost:3000
PORT=5000
```

**Frontend (.env.local)**
```
NEXT_PUBLIC_API_URL=http://localhost:5000/api
NEXT_PUBLIC_APP_NAME=TechTots LMS
```

### Running the Project

**Terminal 1: MongoDB**
```bash
cd /vercel/share/v0-project
docker-compose up -d
```

**Terminal 2: Backend**
```bash
cd backend
python run.py
```

**Terminal 3: Frontend**
```bash
pnpm dev
```

Then open http://localhost:3000

### Project Structure

```
TechTots LMS/
├── backend/
│   ├── app/models/         # Data models (user, course, etc)
│   ├── app/services/       # Business logic
│   ├── app/routes/         # API endpoints
│   ├── app/utils/          # Utilities (auth, db, errors)
│   ├── config/             # Configuration
│   └── run.py              # Entry point
├── app/
│   ├── auth/               # Auth pages (login, register)
│   ├── dashboard/          # Main dashboard
│   ├── learn/              # Course discovery
│   └── layout.tsx          # Root layout
├── components/             # React components
├── contexts/               # React contexts
├── lib/                    # Utilities (API client)
└── types/                  # TypeScript types
```

## Development Workflow

### Adding a New API Endpoint

**Step 1: Create the Model** (`backend/app/models/`)
```python
class MyModel:
    def __init__(self, name, ...):
        self._id = ObjectId()
        self.name = name
        # ... other fields
    
    def to_dict(self, include_id=True):
        data = {...}
        if include_id:
            data['id'] = str(self._id)
        return data
```

**Step 2: Create the Service** (`backend/app/services/`)
```python
class MyService:
    def __init__(self, db):
        self.db = db
        self.collection = db.my_collection
    
    def create_item(self, **kwargs):
        # Validate input
        # Create model instance
        # Insert into DB
        # Return result
        pass
```

**Step 3: Create the Routes** (`backend/app/routes/`)
```python
@bp.route('', methods=['POST'])
@require_auth
def create_item():
    try:
        data = request.get_json()
        service = MyService(current_app.db)
        item = service.create_item(**data)
        return success_response({'item': item.to_dict()}, 'Created', 201), 201
    except Exception as e:
        return error_response(str(e), 500)
```

**Step 4: Register the Blueprint** (`backend/app/routes/__init__.py`)
```python
from . import my_model
app.register_blueprint(my_model.bp)
```

### Adding a New Frontend Component

**Step 1: Create the Component** (`components/...`)
```typescript
'use client'

import { useState, useEffect } from 'react'

export function MyComponent({ prop1, prop2 }) {
  const [state, setState] = useState(null)
  
  useEffect(() => {
    // Load data
  }, [])
  
  return (
    <div>
      {/* JSX */}
    </div>
  )
}
```

**Step 2: Use in Page**
```typescript
import { MyComponent } from '@/components/my-component'

export default function Page() {
  return (
    <main>
      <MyComponent prop1="value" />
    </main>
  )
}
```

## API Usage Examples

### Fetch with Auth

```typescript
const response = await fetch('/api/endpoint', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({ data })
})

const data = await response.json()
```

### Using API Client

```typescript
import { apiClient } from '@/lib/api-client'

// GET
const result = await apiClient.get('/endpoint')

// POST
const result = await apiClient.post('/endpoint', { data })

// PUT
const result = await apiClient.put('/endpoint/id', { data })

// DELETE
const result = await apiClient.delete('/endpoint/id')
```

## Common Tasks

### Modify User Roles

Update `backend/app/models/user.py`:
```python
class UserRole(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    # Add new role here
```

### Add New Course Field

**Backend:**
1. Update model in `app/models/course.py`
2. Update service in `app/services/course_service.py`
3. Add validation in routes

**Frontend:**
1. Update type in `types/index.ts`
2. Update form component
3. Update API calls

### Create New Page

```bash
# Create directory
mkdir -p app/[section]

# Create page.tsx
# Add necessary components
# Update layout if needed
```

## Database Operations

### Query Examples

**Find one:**
```python
user = collection.find_one({'email': 'user@example.com'})
```

**Find many:**
```python
users = list(collection.find({'role': 'student'}).limit(10))
```

**Insert:**
```python
result = collection.insert_one(document)
_id = result.inserted_id
```

**Update:**
```python
result = collection.update_one(
    {'_id': ObjectId(id)},
    {'$set': {'field': 'new_value'}}
)
```

**Delete:**
```python
collection.delete_one({'_id': ObjectId(id)})
```

## Error Handling

### Backend

```python
from app.utils.errors import NotFoundError, ValidationError

try:
    # Your code
    pass
except ValidationError as e:
    return error_response(str(e), 400)
except NotFoundError as e:
    return error_response(str(e), 404)
except Exception as e:
    return error_response(str(e), 500)
```

### Frontend

```typescript
try {
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  const data = await response.json()
} catch (error) {
  console.error('Error:', error)
  // Handle error
}
```

## Testing

### Backend Testing

```bash
cd backend
pytest tests/

# Run specific test
pytest tests/test_courses.py::test_create_course

# With coverage
pytest --cov=app tests/
```

### Frontend Testing

```bash
# Unit tests
pnpm test

# End-to-end tests
pnpm cypress:run
```

## Debugging

### Backend

Use print statements or logging:
```python
import logging
logger = logging.getLogger(__name__)
logger.debug('Debug message')
logger.info('Info message')
logger.error('Error message')
```

### Frontend

Use browser DevTools:
```typescript
console.log('[v0] Debug:', data)
console.error('[v0] Error:', error)
console.trace('[v0] Stack trace')
```

## Performance Tips

### Backend
- Add database indexes for frequently queried fields
- Use pagination for large result sets
- Cache frequently accessed data
- Use async/await properly
- Minimize database calls

### Frontend
- Use React.memo for expensive components
- Implement code splitting
- Use dynamic imports for lazy loading
- Optimize images with next/image
- Minimize bundle size

## Security Considerations

### Always Do
- Validate user input
- Check authentication on protected routes
- Sanitize database inputs
- Use HTTPS in production
- Store secrets in .env files
- Never commit sensitive data

### Never Do
- Hardcode API keys
- Log sensitive information
- Store passwords in plain text
- Trust client-side validation
- Disable CORS security
- Expose error details to users

## Deployment Checklist

Before deploying:
- [ ] Environment variables configured
- [ ] Database backups enabled
- [ ] Error logging set up
- [ ] Rate limiting enabled
- [ ] HTTPS configured
- [ ] CORS properly configured
- [ ] Load testing passed
- [ ] Security audit completed
- [ ] Documentation updated
- [ ] Tests passing

## Resources

### Backend
- Flask: https://flask.palletsprojects.com/
- MongoDB: https://docs.mongodb.com/
- PyJWT: https://pyjwt.readthedocs.io/

### Frontend
- Next.js: https://nextjs.org/docs
- React: https://react.dev
- TypeScript: https://www.typescriptlang.org/
- Tailwind CSS: https://tailwindcss.com/
- Shadcn/ui: https://ui.shadcn.com/

## Troubleshooting

### MongoDB Connection Error
```
Error: connect ECONNREFUSED 127.0.0.1:27017
```
**Solution**: Start MongoDB with `docker-compose up -d`

### CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```
**Solution**: Check CORS_ORIGINS in .env backend file

### Auth Token Invalid
```
401 Unauthorized
```
**Solution**: Check token expiration, refresh token needed

### Port Already in Use
```
Port 3000/5000 already in use
```
**Solution**: Kill process or use different port

### Missing Environment Variables
```
KeyError: 'MONGODB_URI'
```
**Solution**: Create .env file with all required variables

## Getting Help

1. Check the documentation files
2. Review similar code in the project
3. Check error messages carefully
4. Use debugging techniques
5. Search online for similar issues

---

**Happy coding! 🚀**
