# 💸 Expense Tracker CLI

A simple yet powerful command-line expense tracker built with Python.
This project is part of a learning journey following roadmap.sh backend projects.

It supports basic CRUD operations, date-based filtering, and summary analytics, all stored locally using JSON.

---

## 🚀 Features

- Add expense with description and amount
- Delete expense by ID
- List all expenses in a clean table format
- Summary of total expenses
- Filter summary by:

  - Day
  - Month
  - Year

- Persistent storage using JSON
- Automatic ID indexing
- Basic error logging system

---

## 🛠️ Tech Stack

- Python 3.10+
- Pydantic (data validation)
- JSON (local storage)
- argparse (CLI interface)
- logging (error tracking)

---

## 📦 Installation

```bash
git clone https://github.com/your-username/expense-tracker-cli.git
cd expense-tracker-cli
```

No external dependencies required except Pydantic:

```bash
pip install pydantic
```

---

## ▶️ Usage

### Add Expense

```bash
python main.py add --description "Lunch" --amount 20
```

### List Expenses

```bash
python main.py list
```

### Delete Expense

```bash
python main.py delete --id 1
```

### Summary Total

```bash
python main.py summary
```

### Filter Summary

By Month:

```bash
python main.py summary --month 8
```

By Day:

```bash
python main.py summary --day 17
```

By Year:

```bash
python main.py summary --year 2026
```

Combined:

```bash
python main.py summary --day 17 --month 6 --year 2026
```

---

## 📁 Project Structure

```
.
├── main.py
├── expense_db.json
├── error.log
└── README.md
```

---

## ⚠️ Notes

- Amount must be numeric (integer)
- Data is stored locally in JSON format
- Deleting data cannot be undone
- This project is for learning purposes

---

## 🧠 What I Learned

- CLI design using argparse
- Data modeling with Pydantic
- File-based persistence
- Filtering and query logic
- Clean architecture separation (DB, logic, UI)
- Error handling using sys.excepthook

---

## 🔥 Future Improvements

- Transaction-safe file writing (atomic save)
- Query builder system (SQL-like filtering)
- Plugin-based command system
- Export to CSV / Excel
- Better CLI UX (colors, formatting)
- UUID-based IDs instead of incremental index

---

## 📜 License

MIT License — free to use for learning purposes.

---

> Built as part of backend learning journey from [roadmap.sh](https://roadmap.sh/projects/expense-tracker)
> Not production-ready, but evolving 🚀
> :::
