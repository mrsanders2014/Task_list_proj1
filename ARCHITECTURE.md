# Task Manager CLI - Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                      │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              CLI Interface (cli.py)                     │  │
│  │  • Rich Terminal UI                                     │  │
│  │  • Interactive Menus                                    │  │
│  │  • Input Validation                                     │  │
│  │  • Formatted Output                                     │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  BUSINESS LOGIC LAYER                         │
│                                                               │
│  ┌──────────────────────┐    ┌──────────────────────┐       │
│  │  User Management     │    │  Task Management     │       │
│  │  • Authentication    │    │  • CRUD Operations   │       │
│  │  • Profile Updates   │    │  • Filtering         │       │
│  │  • Status Control    │    │  • Dependencies      │       │
│  └──────────────────────┘    └──────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER                          │
│                                                               │
│  ┌──────────────────────┐    ┌──────────────────────┐       │
│  │  UserRepository      │    │  TaskRepository      │       │
│  │  • create()          │    │  • create()          │       │
│  │  • get_by_id()       │    │  • get_by_user()     │       │
│  │  • update()          │    │  • update()          │       │
│  │  • delete()          │    │  • delete()          │       │
│  │  • authenticate()    │    │  • get_overdue()     │       │
│  └──────────────────────┘    └──────────────────────┘       │
│                              │                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          DatabaseConnection (Singleton)               │   │
│  │          • Connection Management                      │   │
│  │          • Index Creation                             │   │
│  │          • Error Handling                             │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      MODEL LAYER                              │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  User Model  │  │  Task Model  │  │ Label Model  │      │
│  │  • Fields    │  │  • Fields    │  │  • Fields    │      │
│  │  • Validate  │  │  • Validate  │  │  • Validate  │      │
│  │  • to_dict() │  │  • to_dict() │  │  • to_dict() │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                             │
│                                                               │
│                        MongoDB                                │
│                                                               │
│  ┌──────────────────┐           ┌──────────────────┐        │
│  │  Users           │           │  Tasks           │        │
│  │  Collection      │ ◄───────► │  Collection      │        │
│  │                  │  1:many   │                  │        │
│  └──────────────────┘           └──────────────────┘        │
│                                         │                     │
│                                         │ self-reference      │
│                                         ▼                     │
│                                  (dependencies)               │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### User Registration Flow
```
User Input → CLI → User Model (validate) → UserRepository
→ MongoDB (Users Collection) → Success/Error → CLI → User
```

### Task Creation Flow
```
User Input → CLI → Task Model (validate) → Label Models
→ TaskRepository → MongoDB (Tasks Collection)
→ Success/Error → CLI → User
```

### Task Query Flow
```
User Filter Request → CLI → TaskRepository (with filters)
→ MongoDB Query → Task Models → Format → Display Table → User
```

## Component Relationships

### 1. CLI Layer (Presentation)
- **Responsibilities:**
  - User interaction
  - Input collection and validation
  - Output formatting
  - Menu navigation
  - Error display

- **Dependencies:**
  - Rich library for UI
  - UserRepository for user operations
  - TaskRepository for task operations

### 2. Repository Layer (Data Access)
- **Responsibilities:**
  - Database operations
  - Query construction
  - Result transformation
  - Error handling

- **Components:**
  - `UserRepository`: User-specific operations
  - `TaskRepository`: Task-specific operations
  - `DatabaseConnection`: Connection management

### 3. Model Layer (Domain)
- **Responsibilities:**
  - Data structure definition
  - Validation rules
  - Type safety
  - Serialization/Deserialization

- **Components:**
  - `User`: User entity
  - `Task`: Task entity
  - `Label`: Label entity

### 4. Database Layer (Storage)
- **Responsibilities:**
  - Data persistence
  - Query optimization
  - Index management
  - Data integrity

- **Collections:**
  - `Users`: User documents
  - `Tasks`: Task documents

## Design Patterns

### 1. Singleton Pattern
**Used in:** `DatabaseConnection`

**Purpose:** Ensure only one database connection instance exists

```python
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 2. Repository Pattern
**Used in:** `UserRepository`, `TaskRepository`

**Purpose:** Separate data access logic from business logic

```python
class UserRepository:
    def create(self, user: User) -> str
    def get_by_id(self, id: str) -> User
    def update(self, id: str, data: dict) -> bool
    def delete(self, id: str) -> bool
```

### 3. Factory Pattern
**Used in:** Model classes (`from_dict()` methods)

**Purpose:** Create objects from dictionaries

```python
@classmethod
def from_dict(cls, data: Dict) -> User:
    return cls(
        firstname=data.get('firstname'),
        ...
    )
```

### 4. Active Record Pattern (Simplified)
**Used in:** Model classes

**Purpose:** Combine data and behavior in model objects

```python
class User:
    def to_dict(self) -> Dict
    def _validate(self) -> None
