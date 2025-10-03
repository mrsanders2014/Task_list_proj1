# **Task_list_proj1**
### Author: Michael Sanders 

## **Project Overview**
This project is intended to build a full-stack TODO application with user authentication, tasks, and labels. The backend will be a RESTful API built with Python's FastAPI, and the frontend will be a Next.js application. The application will use MongoDB for data persistence. This project is designed to provide hands-on experience with modern web development tools and best practices.

## Features Include: 
These are the essential features that must be completed for a passing grade.

### User Management
    
    Account creation by a user designed to create/manage task lists.
    Login capability so that a user profile and tasks can be managed (including deletion)
    Ensure proper 'logout' capability to ensure security of users data.

### Task Management
    Be able create a new task, be able to assign priority, start/stop date and predecessor task
    Be able to view all existing tasks in various sort form
    Be able to update an existing task on every field with certain exceptions
    Be able to delete a task

### Labeling System
    Be able tocreate and manage labels (e.g., 'Work,' 'Personal,' 'Urgent'), so I can categorize and/or prioritize my tasks.
    Be able to assign one or more labels to a task, so I can easily filter and organize my tasks.

### Required Task Fields: Every task must include a 
-title 
-optional description 
-priority level (e.g., High, Medium, Low)
-task color
-deadline (due-date)
-time unit for task
-task status
-can task be done in parallel with other tasks?
-if so, list of parallel tasks
-predecessor task


### Data Persistence
    The application must persist all user, task, and label data in a MongoDB database.

### Possible Goals as of 10/1/25

    As a user, I want to filter my tasks by label, so I can quickly find and organize what I need to work on.
    As a user, I want to be able to edit my profile details, so I can keep my information up to date.
    As a user, I want the application to be responsive and work well on different screen sizes, so I can access my tasks from any device, including my phone or tablet.
    As a user, I want to see clear, helpful messages when something goes wrong, so I know what happened and how to proceed.

### Technical Requirements & File Structure
Use best python practices for project structure
Will include the use UV project management

### Database: MongoDB
The project should leverage a MongoDB database filled with appropriately modeled documents & collections. 
Initial design will consist of a database with 2 collections: Users and Tasks. Tasks will be related to Users (1 user -> many tasks)

### Backend: FastAPI
The project directory will follow a modular structure based on current Python best practices. 

### Frontend: Next.js
The project structure should follow best practices for a Next.js application. 



### GitHubRepository Location/URL
   [Task_list_proj1](https://github.com/mrsanders2014/Task_list_proj1)

## Technical Build and Run Instructions
Instructions on how to set up and run the application.

A list of technologies used.
A list of completed features (and stretch goals, if any).

