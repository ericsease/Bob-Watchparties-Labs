# Bob Hands-On Labs

Welcome to the Bob hands-on labs! This practical training series will teach you how to leverage Bob's AI-powered development capabilities through real-world exercises.

## 🎯 Overview

These labs are designed to give you hands-on experience with Bob's core features through five progressive exercises:

1. **Lab 1: Bring Your Own Use Case** — Explore Bob with a project of your choice
2. **Lab 2: Beginner - Building a Todo Application** — Create a full-stack application from scratch
3. **Lab 3: Advanced - Security Analysis & Code Fixes** — Identify and fix security vulnerabilities
4. **Lab 4: Bob v2 in Action — The Bookmarks Feature** — Subagents, parallel tool calls, and workflows
5. **Lab 5: Java Modernization Partner** — Migrate a legacy Java 8 service to Java 17 with Bob

**Total Learning Time**: ~3.5 hours (pick the labs that match your interests!)

## 🚀 Quick Start

### Step 1: Clone This Repository

First, let's get the lab materials on your computer. Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and run:

```bash
# Clone the repository
git clone https://github.com/ericsease/Bob-Watchparties-Labs.git

# Navigate into the directory
cd Bob-Watchparties-Labs
```

**Don't have Git?** [Download and install Git here](https://git-scm.com/downloads)

**What is git clone?** This command downloads all the lab files from GitHub to your computer so you can work with them locally.

### Step 2: Open in Bob

Now let's open the labs in Bob:

1. **Launch Bob IDE** on your computer
2. **Open the folder:**
   - Click `File` → `Open Folder` (or `File` → `Open` on Mac)
   - Navigate to the folder you just cloned
   - Click `Select Folder` (or `Open` on Mac)

3. **Verify it worked:**
   - You should see the lab folders (lab1, lab2, lab3, lab4, lab5) in Bob's file explorer
   - You should see this README.md file

**Don't have Bob?** Make sure Bob is installed and configured before proceeding. Contact your administrator if you need access.

### Step 3: Check Prerequisites

Before starting the labs, make sure you have the required software installed. See [prerequisites.md](prerequisites.md) for detailed setup instructions.

**Quick check:**

```bash
# Check Python version (need 3.8+)
python --version
# or
python3 --version

# Check Git version
git --version
```

### Step 4: Choose Your Starting Point

- **New to Bob?** → Start with [Lab 1: Bring Your Own Use Case](lab1/README.md)
- **Want structured learning?** → Start with [Lab 2: Beginner - Todo App](lab2/README.md)
- **Interested in security?** → Start with [Lab 3: Advanced - Security Analysis](lab3/README.md)
- **Want to see Bob v2 in action?** → Try [Lab 4: Bookmarks Feature](lab4/README.md)
- **Enterprise Java / SAP developer?** → Try [Lab 5: Java Modernization](lab5/README.md)

---

## 📚 Lab Descriptions

### 🟢 Lab 1: Bring Your Own Use Case (30-45 minutes)

**Perfect for:** First-time Bob users who want to explore freely

Explore Bob's capabilities by building something that interests you! This open-ended lab provides:

- Suggested project ideas (browser games, productivity tools, dashboards)
- Best practices for proof-of-concept projects
- Tips for effective prompting
- Guidance on using Bob's different modes

**What you'll learn:**

- How to effectively prompt Bob
- When to use different Bob modes
- Rapid prototyping with AI assistance
- Iterative development techniques

**[Start Lab 1 →](lab1/README.md)**

---

### 🟢 Lab 2: Beginner - Building a Todo Application (45 minutes)

**Perfect for:** Learning Bob's core features through a structured beginner project

Build a complete full-stack application from scratch using Bob's AI-powered features.

**What you'll build:**

- Python Flask REST API backend
- JavaScript frontend with modern UI
- SQLite database integration
- Complete CRUD operations

**Bob features you'll use:**

- ✅ Plan Mode for architecture and planning
- ✅ Code Mode for implementation
- ✅ Auto-approvals for rapid development
- ✅ Literate coding for self-documenting code

**What you'll learn:**

- Switching between Bob's modes effectively
- Using auto-approvals safely
- Building full-stack applications with AI
- Rapid prototyping with Bob

**[Start Lab 2 →](lab2/README.md)**

---

### 🔴 Lab 3: Advanced - Security Analysis & Code Fixes (45 minutes)

**Perfect for:** Developers who want to learn security best practices and vulnerability detection

Use Bob to analyze existing code, identify security vulnerabilities, and implement fixes. Learn to recognize common security issues like SQL injection, XSS, and hardcoded secrets.

