# 🚀 Compiler Design Mini Project
## Advanced SQL-Like Query Language Compiler

A Python-based SQL-Like Query Language Compiler developed as part of the Compiler Design Mini Project. This application demonstrates the fundamental phases of compiler design through an interactive web interface built using Streamlit.

The compiler accepts SQL-like queries, processes them through different compilation phases, identifies errors, and generates an Abstract Syntax Tree (AST).

---

## 📌 Project Overview

The main objective of this project is to understand how a compiler processes and validates a query through multiple stages.

The application implements three major compiler phases:

1. **Lexical Analysis (Lexer):** Converts the input query into meaningful tokens such as keywords, identifiers, operators, numbers, and symbols.
2. **Syntax Analysis (Parser):** Checks whether the query follows the defined grammar rules and generates an Abstract Syntax Tree (AST).
3. **Semantic Analysis:** Performs logical validation, including duplicate column detection and basic schema validation.

---

## ✨ Key Features

- Lexical Analysis and Token Generation
- Syntax Analysis and Grammar Validation
- Semantic Analysis and Error Detection
- Abstract Syntax Tree (AST) Generation
- Support for SELECT, FROM, WHERE, and ORDER BY clauses
- Comparison operators such as `>`, `<`, `=`, `>=`, `<=`, and `!=`
- ASC and DESC sorting support
- Duplicate column detection
- Interactive Streamlit-based User Interface
- Compilation status and token count
- Compilation time measurement
- Error handling for invalid queries

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web-based user interface |
| Regular Expressions (Regex) | Token identification |
| JSON | AST representation |
| Git & GitHub | Version control and project hosting |

---

## 📂 Project Structure

```text
CompilerDesign-MiniProject/
│
├── cdApp.py
│   └── Main compiler application
│
├── requirements.txt
│   └── Required Python dependencies
│
├── SQL_Compiler_Mini_Project_Report.pdf
│   └── Final project report
│
└── README.md
    └── Project documentation
```

---

## 💻 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rachit-barapatre/CompilerDesign-MiniProject.git
```

### 2. Navigate to Project Directory

```bash
cd CompilerDesign-MiniProject
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run cdApp.py
```

The application will open in your default web browser.

---

## 📝 Sample SQL Queries

**1. Basic SELECT Query**

```sql
SELECT name, age, city FROM students;
```

**2. WHERE Condition**

```sql
SELECT name, age FROM students WHERE age >= 21;
```

**3. ORDER BY Ascending**

```sql
SELECT name, age FROM students ORDER BY age ASC;
```

**4. ORDER BY Descending**

```sql
SELECT name, age FROM students ORDER BY age DESC;
```

**5. Combined SQL Query**

```sql
SELECT name, age, city
FROM students
WHERE age >= 21
ORDER BY age DESC;
```

---

## ⚙️ Compilation Workflow

```text
SQL Query Input
      |
      v
Lexical Analysis
      |
      v
Token Generation
      |
      v
Syntax Analysis
      |
      v
AST Generation
      |
      v
Semantic Analysis
      |
      v
Compilation Result
```

---

## 📊 Application Output

The application displays:

- Generated Token Stream
- Abstract Syntax Tree (AST)
- Compilation Status
- Total Number of Tokens
- Compilation Time
- Lexical, Syntax, and Semantic Errors

---

## ⚠️ Project Limitations

This is an academic compiler frontend prototype. It validates SQL-like queries according to its implemented grammar but does not execute queries against an actual database.

Advanced SQL features such as JOIN, GROUP BY, and multiple WHERE conditions are not currently implemented.

---

## 🎯 Project Objective

To demonstrate the working principles of compiler design by implementing lexical, syntactic, and semantic analysis in Python and presenting the compilation process through an interactive web application.

---

## 👨‍💻 Author

**Rachit Barapatre**

Compiler Design Mini Project

GitHub: [rachit-barapatre](https://github.com/rachit-barapatre)

---

## 📄 License

This project is developed for academic and educational purposes.