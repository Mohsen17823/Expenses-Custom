# Expenses Custom

## 📌 Overview
This project customizes the Odoo 17 Expenses module by introducing a multi-stage approval workflow, role-based access control, and validation rules to improve expense management.
## 🎯 Features
### 🔄 Multi-state workflow
Implements a custom approval flow for expense reports.
<img width="1252" height="123" alt="Screenshot from 2026-05-03 19-05-44" src="https://github.com/user-attachments/assets/ced0e4b2-05f4-427c-9b11-66efc231366e" />
  
### 👥 Role-based access control
- Restricts actions based on user roles at each stage.
  
### 🔐 State-specific permissions
- Control who can view, edit, and approve per state
- Prevent unauthorized actions
  <img width="550" height="557" alt="Screenshot from 2026-05-03 19-30-40" src="https://github.com/user-attachments/assets/9a689140-de9a-4d67-b058-7c1be0787618" />
  
### ✅ Validation rules
- Prevent invalid state transitions
- Ensure required data is filled before approval
<img width="1220" height="694" alt="Screenshot from 2026-05-03 19-02-13" src="https://github.com/user-attachments/assets/930d8479-dabd-4ee6-b539-72abfcef7a61" />

### 🧭 UI Enhancements
- Customized views to match workflow
- Added wizard to recall reports from any state

## 🧩 Modules Included
### 📦 expenses_categories
- Adds Expense Limit per category
- Triggers validation if yearly limit is exceeded
- Defines Approval Type (HR / Finance)
<img width="1751" height="716" alt="Untitled design" src="https://github.com/user-attachments/assets/c08c665a-7aa5-4f4a-ba8d-d959738c9853" />

### 📦 expenses_report
- Core logic for:
  - Workflow states
  - Business validations
  - Constraints

## 🧠 What I Learned
- Extending standard Odoo modules using inheritance
- Designing multi-stage approval workflows
- Implementing record rules and user groups for access control
- Writing Python constraints for business validation
- Debugging access errors and workflow issues