**What you'll analyze:**

- SQL injection vulnerabilities in database queries
- Cross-site scripting (XSS) in frontend code
- Hardcoded secrets and credentials
- Missing input validation
- Insecure error handling

**Bob features you'll use:**

- ✅ Ask Mode for code understanding
- ✅ Plan Mode for security analysis and planning
- ✅ Code Mode for implementing fixes
- ✅ Bob Findings for automated vulnerability detection
- ✅ Multi-file code analysis

**What you'll learn:**

- Using Bob's different modes for security analysis
- Identifying SQL injection vulnerabilities
- Recognizing XSS attack vectors
- Finding and fixing hardcoded secrets
- Implementing secure coding best practices
- Applying defense-in-depth security principles

**[Start Lab 3 →](lab3/README.md)**

---

### 🟡 Lab 4: Bob v2 in Action — The Bookmarks Feature (30 minutes)

**Perfect for:** Developers who want to see Bob v2's new capabilities in a concrete, full-stack feature build

Build a persistent Bookmarks feature into the **RepoRadar** app — a React + Flask + SQLite codebase — and experience what makes Bob v2 different from v1.

**What you'll build:**

- A `Bookmark` SQLAlchemy model and SQLite table
- Three new REST API endpoints (`GET`, `POST`, `DELETE /api/bookmarks`)
- A live bookmark toggle button on every repo card
- A sidebar panel displaying and managing saved bookmarks
- A pytest test suite written by a background subagent

**Bob v2 features you'll see in action:**

- ✅ **Parallel tool calls** — Bob reads multiple files simultaneously instead of sequentially
- ✅ **Subagents** — a background agent writes tests while the main agent implements the feature
- ✅ **Todo tracking** — live checklist showing exactly what's done, in progress, and pending
- ✅ **Workflows** — the built-in Create PR workflow and a custom `/health-check` command
- ✅ **Fewer interruptions, same control** — Bob acts autonomously on safe changes, gates on risky ones

**[Start Lab 4 →](lab4/README.md)**

---

### 🔵 Lab 5: Bob as Your Java Modernization Partner (35–45 minutes)

**Perfect for:** Enterprise Java and SAP developers who want to see Bob as a full SDLC partner, not just a code autocomplete tool

Modernize a legacy Java 8 inventory service to Java 17 — complete with tests, CI/CD, containerization, and a live security audit — all in a single Bob session.

**What you'll modernize:**

- `InventoryItem.java` — convert a 96-line POJO to a 3-line Java record
- `InventoryService.java` — replace for-loops with Stream API, `Date` with `LocalDateTime`
- `InventoryController.java` — remove raw `HashMap` error responses, use `var` for type inference
- `application.properties` — externalize hardcoded credentials to environment variables
- Add a GitHub Actions CI pipeline (build, secret scan, Docker) and a multi-stage Dockerfile

**Bob v2 features you'll see in action:**

- ✅ **Custom modes** — switch Bob to a "Java Architect" persona with Java 17 best practices built in
- ✅ **Skills** — load a `java-modernization` playbook before touching any code
- ✅ **Parallel subagents** — Security Auditor and Test Engineer run simultaneously while migration continues
- ✅ **Lifecycle hooks** — a `check-secrets.sh` hook *blocks* Bob from writing hardcoded passwords to disk
- ✅ **General-purpose MCP** — Bob fetches live Spring Boot migration docs from spring.io
- ✅ **Full SDLC** — assess → migrate → test → CI/CD → containerize → PR in one session

**Additional prerequisites for Lab 5:**

- Java 17 JDK (`java -version` should show 17+)
- Maven 3.9+ (`mvn -version`)
- Docker *(optional, for the Dockerfile demo)*

**[Start Lab 5 →](lab5/README.md)**

---

## 🗺️ Choose Your Lab

**Pick the lab that interests you most!** Each lab is designed to be completed independently in about 45-60 minutes.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Prerequisites                                  │
│                     Check software requirements                          │
│                           (5-10 minutes)                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
        ┌──────────┬───────────────┴───────────────┬──────────┐
        ↓          ↓               ↓               ↓          ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Lab 1:     │ │   Lab 2:     │ │   Lab 3:     │ │   Lab 4:     │ │   Lab 5:     │
