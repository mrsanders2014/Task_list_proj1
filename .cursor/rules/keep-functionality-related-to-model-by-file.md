---
# Rule: Enforce Layered Architecture Naming Conventions

## Applies To
- All Python projects in this workspace

## Rule
- All files and folders must follow the layered architecture naming convention

### Folder Names
- model/ — for all domain/entity models
- bus_rules/ — for business logic/services
- dbase/ — for data access/database logic
- routers/ — for FastAPI routers (API endpoints)

### File Names
- Each file must be named as:  
  {entity/layer_name}_{layer}.py

#### Examples:
- Model: model/task.py (not `models.py` or `TaskModel.py`)
- Service: bus_rules/Task_service.py
- Database: dbase/Tasks_db.py and dbase/User_db.py
- Router: routers/tasks_router.py

### Additional Rules
- Only one entity per file (e.g., `task.py` for the task model, not `song_and_album.py`)
- Plural folder names are not allowed (use `model/`, not `models/`)
- No camelCase or PascalCase in file names; use snake_case only
- No generic names like `utils.py` or `helpers.py` in these core folders

## Rationale
- Ensures consistency and clarity across all projects
- Makes it easy to locate files by entity and layer
- Supports scalable, maintainable, and testable codebases

## Enforcement
- All new files and folders must follow this convention.
- Code reviews should reject PRs that do not comply.
- Refactor legacy code to match this structure when touched.

alwaysApply: true
---