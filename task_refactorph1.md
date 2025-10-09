
# Refactoring Plan: User Authentication Module

## Project Context
This project is a web application that will use NEXTJS, Fastapi and Beanie. 
The database entity consists of a user class and a task class.  
The task class needs to be refactored to add additional fields, and move some fields into sub lists.

## Refactoring Goals
1.  ** Better definition of Tasks:** Make class better defined.
2.  ** Increase Maintainability:** Refactor existing functions for better readability and modularity.
3.  ** Remove Technical Debt:** Eliminate deprecated functions and unnecessary code.

## High-Level Plan
1.  ** Refactor src/model/task.py with details below**
2.  ** Update all associated code that uses or requires task.py accordingly**
3.  ** Documentation Update**: Update all documentation to reflect new changes.
4.  ** Testing:** Ensure all changes are covered by unit and integration tests.

## Detailed Steps

### Phase 1: Class task
A. ** Class task should now consist of the following fields
	- _id :[objectid] **id assigned by MongoDB
   	- user_id:[objectid] ** MongoDb id assigned to the user who created the task. (Users can create 1 to many tasks; all tasks are owned by a specified user; a user can have zero tasks).
	- task title :string ( 50 characters maximum, required)\
	- description :string ( 250 character maximum, optional)\
	- createdate : timestamp (when task is created)\
	- lastmoddate : timestamp (when task is last modified from business rule)\
	- status (can be one of "Created", "Started", "InProcess", "Modified", "Scheduled", "Complete", "Deleted") default = "Created"
	- labels : optional[List[Labels]] = None
	- task_mgmt :optional[[List[task_mgmt_details] = None
	- task_history : list[previous_status, new_status, lastmoddate, reason : string]

B. ** Class task_mgmt_details will consist of the following fields\
	- Priority : integer range from 1-10 default = 1 (1 is high, 10 is low)
	- duedate : date stamp. Date must be in the future by at least 1 minute from creation time
	- time_unit : ("minutes", "hours", "days", "weeks", "months", "years") default = "hours"
	- estimated_time_to_complete : float, minimum 1 time_unit
	- Notify_time: float, default = 0
	- Notify_time_units : time_unit
	- Notification_wanted : Y/N, default = N
	- time_mgmt : List[task_time_mgmt]

C. ** Class task_time_mgmt will consist of the following fields
	- create_date ; timestamp
	- scheduled_start_date : timestamp
	- actual_start_date: timestamp
	- scheduled_comp_date: timestamp
	- actual_comp_date: timestamp
	- archived_date: timestamp
D. **Refactor 'cli.py' to reflect the changes

### Phase 3: Code Cleanup and Refactoring\
1.  **Extract Functions:** Break down large functions in all '.py' fields into smaller, more focused functions (e.g., `validate_credentials`, `hash_password`).\
2.  **Rename Variables:** Improve variable and function naming for better clarity.
3.  **Remove Dead Code:** Identify and remove any unused functions or imports.
4.  **Docstrings and Type Hinting:** Add comprehensive docstrings and type hints to all functions.
5.  **Documentation:** Read all .MD files and update them accordingly

### Phase 4: Testing
1.  **Unit Tests:** Create or update unit tests for all new and modified functions.
2.  **Run unit tests with pytester**


## Files to be Modified\
*   `src/model/task.py'
*   'src/model/user.py'
*   'src/dbase/task_repository.py'
*   'src/dbase/user_repository.py'
*   'src/dbase/connection.py'

}