│   BYOC       │ │   Todo App   │ │   Security   │ │  Bookmarks   │ │    Java      │
│              │ │              │ │              │ │              │ │Modernization │
│ Explore      │ │ Beginner     │ │ Advanced     │ │  Bob v2      │ │ Enterprise   │
│ Freely       │ │ Structured   │ │ Security     │ │  Features    │ │   Java       │
│              │ │              │ │              │ │              │ │              │
│ 30-45 min    │ │ 45 min       │ │ 45 min       │ │ 30 min       │ │ 35-45 min    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
        ↓          ↓               ↓               ↓          ↓
        └──────────┴───────────────┴───────────────┴──────────┘
                                    ↓
                        Apply to Your Projects!
```

### Which Lab Should You Choose?

- **Want to explore freely?** → Lab 1 (BYOC) — build what interests you
- **Prefer structured learning?** → Lab 2 (Beginner) — follow step-by-step
- **Interested in security?** → Lab 3 (Advanced) — learn vulnerability detection
- **Want to see Bob v2's new features?** → Lab 4 (Bookmarks) — subagents, parallel calls, workflows
- **Enterprise Java / SAP developer?** → Lab 5 (Java Modernization) — full SDLC with Bob

**Note:** Labs are independent — pick one and dive in! No need to complete them in order.

---

## 📋 Prerequisites

Before starting these labs, ensure you have:

### Required Software

- **Python 3.8+** — [Download](https://www.python.org/downloads/)
- **Node.js 18+** — [Download](https://nodejs.org/) *(required for Labs 2, 4, 5)*
- **Git 2.x+** — [Download](https://git-scm.com/)
- **Bob IDE** — Installed and configured
- **Text Editor** — VS Code recommended (if not using Bob exclusively)

#### Additional prerequisites for Lab 5 only

- **Java 17 JDK** — [Download](https://adoptium.net/)
- **Maven 3.9+** — [Download](https://maven.apache.org/download.cgi)
- **Docker** *(optional)* — for the containerization demo

### Required Knowledge

- Basic command line usage (cd, ls, running commands)
- Basic understanding of files and directories
- Willingness to learn and experiment!

### Optional (Helpful but not required)

- Basic Python syntax
- Basic HTML/CSS/JavaScript
- REST API concepts
- Git basics

**For detailed setup instructions and lab-specific requirements, see [prerequisites.md](prerequisites.md).**

---

## 🎓 What You'll Learn

### Bob's Core Features

- **Multiple Modes**: Plan, Code, Ask, and custom modes for different tasks
- **Parallel Tool Calls**: Bob reads and writes multiple files simultaneously
- **Subagents**: Delegate self-contained tasks to background agents while you continue working
- **Auto-approvals**: Rapid development with automated confirmations
- **Literate Coding**: Self-documenting code with inline explanations
- **Security Features**: `.bobignore`, custom rules, and lifecycle hooks for secure development
- **Workflows**: Built-in and custom `/command` sequences for repeatable multi-step tasks
- **MCP Servers**: General-purpose tool connections (e.g. live web fetch)
- **Code Analysis**: Understanding and improving existing codebases

### Technical Skills

- Full-stack web development (Python Flask + JavaScript)
- REST API design and implementation
- Security best practices (SQL injection prevention, secrets management)
- Secure coding patterns
- AI-assisted development workflows

### Best Practices

- Effective prompting techniques
- Iterative development with AI
- Security-first development
- Code review and quality assurance
- Documentation and maintainability

---

## ✅ Success Criteria

You'll know you've successfully completed the labs when you can:

### After Lab 1 (BYOC)

- [ ] Effectively prompt Bob for your specific needs
- [ ] Switch between Bob's different modes
- [ ] Build a working prototype quickly
- [ ] Iterate on ideas with AI assistance

### After Lab 2 (Beginner)

- [ ] Use Plan Mode for architecture decisions
- [ ] Use Code Mode for implementation
- [ ] Apply auto-approvals safely
- [ ] Build full-stack applications with Bob
- [ ] Integrate version control

### After Lab 3 (Advanced)

- [ ] Identify common security vulnerabilities
- [ ] Use `.bobignore` to protect sensitive files
- [ ] Create custom security rules
- [ ] Implement defense-in-depth security
- [ ] Apply secure coding practices

### After Lab 4 (Bookmarks / Bob v2)

- [ ] Observe parallel tool calls firing simultaneously in the tool trace
- [ ] Spawn a background subagent for a self-contained task
- [ ] Read Bob's live todo checklist to track autonomous progress
- [ ] Run a custom `/health-check` workflow
- [ ] Generate a PR description (or create a PR via the built-in workflow)

### After Lab 5 (Java Modernization)

- [ ] Switch Bob into a custom Java Architect mode
- [ ] Activate a skill to pre-load domain knowledge before coding
- [ ] Run parallel subagents (Security Auditor + Test Engineer) simultaneously
- [ ] Witness a lifecycle hook block Bob from writing hardcoded credentials
- [ ] Generate a complete GitHub Actions CI pipeline from a single prompt
- [ ] Use the fetch MCP to pull live documentation into Bob's context

---

## 🆘 Getting Help

### During the Labs

Each lab includes:

- Step-by-step instructions
- Example prompts to use with Bob
- Troubleshooting sections
- Common issues and solutions

### If You Get Stuck

1. **Check the troubleshooting section** in the lab README
2. **Use Bob's Ask Mode** to get explanations
3. **Review the prerequisites** to ensure everything is installed
4. **Start fresh** - sometimes it helps to begin a step again

### Common Issues

**Bob isn't responding as expected:**

- Make sure you're in the correct mode (Plan, Code, or Ask)
- Try rephrasing your prompt more specifically
- Check if Bob needs more context about your goal

**Code isn't working:**

- Verify all dependencies are installed
- Check that you're in the correct directory
- Review error messages carefully
- Ask Bob to explain the error

**Installation problems:**

- See [prerequisites.md](prerequisites.md) for detailed setup
- Verify software versions match requirements
- Check system compatibility

---

## 🎉 What's Next?

After completing these labs, you can:

### Apply to Real Projects

- Use Bob on your own development work
- Apply security practices to your applications
- Build prototypes quickly
- Improve existing codebases

### Explore Advanced Features

- Create custom Bob modes for your team
- Integrate Bob into CI/CD pipelines
- Build custom MCP servers
- Develop team-specific rules and guidelines

### Share Your Experience

- Help others learn Bob
- Share your projects
- Contribute improvements to these labs
- Document your own best practices

---

## 📖 Additional Resources

### Documentation

- [Prerequisites & Setup](prerequisites.md) — Detailed installation and setup
- [Lab 1: BYOC](lab1/README.md) — Bring your own use case
- [Lab 2: Building Apps](lab2/README.md) — Beginner full-stack development
- [Lab 3: Security](lab3/README.md) — Advanced security analysis and fixes
- [Lab 4: Bookmarks / Bob v2](lab4/README.md) — Subagents, parallel calls, workflows
- [Lab 5: Java Modernization](lab5/README.md) — Enterprise Java SDLC with Bob

---

## 🤝 Contributing

Found an issue or have a suggestion? We welcome contributions!

- Report bugs or issues
- Suggest improvements
- Share feedback about the labs
- Help other learners

---

## 📝 Lab Completion Tracking

Track your progress through the labs:

- [ ] **Lab 1**: Bring Your Own Use Case
- [ ] **Lab 2**: Building Applications
- [ ] **Lab 3**: Security Analysis
- [ ] **Lab 4**: Bookmarks Feature (Bob v2)
- [ ] **Lab 5**: Java Modernization

---

## 💡 Tips for Success

### Before You Start

1. ✅ Verify all prerequisites are installed
2. ✅ Read through the lab overview
3. ✅ Set aside uninterrupted time
4. ✅ Have a notepad ready for notes

### During the Labs

1. 🎯 Follow the steps in order
2. 💬 Read Bob's responses carefully
3. 🧪 Test frequently as you build
4. 📝 Take notes on what you learn

### After Each Lab

1. 🎉 Celebrate your progress!
2. 📊 Review what you built
3. 🤔 Reflect on what you learned
4. 🚀 Think about how to apply it

---

## ⏱️ Time Commitment

- **Lab 1**: 30–45 minutes (flexible)
- **Lab 2**: 45 minutes
- **Lab 3**: 45 minutes
- **Lab 4**: 30 minutes
- **Lab 5**: 35–45 minutes
- **All labs**: ~3.5 hours (including breaks)

**Tip:** Take a 5-minute break between labs to stay fresh!

---

## 🎯 Ready to Begin?

1. ✅ Repository cloned
2. ✅ Opened in Bob
3. ✅ Prerequisites checked
4. ✅ Lab chosen

**Let's get started!**

- [Lab 1: Bring Your Own Use Case →](lab1/README.md)
- [Lab 2: Building Applications →](lab2/README.md)
- [Lab 3: Security Analysis →](lab3/README.md)
- [Lab 4: Bookmarks Feature (Bob v2) →](lab4/README.md)
- [Lab 5: Java Modernization →](lab5/README.md)

---

**Happy Learning! 🚀**

_Last Updated: July 2025_
