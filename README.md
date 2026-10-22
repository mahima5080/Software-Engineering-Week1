# Command-Line Task Manager (Software Engineering — Week 1)

A clean, object-oriented Command-Line Interface (CLI) Task Manager built with Python. This application allows users to perform full CRUD operations on tasks, assign priorities and due dates, persist data using JSON storage, and handle user errors gracefully.

---

## 📌 Features

- **Create (Add Task):** Create tasks with titles, priorities (`LOW`, `MEDIUM`, `HIGH`), and due dates (`YYYY-MM-DD`).
- **Read (View Tasks):** Display all pending and completed tasks with formatted status indicators.
- **Update (Modify Task):** Selectively update task titles, priority levels, or due dates.
- **Delete (Remove Task):** Remove completed or unwanted tasks by ID.
- **Mark Complete:** Instantly update task status to completed (`✓ Done`).
- **JSON Persistence:** All tasks are saved automatically to `tasks.json` across sessions.
- **Robust Error Handling:** Validates user inputs (empty fields, invalid dates, numerical IDs) to prevent crashes.

---

## 🏗️ Architecture & OOP Design

- **`Task` Class:** Encapsulates task properties (`task_id`, `title`, `priority`, `due_date`, `completed`) and handles JSON serialization/deserialization.
- **`TaskManager` Class:** Manages file I/O operations and task collection modifications (Create, Read, Update, Delete).
- **Separation of Concerns:** Business logic and CLI user interactions are cleanly separated.

---

## 🚀 How to Run the Application

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mahima5080/Software-Engineering-Week1.git](https://github.com/mahima5080/Software-Engineering-Week1.git)
   cd Software-Engineering-Week1
