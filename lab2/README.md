# Lab 2: Beginner - Building a Todo Application with Bob

## Overview

In this lab, you'll learn to use Bob's AI-powered features to build a complete full-stack todo application from scratch. You'll experience Bob's different modes, auto-approvals, literate coding, and GitHub integration.

**Duration**: 45 minutes
**Difficulty**: Beginner to Intermediate

## 💡 Building From Scratch

In this lab, you'll build the entire application from scratch with Bob's help. There are no starter files or solution folders - you'll create everything yourself! This gives you the full experience of using Bob to build a complete application.

Don't worry if you get stuck - Bob is there to help you at every step. Just ask questions and iterate on the code together.

## What You'll Build

A full-stack todo application with:
- **Backend**: Python Flask REST API with SQLite database
- **Frontend**: Modern JavaScript single-page application
- **Features**: Create, read, update, and delete todos
- **Version Control**: GitHub repository with proper commits

## Learning Objectives

By the end of this lab, you will:
- ✅ Understand Bob's three modes (Plan, Code, Ask)
- ✅ Use auto-approvals for rapid development
- ✅ Practice literate coding techniques
- ✅ Integrate GitHub using MCP servers
- ✅ Build a complete full-stack application

## Prerequisites

Before starting, ensure you have:
- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed (for npm)
- [ ] Git installed and configured
- [ ] Bob installed and running
- [ ] GitHub account (for MCP integration)
- [ ] Text editor or IDE open

If you haven't completed setup, see [prerequisites.md](../prerequisites.md).

## Lab Structure

```
Lab 2 Timeline (45 minutes)
├── Step 1: Introduction & Planning (5 min)
├── Step 2: Backend Development (15 min)
├── Step 3: Frontend Development (15 min)
├── Step 4: GitHub Integration (5 min)
└── Step 5: Testing & Verification (5 min)
```

---

## Step 1: Introduction to Bob Modes (5 minutes)

### Understanding Bob's Modes

Bob has three distinct modes, each optimized for different tasks:

#### 🎯 Plan Mode
**When to use**: Planning, designing, strategizing
- Create project structures
- Design API endpoints
- Plan database schemas
- Make architectural decisions

#### 💻 Code Mode
**When to use**: Writing, modifying, refactoring code
- Implement features
- Create files
- Modify existing code
- Fix bugs

#### ❓ Ask Mode
**When to use**: Learning, understanding, getting help
- Explain code concepts
- Get documentation
- Understand errors
- Learn best practices

### Switching Between Modes

In Bob's interface:
1. Look for the mode selector (usually at the top)
2. Click to see available modes
3. Select the mode you need
4. Bob will adapt its behavior accordingly

### Your First Task: Project Planning

**Switch to Plan Mode** and ask Bob:

```
I want to create a todo application with a Python Flask backend and JavaScript frontend.
Please help me plan:
1. Project directory structure
2. API endpoints needed
3. Database schema
4. Technology stack recommendations

I want to build this completely from scratch.
```

**Bob's Interactive Approach:**

Before providing a plan, Bob will ask clarifying questions to understand your requirements better. This is a key differentiator—Bob lets you drive the process while making helpful suggestions.

Bob might ask:
- "How complex should the application be?"
- "Which database would you prefer (SQLite, PostgreSQL, MySQL)?"
- "Do you need user authentication?"
- "Should we include additional features like categories or priorities?"

**For this lab, respond with basic requirements:**
- Simple/basic complexity
- SQLite database (no installation needed)
- No user authentication
- Basic CRUD operations only

This collaborative approach ensures Bob builds exactly what you need, not what it assumes you want.

**Expected Response from Bob:**

After your clarifications, Bob should provide:
- Directory structure with backend/ and frontend/ folders
- REST API endpoints (GET, POST, PUT, DELETE)
- Database schema for todos (id, title, description, completed, created_at)
- Recommendations for Flask, SQLite, CORS, etc.

**💡 Tip**: Take notes on Bob's recommendations. You'll use this plan in the next steps.

---

## Step 2: Backend Development with Code Mode (15 minutes)

Now let's build the Flask backend using Bob's Code mode.

### 2.1: Switch to Code Mode

Change from Plan to Code mode in Bob's interface.

### 2.2: Create Backend Structure