```

## Key Features

### 1. Connection Management
```
┌────────────────────────────────────────────┐
│  Application Start                         │
│  └─► DatabaseConnection (Singleton)        │
│      └─► Load .env variables               │
│          └─► Connect to MongoDB            │
│              └─► Test connection (ping)    │
│                  └─► Create indexes        │
└────────────────────────────────────────────┘
```

### 2. User Authentication Flow
```
┌────────────────────────────────────────────┐
│  User enters credentials                   │
│  └─► UserRepository.authenticate()         │
│      └─► Find user by userid               │
│          └─► Check password                │
│              └─► Update last_login         │
│                  └─► Return User or None   │
└────────────────────────────────────────────┘
```

### 3. Task Filtering
```
┌────────────────────────────────────────────┐
│  User selects filter (status/priority/etc)│
│  └─► CLI collects filter parameters        │
│      └─► TaskRepository builds query       │
│          └─► MongoDB executes query        │
│              └─► Results formatted         │
│                  └─► Display in table      │
└────────────────────────────────────────────┘
```

## Database Schema

### Users Collection
```json
{
  "_id": ObjectId,           // Auto-generated
  "firstname": String,       // Required
  "lastname": String,        // Required
  "userid": String,          // Required, Unique, Indexed
  "email": String,           // Required, Unique, Indexed
  "password": String,        // Required (min 6 chars)
  "status": String,          // "active" | "inactive"
  "last_login": DateTime     // Auto-updated
}
```

### Tasks Collection
```json
{
  "_id": ObjectId,                    // Auto-generated
  "user_id": String,                  // Required, Indexed
  "title": String,                    // Required
  "description": String,              // Optional
  "priority": Integer,                // Optional (1-10), Indexed
  "due_date": DateTime,               // Optional, Indexed
  "labels": [                         // Optional, Array
    {
      "name": String,
      "color": String                 // Hex color
    }
  ],
  "time_unit": String,                // "minutes"|"hours"|"days"|"weeks"
  "estimated_time": Float,            // Optional
  "status": String,                   // Indexed
  "notification_time_unit": String,   // Time unit for notifications
  "notification_when": Float,         // Optional
  "dependencies": [String],           // Array of task IDs
  "created_at": DateTime,             // Auto-set
  "updated_at": DateTime              // Auto-updated
}
```

### Indexes
```javascript
// Users collection
db.Users.createIndex({ "userid": 1 }, { unique: true })
db.Users.createIndex({ "email": 1 }, { unique: true })

// Tasks collection
db.Tasks.createIndex({ "user_id": 1 })
db.Tasks.createIndex({ "status": 1 })
db.Tasks.createIndex({ "priority": 1 })
db.Tasks.createIndex({ "due_date": 1 })
```

## Error Handling Strategy

### 1. Database Errors
```
MongoDB Error → DatabaseConnection catches
→ Log error → User-friendly message → CLI display
```

### 2. Validation Errors
```
Invalid Input → Model validation → ValueError raised
→ Repository catches → CLI displays error → Retry
```

### 3. Authentication Errors
```
Wrong credentials → authenticate() returns None
→ CLI displays error message → Return to login menu
```

## Security Considerations

### Current Implementation
- ✓ Environment-based configuration
- ✓ Password masking in CLI
- ✓ Input validation
- ✓ MongoDB injection prevention

### Recommended Enhancements
- ⚠ Hash passwords (bcrypt)
- ⚠ Add JWT authentication
- ⚠ Implement rate limiting
- ⚠ Enable MongoDB authentication
- ⚠ Use TLS/SSL connections

## Performance Optimizations

### Implemented
- ✓ Database indexes on frequently queried fields
- ✓ Connection pooling (PyMongo default)
- ✓ Singleton pattern for connection
- ✓ Efficient MongoDB queries

### Potential Improvements
- Consider adding Redis for caching
- Implement pagination for large datasets
- Use aggregation pipeline for complex queries
- Add query result limits
- Lazy load task dependencies

## Scalability Considerations

### Current Capacity
- Suitable for: Single user to hundreds of users
- Task volume: Thousands of tasks per user
- Response time: < 100ms for most operations

### To Scale Further
1. **Horizontal Scaling**
   - MongoDB replica sets
   - Load balancing
   - Sharding by user_id

2. **Caching Layer**
   - Redis for frequent queries
   - Cache task lists by user
   - Cache user sessions

3. **Async Operations**
   - Use Motor (async MongoDB driver)
   - Async I/O for CLI
   - Background task processing

4. **API Layer**
   - REST API with FastAPI
   - GraphQL for flexible queries
   - WebSocket for real-time updates

## Testing Strategy

### Unit Tests
- Model validation
- Repository operations (mocked DB)
- Business logic

### Integration Tests
- Database operations
- End-to-end flows
- Error scenarios

### Manual Testing
- CLI user experience
- Edge cases
- Performance under load

## Deployment Architecture

### Development
```
Developer Machine
├── Python 3.12+
├── Local MongoDB
├── .env (local config)
└── CLI Application
```

### Production (Recommended)
```
Application Server
├── Python 3.12+ (containerized)
├── MongoDB Atlas (cloud)
├── .env (production config)
├── Monitoring (logs)
└── Backup strategy
```

## Monitoring and Logging

### Current Implementation
- Console output for errors
- Connection status messages
- Operation success/failure feedback

### Recommended Additions
- Structured logging (JSON format)
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Log aggregation (ELK stack)
- Performance metrics
- User activity tracking
- Error tracking (Sentry)

## Future Architecture Evolution

### Phase 1: API Layer (Current → RESTful API)
```
CLI ────┐
        ├──► REST API (FastAPI) ──► MongoDB
Web App ┘
```

### Phase 2: Microservices
```
Frontend ──► API Gateway
              ├──► User Service ──► Users DB
              ├──► Task Service ──► Tasks DB
              └──► Notification Service ──► Queue
```

### Phase 3: Event-Driven
```
Services ──► Message Queue (RabbitMQ/Kafka)
              ├──► Task Created Event
              ├──► Task Updated Event
              └──► Notification Events
```

## Conclusion

This architecture provides:
- ✓ Clear separation of concerns
- ✓ Maintainable code structure
- ✓ Extensible design
- ✓ Testable components
- ✓ Scalable foundation
- ✓ Production-ready patterns

The system is built to evolve from a CLI application to a full-featured web application with minimal refactoring of core components.

