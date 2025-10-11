<!-- b231418e-67ac-407d-a8ca-e002f22f38eb d275ee0e-4cff-43dc-935f-993db370939b -->
# Fix All Linter Errors

## 1. Fix Import Ordering in Test Files

**File: `tests/test_task_model.py`**

- Reorder imports: standard library (`datetime`) before third-party (`pytest`)
- Current lines 4-6, change to proper PEP 8 order

**File: `tests/test_user_model.py`**

- Remove protected `_id` access on line 26
- Change `assert user._id is None` to check via response method or remove if not critical

## 2. Fix Test Compatibility Issues in test_task_model.py

The tests use an old Task model signature. The current Task model uses:

- `task_mgmt: TaskMgmtDetails` object (contains priority, duedate, etc.)
- `status` values: "Created", "Started", "InProcess", etc. (not "open", "inprocess")
- No direct `priority`, `due_date`, `estimated_time`, `notification_when`, `dependencies`, `created_at`, `updated_at` attributes
- Uses `createdate` and `lastmoddate` instead

**Tests to fix:**

- `test_task_creation()` (lines 25-41): Remove invalid kwargs (priority, status="open"), use proper status
- `test_task_validation_invalid_priority()` (lines 62-69): Use TaskMgmtDetails with invalid priority
- `test_task_validation_invalid_status()` (lines 72-79): Use valid VALID_STATUSES values
- `test_task_validation_invalid_time_unit()` (lines 82-89): Use TaskMgmtDetails with invalid time_unit
- `test_task_with_dependencies()` (lines 110-122): Remove - Task model doesn't have dependencies
- `test_task_to_dict()` (lines 125-142): Fix assertions for correct field names and structure
- `test_task_from_dict()` (lines 145-167): Fix test data structure and assertions
- `test_task_str_representation()` (lines 170-182): Fix to match actual Task.**str**() format
- `test_task_optional_fields()` (lines 185-199): Rewrite to use TaskMgmtDetails properly

## 3. Summary of Changes

- Fix import order in 1 test file
- Rewrite/fix 9 test functions to match current Task model API
- Remove 1 protected member access in test_user_model.py
- Ensure all tests use correct constructor signatures and field names