**Prompt for Bob:**

```
Create a Flask backend for the todo app in a new directory called 'todo-app/backend/' with the following files:
1. app.py - Main Flask application with CORS enabled
2. models.py - SQLAlchemy Todo model
3. database.py - Database initialization
4. requirements.txt - Python dependencies

The Todo model should have: id, title, description, completed (boolean), created_at (timestamp)

Build this completely from scratch.
```

**What Bob Will Create:**

Bob should generate these files in the `backend/` directory. Review each file as Bob creates them.

### 2.3: Understanding Auto-Approvals

**Auto-approvals** allow Bob to make multiple changes without asking for confirmation each time.

To enable auto-approvals:
1. Look for auto-approval settings in Bob
2. Enable for this session
3. Bob will now create multiple files rapidly

**⚠️ Important**: Review the files after Bob creates them to ensure they match your requirements.

### 2.4: Implement REST API Endpoints

**Prompt for Bob:**

```
Implement the following REST API endpoints in app.py:
- GET /api/todos - List all todos
- POST /api/todos - Create a new todo
- PUT /api/todos/<id> - Update a todo
- DELETE /api/todos/<id> - Delete a todo

Include proper error handling and JSON responses.
```

### 2.5: Review Generated Code

Bob should have created something similar to this structure:

**app.py** (Key sections):
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Todo
from database import db, init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

