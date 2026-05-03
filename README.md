# Expenses Custom

## 📌 Overview
This project customizes the Expenses module in Odoo by introducing a multi-stage approval workflow, role-based access control, and validation rules to improve expense management.
## 🎯 Features
- Multi-state workflow for expense reports
  <img width="1252" height="123" alt="Screenshot from 2026-05-03 19-05-44" src="https://github.com/user-attachments/assets/ced0e4b2-05f4-427c-9b11-66efc231366e" />
  
- Role-based access for each state using user groups
- State-specific permissions (who can view, edit, approve)
  <img width="550" height="557" alt="Screenshot from 2026-05-03 19-30-40" src="https://github.com/user-attachments/assets/9a689140-de9a-4d67-b058-7c1be0787618" />
  
- Custom validation to ensure data consistency before moving between states
  <img width="1220" height="694" alt="Screenshot from 2026-05-03 19-02-13" src="https://github.com/user-attachments/assets/930d8479-dabd-4ee6-b539-72abfcef7a61" />

- Views to match the customization
- A new wizard was added to recall the report even after cancellation or at any state.

## 🧩 Modules Included
- expenses_categories → Adding new fields like Expense Limit, where if checked, the Amount field appears to add the amount of this category; if this                         category exceeds this amount per year, it will raise a validation as mentioned above. The Approval Type field makes the                              report cross the approval state if it was HR or Reviewer
<img width="1751" height="716" alt="Untitled design" src="https://github.com/user-attachments/assets/c08c665a-7aa5-4f4a-ba8d-d959738c9853" />

- report → The main model that has all constrains,states, and validations 

