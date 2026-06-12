# Lab 3: Security Analysis & Code Fixes

## Overview

In this lab, you'll use Bob to analyze existing code, identify security vulnerabilities, and implement fixes. You'll learn to recognize common security issues like SQL injection, XSS, and hardcoded secrets, then use Bob's different modes to fix them.

> **🔍 Bob Differentiator: [Bob Findings](../bob-differentiators.md#3--bob-findings-automated-analysis-engine)**
> This lab showcases Bob Findings, Bob's automated security and code quality analysis engine. Unlike simple linters, Bob Findings provides continuous, proactive analysis with specific remediation recommendations, severity ratings, and code examples. It's like having a security expert reviewing your code in real-time!

**Duration**: 45 minutes
**Difficulty**: Advanced

## What You'll Analyze

A vulnerable todo application with intentional security flaws:
- **SQL Injection** vulnerabilities in database queries
- **Cross-Site Scripting (XSS)** in frontend code
- **Hardcoded secrets** and credentials
- **Missing input validation**
- **Insecure error handling**

## Learning Objectives

By the end of this lab, you will:
- ✅ Use Ask mode to understand existing codebases
- ✅ Use Architect mode to identify bugs and plan fixes
- ✅ Recognize SQL injection vulnerabilities
- ✅ Identify XSS attack vectors
- ✅ Find hardcoded secrets and credentials
- ✅ Implement security fixes using Code mode
- ✅ Apply secure coding best practices

## Prerequisites

Before starting, ensure you have:
- [ ] Completed Lab 1 and Lab 2 (or familiar with Flask and JavaScript)
- [ ] Python 3.8+ installed
- [ ] Bob installed and running
- [ ] Understanding of basic web security concepts

## Lab Structure

```
Lab 3 Timeline (45 minutes)
├── Step 1: Code Exploration (10 min)
├── Step 2: Bug Identification (10 min)
├── Step 3: Security Analysis (15 min)
└── Step 4: Implementing Fixes (10 min)
```

---

## Step 1: Code Exploration with Ask Mode (10 minutes)

### Understanding the Vulnerable Codebase

The `vulnerable-app/` directory contains a todo application with intentional security issues. Let's use Bob's Ask mode to understand the code structure.

### 1.1: Switch to Ask Mode

Open Bob and switch to **Ask Mode** (❓).

### 1.2: Explore the Backend

**Prompt for Bob:**

```
Please analyze the code in lab3/vulnerable-app/backend/ and explain:
1. What is the overall structure of the application?
2. How are database queries constructed?
3. How is user input handled?
4. What security measures are in place?
```

**What to Look For:**

Bob should identify:
- Flask application with REST API endpoints
- Direct string concatenation in SQL queries ⚠️
- Hardcoded database credentials ⚠️
- Missing input validation ⚠️

### 1.3: Explore the Frontend

**Prompt for Bob:**

```
Analyze the frontend code in lab3/vulnerable-app/frontend/ and explain:
1. How is user input displayed in the UI?
2. Are there any DOM manipulation methods that could be risky?
3. How is data from the API rendered?
```

**What to Look For:**

Bob should identify:
- Use of `innerHTML` for rendering user content ⚠️
- No input sanitization ⚠️
- Direct insertion of user data into DOM ⚠️

### 1.4: Ask About Specific Functions

**Prompt for Bob:**

```
Explain the search_todos() function in app.py. 
What does it do and are there any security concerns?
```

**Expected Response:**

Bob should explain that the function uses string formatting to build SQL queries, which is vulnerable to SQL injection attacks.

**💡 Key Learning**: Ask mode is perfect for understanding unfamiliar code and getting explanations of how things work.

---

## Step 2: Bug Identification with Plan Mode (10 minutes)

Now let's use Architect mode to systematically identify all the issues.

### 2.1: Switch to Plan Mode

Change from Ask to **Plan Mode** (🎯).

### 2.2: Request Security Analysis

> **💡 Using Bob Findings**
> Bob Findings can automatically scan your code for security vulnerabilities, code quality issues, and compliance violations. The analysis you're about to request demonstrates Bob's [Security Vulnerability Detection](../bob-differentiators.md#security-vulnerability-detection) capabilities, which go beyond basic static analysis to provide context-aware recommendations.

**Prompt for Bob:**

```
Analyze the codebase in lab3/vulnerable-app/ for security vulnerabilities.
Create a comprehensive report including:
1. List of all security issues found
2. Severity rating for each issue (Critical/High/Medium/Low)
3. Potential impact of each vulnerability
4. Recommended fix for each issue
5. Priority order for fixes
```

**Expected Output:**

Bob should provide a structured analysis like:

```
SECURITY ANALYSIS REPORT
========================

CRITICAL ISSUES:
1. Hardcoded Database Credentials (config.py)
   - Impact: Full database access if code is exposed
   - Fix: Use environment variables
   - Priority: 1

2. SQL Injection (app.py, search_todos function)
   - Impact: Unauthorized data access, data manipulation
   - Fix: Use parameterized queries
   - Priority: 1

HIGH ISSUES:
3. Cross-Site Scripting (app.js, displayTodo function)
   - Impact: Script injection, session hijacking
   - Fix: Use textContent instead of innerHTML
   - Priority: 2

MEDIUM ISSUES:
4. Missing Input Validation
   - Impact: Invalid data in database
   - Fix: Add validation middleware
   - Priority: 3
```

### 2.3: Create Fix Plan

**Prompt for Bob:**

```
Based on the security analysis, create a detailed plan for fixing these issues.
Include:
1. Order of fixes (most critical first)
2. Files that need to be modified
3. Specific code changes required
4. Testing strategy
```

**Bob's Response:**

Bob will create a detailed TODO list with all the fixes needed. This demonstrates Bob's ability to break down complex problems into actionable steps.

**⚠️ Important**: Review the TODO list Bob creates, but **do not implement the fixes yet**. We'll examine each vulnerability type in detail in the next step before making any changes. This ensures you understand what you're fixing and why.

**💡 Key Learning**: Plan mode excels at analysis, planning, and creating structured approaches to problems. The TODO list serves as your roadmap for the implementation phase.

---

## Step 3: Security Vulnerability Deep Dive (15 minutes) - Optional

This step provides a detailed explanation of each vulnerability type. If you're already familiar with these security concepts, you can skip to [Step 4: Implementing Fixes](#step-4-implementing-fixes-10-minutes).

**What you'll learn in this deep dive:**
- How SQL injection attacks work
- How XSS vulnerabilities can be exploited
- Why hardcoded secrets are dangerous
- Best practices for secure coding

Let's examine each vulnerability type in detail.

### 3.1: SQL Injection Vulnerability

**Location**: `vulnerable-app/backend/app.py`

**Vulnerable Code:**
```python
@app.route('/api/todos/search', methods=['GET'])
def search_todos():
    query = request.args.get('q')
    # VULNERABLE: Direct string formatting in SQL
    sql = f"SELECT * FROM todos WHERE title LIKE '%{query}%'"
    results = db.session.execute(sql)
    return jsonify([dict(row) for row in results])
```

**The Problem:**

An attacker could send a malicious query like:
```
?q='; DROP TABLE todos; --
```

This would result in:
```sql
SELECT * FROM todos WHERE title LIKE '%'; DROP TABLE todos; --%'
```

**Prompt for Bob (Ask Mode):**

```
Explain how the SQL injection vulnerability in search_todos() works.
Provide an example of a malicious query and what damage it could cause.
```

**The Fix:**

Use parameterized queries:
```python
@app.route('/api/todos/search', methods=['GET'])
def search_todos():
    query = request.args.get('q')
    # SECURE: Parameterized query
    results = Todo.query.filter(Todo.title.like(f'%{query}%')).all()
    return jsonify([todo.to_dict() for todo in results])
```

### 3.2: Cross-Site Scripting (XSS) Vulnerability

**Location**: `vulnerable-app/frontend/app.js`

**Vulnerable Code:**
```javascript
function displayTodo(todo) {
    const todoElement = document.createElement('div');
    // VULNERABLE: innerHTML with user content
    todoElement.innerHTML = `
        <h3>${todo.title}</h3>
        <p>${todo.description}</p>
    `;
    document.getElementById('todo-list').appendChild(todoElement);
}
```

**The Problem:**

An attacker could create a todo with title:
```html
<img src=x onerror="alert('XSS Attack!')">
```

This script would execute when the todo is displayed.

**Prompt for Bob (Ask Mode):**

```
Explain the XSS vulnerability in the displayTodo() function.
Show me an example of a malicious payload and how it would execute.
```

**The Fix:**

Use `textContent` instead of `innerHTML`:
```javascript
function displayTodo(todo) {
    const todoElement = document.createElement('div');
    const title = document.createElement('h3');
    const description = document.createElement('p');
    
    // SECURE: textContent prevents script execution
    title.textContent = todo.title;
    description.textContent = todo.description;
    
    todoElement.appendChild(title);
    todoElement.appendChild(description);
    document.getElementById('todo-list').appendChild(todoElement);
}
```

### 3.3: Hardcoded Secrets Vulnerability

**Location**: `vulnerable-app/backend/config.py`

**Vulnerable Code:**
```python
# VULNERABLE: Hardcoded credentials
DATABASE_URL = "postgresql://admin:SuperSecret123@localhost/todos"
API_KEY = "sk_live_abc123xyz789"
SECRET_KEY = "my-secret-key-12345"
```

**The Problem:**

- Credentials are visible in source code
- Anyone with code access has full system access
- Credentials can't be changed without code changes
- Different environments use same credentials

**Prompt for Bob (Ask Mode):**

```
Why are hardcoded secrets a security risk?
What are the best practices for managing secrets in applications?
```

**The Fix:**

Use environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()

# SECURE: Load from environment
DATABASE_URL = os.getenv('DATABASE_URL')
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

# Validate that secrets are loaded
if not all([DATABASE_URL, API_KEY, SECRET_KEY]):
    raise ValueError("Missing required environment variables")
```

Create `.env` file (never commit this!):
```
DATABASE_URL=postgresql://admin:SuperSecret123@localhost/todos
API_KEY=sk_live_abc123xyz789
SECRET_KEY=my-secret-key-12345
```

### 3.4: Testing Vulnerabilities

**⚠️ WARNING**: Only test on your own systems!

**Test SQL Injection:**
```bash
# Try to inject SQL
curl "http://localhost:5000/api/todos/search?q=test'%20OR%20'1'='1"
```

**Test XSS:**
```bash
# Create todo with script
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"<script>alert(\"XSS\")</script>","description":"test"}'
```

---

## Step 4: Implementing Fixes with Code Mode (10 minutes)

Now let's fix all the vulnerabilities using Bob's Code mode.

### 4.1: Switch to Code Mode

Change to **Code Mode** (💻).

### 4.2: Fix SQL Injection

**Prompt for Bob:**

```
Fix the SQL injection vulnerability in vulnerable-app/backend/app.py.
Replace the string formatting with parameterized queries using SQLAlchemy.
```

Bob should modify the `search_todos()` function to use safe queries.

### 4.3: Fix XSS Vulnerability

**Prompt for Bob:**

```
Fix the XSS vulnerability in vulnerable-app/frontend/app.js.
Replace innerHTML usage with safe DOM manipulation using textContent.
Update all functions that display user-generated content.
```

### 4.4: Fix Hardcoded Secrets

**Prompt for Bob:**

```
Fix the hardcoded secrets in vulnerable-app/backend/config.py.
1. Move secrets to environment variables
2. Create a .env.example file with placeholder values
3. Add python-dotenv to requirements.txt
4. Update the code to load from environment
```

### 4.5: Add Input Validation

**Prompt for Bob:**

```
Add input validation to the todo creation endpoint.
Validate:
- Title is required and not empty
- Title length is between 1 and 200 characters
- Description length is less than 1000 characters
Return appropriate error messages for invalid input.
```

### 4.6: Verify Fixes

**Important**: Bob has made the fixes directly to the files in `lab2/vulnerable-app/` (not in a separate solution folder). The vulnerable code has been replaced with secure code.

Run the application and test the fixes:

```bash
# Start backend (from the vulnerable-app directory where fixes were applied)
cd lab3/vulnerable-app/backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py # may conflict with AirPlay on the Mac, in which case run the following instead:
FLASK_RUN_PORT=8080 flask run

# Open frontend (from the vulnerable-app directory)
cd ../frontend
# Open index.html in browser
```

**Test Security:**
1. Try SQL injection - should fail safely (no data leaked)
2. Try XSS payload - should display as plain text (not execute)
3. Check no secrets in code (verify config.py uses environment variables)
4. Test input validation (try empty title, too long title, etc.)

**Compare Before/After:**
If you want to see the original vulnerable code, you can review the git history or ask Bob to explain what the vulnerabilities were before the fixes.

---

## Congratulations! 🎉

You've successfully completed Lab 3! You've learned to:

- ✅ Use Ask mode to understand existing code
- ✅ Use Architect mode for security analysis
- ✅ Identify SQL injection vulnerabilities
- ✅ Recognize XSS attack vectors
- ✅ Find and fix hardcoded secrets
- ✅ Implement secure coding practices
- ✅ Use Code mode to fix security issues

> **🎯 Bob Findings in Action**
> In this lab, you experienced Bob's [automated security analysis](../bob-differentiators.md#security-vulnerability-detection) capabilities. Bob Findings continuously monitors your code for vulnerabilities and provides actionable remediation guidance. This proactive approach helps you catch security issues before they reach production, reducing risk and technical debt.

## Security Best Practices Learned

### 1. SQL Injection Prevention
- ✅ Always use parameterized queries
- ✅ Never concatenate user input into SQL
- ✅ Use ORM features (like SQLAlchemy)
- ✅ Validate and sanitize input

### 2. XSS Prevention
- ✅ Use `textContent` instead of `innerHTML`
- ✅ Sanitize user input before display
- ✅ Use Content Security Policy headers
- ✅ Encode output properly

### 3. Secrets Management
- ✅ Never hardcode credentials
- ✅ Use environment variables
- ✅ Use secret management services
- ✅ Rotate secrets regularly
- ✅ Never commit secrets to version control

### 4. Input Validation
- ✅ Validate all user input
- ✅ Use whitelist validation
- ✅ Set appropriate length limits
- ✅ Return clear error messages

## Comparison: Before and After

### Before (Vulnerable)
```python
# SQL Injection risk
sql = f"SELECT * FROM todos WHERE title LIKE '%{query}%'"

# Hardcoded secrets
DATABASE_URL = "postgresql://admin:password@localhost/db"

# XSS risk
element.innerHTML = `<h3>${userInput}</h3>`
```

### After (Secure)
```python
# Safe parameterized query
results = Todo.query.filter(Todo.title.like(f'%{query}%')).all()

# Environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Safe DOM manipulation
element.textContent = userInput
```

## Additional Security Resources

### OWASP Top 10
1. Injection
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entities (XXE)
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting (XSS)
8. Insecure Deserialization
9. Using Components with Known Vulnerabilities
10. Insufficient Logging & Monitoring

### Recommended Reading
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)
- [JavaScript Security Best Practices](https://developer.mozilla.org/en-US/docs/Web/Security)

## Next Steps

### Continue Learning
You've completed all three labs! Great work! 🎉

### Apply Your Skills
- Use Bob on your own projects
- Practice security analysis on real codebases
- Share what you've learned with your team

### Practice More
Try finding and fixing these additional vulnerabilities:
1. **CSRF** - Add CSRF protection
2. **Authentication** - Implement user authentication
3. **Authorization** - Add role-based access control
4. **Rate Limiting** - Prevent brute force attacks
5. **HTTPS** - Enforce secure connections

## Troubleshooting

### Backend Issues

**Problem**: Import errors after fixing secrets
```bash
# Install python-dotenv
pip install python-dotenv
```

**Problem**: Environment variables not loading
```bash
# Check .env file exists
ls -la .env

# Verify .env format (no spaces around =)
DATABASE_URL=value
```

### Frontend Issues

**Problem**: XSS still working after fix
- Verify you're using `textContent` not `innerHTML`
- Check all user input display points
- Clear browser cache

### Testing Issues

**Problem**: Can't test SQL injection
- Ensure you're testing on the vulnerable version first
- Check backend is running
- Verify endpoint URL is correct

## Feedback

How was this lab? We'd love to hear:
- Did you find all the vulnerabilities?
- Were the explanations clear?
- What other security topics interest you?

---

**Congratulations on completing the Bob Watch Party Labs!** 🎉

*Last Updated: December 2025*