init_db(app)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo = Todo(
        title=data.get('title'),
        description=data.get('description', ''),
        completed=False
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

# Additional endpoints...
```

### 2.6: Create Unit Test Cases and Run them

**Prompt for Bob:**

```bash
Create unit test cases for each of the api endpoints, and ensure at least 90% code coverage.
```

### 2.7: Test Backend Setup

**Important:** Always use a virtual environment to isolate project dependencies.

Create a virtual environment and install dependencies:

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

**Why use a virtual environment?**
- Isolates project dependencies from system Python packages
- Prevents version conflicts between different projects
- Makes it easy to reproduce the exact environment on other machines
- Keeps your system Python installation clean

**Note:** Remember to activate the virtual environment every time you work on the project. You'll know it's activated when you see `(venv)` in your terminal prompt.

Alternatively, you can ask Bob to do that for you.

**Prompt for Bob:**

```bash
Run the backend application and test it with 1 sample curl command per each API endpoint.
```

The server should start on `http://localhost:5000`

**✅ Checkpoint**: Backend is running without errors.

---

## Step 3: Frontend Development (15 minutes)

Now let's create the user interface using JavaScript.

### 3.1: Create Frontend Structure

**Prompt for Bob (still in Code mode):**

```
Create a frontend for the todo app in todo-app/frontend/ with:
1. index.html - Main HTML structure with a clean, modern design
2. styles.css - Responsive CSS styling
3. app.js - JavaScript for API interactions

Include:
- Input field for new todos
- List to display todos
- Buttons for complete and delete actions
- Responsive design for mobile and desktop
```

### 3.2: Understanding Literate Coding

**Literate coding** means writing code that explains itself through comments and clear structure.

**Prompt for Bob:**

```
In app.js, use literate coding to explain:
- How the API calls work
- Why we use async/await
- How error handling is implemented
- The purpose of each function

Add detailed comments that would help a beginner understand the code.
```

### 3.3: Review Frontend Code

Bob should create files similar to this:

**app.js** (with literate coding):
```javascript
/**
 * Todo Application - Frontend JavaScript
 * 
 * This file handles all interactions between the user interface
 * and the Flask backend API. We use modern JavaScript features
 * like async/await for cleaner asynchronous code.
 */

// API base URL - points to our Flask backend
const API_URL = 'http://localhost:5000/api/todos';

/**
 * Fetches all todos from the backend API
 * 
 * This function demonstrates the async/await pattern:
 * - 'async' keyword allows us to use 'await' inside
 * - 'await' pauses execution until the promise resolves
 * - This makes asynchronous code look synchronous and easier to read
 * 
 * @returns {Promise<void>}
 */
async function fetchTodos() {
    try {
        // Make GET request to backend
        const response = await fetch(API_URL);
        
        // Parse JSON response
        const todos = await response.json();
        
        // Update the UI with fetched todos
        displayTodos(todos);
    } catch (error) {
        // Handle any errors (network issues, server errors, etc.)
        console.error('Error fetching todos:', error);
        showError('Failed to load todos. Please try again.');
    }
}

/**
 * Creates a new todo item
 * 
 * This function shows how to make a POST request with JSON data.
 * We use the Fetch API which returns promises, making it perfect
 * for async/await syntax.
 * 
 * @param {string} title - The todo title
 * @param {string} description - The todo description
 */
async function createTodo(title, description) {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, description })
        });
        
        if (response.ok) {
            // Refresh the todo list
            await fetchTodos();
            // Clear the input form
            clearForm();
        }
    } catch (error) {
        console.error('Error creating todo:', error);
        showError('Failed to create todo. Please try again.');
    }
}

// Additional functions with detailed explanations...
```

### 3.4: Test Frontend

Open `frontend/index.html` in your browser:

```bash
# From the lab2 directory
cd frontend

# Open in default browser
# Windows:
start index.html
# macOS:
open index.html
# Linux:
xdg-open index.html
```

**✅ Checkpoint**: Frontend loads and displays the UI.

---

## Step 4: GitHub Integration with MCP (10 minutes)

Now let's use Bob's GitHub MCP server to manage version control.

### 4.1: Switch to Advanced Mode

Before using GitHub MCP servers, switch to Advanced mode:

1. Click the mode selector in Bob's interface
2. Select **Advanced** mode (⚡ Advanced)
3. Confirm the mode switch

**Why Advanced mode is required:**
- Advanced mode provides the same code editing capabilities as Code mode, plus advanced GitHub MCP server access
- With Advanced mode, Bob can execute advanced GitHub operations (create repos, make commits, push code)

Once in Advanced mode, you can use all the same code editing features while also accessing GitHub MCP integrations.

### 4.2: Understanding MCP Servers

> **🔧 Bob Differentiator: [MCP Server Integration](../bob-differentiators.md#mcp-server-integration)**
> Bob's MCP (Model Context Protocol) integration is a powerful differentiator that allows you to connect external tools and services directly into your workflow. Unlike other AI assistants that work in isolation, Bob can integrate with your company's internal APIs, databases, documentation systems, and more. This means Bob adapts to YOUR environment, not the other way around.

**MCP (Model Context Protocol)** allows Bob to interact with external services like GitHub.

Benefits:
- Bob can create repositories
- Bob can make commits
- Bob can push code
- All through natural language commands
- **Extensible**: Connect to any service with an MCP server (JIRA, databases, deployment tools, etc.)
- **Seamless**: No context switching between tools

### 4.2: Initialize Git Repository

**Prompt for Bob:**

```
Use the GitHub MCP server to:
1. Initialize a git repository in the current directory
2. Create a .gitignore file for Python and Node.js
3. Create an initial commit with message "Initial todo app implementation"
```

### 4.3: Create GitHub Repository

**Prompt for Bob:**

```
Create a new GitHub repository called "bob-todo-app" and push the code.
Include a README.md describing the project.
```

**What Bob Will Do:**
1. Create `.gitignore` with appropriate entries
2. Initialize git repository
3. Add all files to staging
4. Create initial commit
5. Create GitHub repository (if MCP is configured)
6. Push code to GitHub

### 4.4: Verify on GitHub

1. Go to your GitHub account
2. Find the `bob-todo-app` repository
3. Verify all files are present
4. Check the commit history

**✅ Checkpoint**: Code is on GitHub with proper commits.

---

## Step 5: Testing & Verification (5 minutes)

Let's test the complete application end-to-end.

### 5.1: Start the Backend

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if not already activated)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run the application
python app.py
```

Server should be running on `http://localhost:5000`

**💡 Tip:** You'll know the virtual environment is activated when you see `(venv)` at the beginning of your terminal prompt.

### 5.2: Open the Frontend

Open `frontend/index.html` in your browser.

### 5.3: Test CRUD Operations

**Create a Todo:**
1. Enter a title: "Learn Bob"
2. Enter a description: "Complete all three labs"
3. Click "Add Todo"
4. ✅ Todo appears in the list

**Mark as Complete:**
1. Click the "Complete" button on a todo
2. ✅ Todo shows as completed (strikethrough or checkmark)

**Delete a Todo:**
1. Click the "Delete" button on a todo
2. ✅ Todo is removed from the list

**Refresh Page:**
1. Refresh the browser
2. ✅ Todos persist (stored in database)

### 5.4: Check Browser Console

Open browser developer tools (F12):
- ✅ No JavaScript errors
- ✅ API calls succeed (200 status codes)
- ✅ Data is properly formatted

### 5.5: Verify Database

```bash
# In backend directory
python
>>> from app import app, db
>>> from models import Todo
>>> with app.app_context():
...     todos = Todo.query.all()
...     for todo in todos:
...         print(f"{todo.id}: {todo.title}")
```

✅ Todos are stored in the database

---

## Congratulations! 🎉

You've successfully completed Lab 1! You've learned to:

- ✅ Use Bob's Plan mode for planning
- ✅ Use Bob's Code mode for implementation
- ✅ Enable and use auto-approvals
- ✅ Apply literate coding principles
- ✅ Integrate GitHub using MCP servers
- ✅ Build a complete full-stack application

## What You've Built

```
bob-todo-app/
├── backend/
│   ├── app.py              # Flask REST API
│   ├── models.py           # Database models
│   ├── database.py         # DB initialization
│   ├── requirements.txt    # Dependencies
│   └── todos.db           # SQLite database
├── frontend/
│   ├── index.html         # UI structure
│   ├── styles.css         # Styling
│   └── app.js             # Frontend logic
└── .gitignore             # Git ignore rules
```

## Key Takeaways

### Bob's Modes
- **Plan**: Perfect for planning and design decisions
- **Code**: Best for implementation and file creation
- **Ask**: Great for learning and understanding
- **Custom Modes**: Create your own specialized modes ([Learn more](../bob-differentiators.md#customizable-modes))

### Auto-Approvals
- Speeds up development significantly
- Useful for creating multiple related files
- Always review the generated code

### Literate Coding
- Makes code self-documenting
- Helps team members understand your code
- Useful for learning and teaching

### GitHub MCP
- Streamlines version control
- Natural language git operations
- Integrates seamlessly with Bob
- **Extensible**: Part of Bob's [MCP Server Integration](../bob-differentiators.md#mcp-server-integration) capability

> **💡 Behind the Scenes: Intelligent Resource Optimization**
> While you've been building this app, Bob has been automatically selecting the right AI model for each task—using powerful models for complex architecture decisions and lighter models for simple file operations. This [automatic model selection](../bob-differentiators.md#automatic-model-selection) optimizes both quality and cost without you having to think about it. You can save up to 60% on AI costs while maintaining excellent results!

## Next Steps

### Enhance Your App
Try these improvements:
1. Add todo categories or tags
2. Implement due dates
3. Add user authentication
4. Create a priority system
5. Add search and filter functionality

### Continue Learning
- **[Lab 1: Bring Your Own Use Case ←](../lab1/README.md)** - Explore Bob with your own project
- **[Lab 3: Advanced - Security Analysis →](../lab3/README.md)** - Learn to identify and fix security vulnerabilities

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'flask'`
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Problem**: `Address already in use`
```bash
# Kill the process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

**Problem**: Database errors
```bash
# Delete and recreate database
rm todos.db
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

### Frontend Issues

**Problem**: CORS errors in browser console
- Ensure Flask-CORS is installed: `pip install flask-cors`
- Verify CORS is enabled in `app.py`
- Check backend is running on port 5000

**Problem**: API calls fail
- Verify backend is running
- Check API_URL in `app.js` matches backend URL
- Open browser dev tools and check Network tab

**Problem**: Todos don't persist
- Check browser console for errors
- Verify database file exists
- Test API endpoints directly using curl or Postman

### Git/GitHub Issues

**Problem**: Git not initialized
```bash
git init
git add .
git commit -m "Initial commit"
```

**Problem**: GitHub authentication fails
- Verify GitHub MCP is configured in Bob
- Check GitHub personal access token
- Try manual git push to test credentials

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [JavaScript Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bob Documentation](https://bob-docs-url)

## Feedback

How was this lab? We'd love to hear your thoughts:
- What worked well?
- What was confusing?
- What would you like to see added?

---

**Ready for the next challenge?** → [Start Lab 3: Advanced - Security Analysis](../lab3/README.md)

**Last Updated: February 2026**
