<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=160&section=header&text=Online%20Banking%20API&fontSize=36&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Flask%20%7C%20JWT%20%7C%20Repository-Service%20Architecture&descAlignY=58&descSize=15)

**A RESTful backend for online banking — accounts, transactions, fund transfers, and role-based access — built with Flask, following clean Repository-Service layer architecture.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)

</div>

---

<img align="right" width="280" src="https://raw.githubusercontent.com/TheDudeThatCode/TheDudeThatCode/master/Assets/Developer.gif" alt="Developer GIF">

## 📖 About

This project is an online banking backend exposing core banking resources — **Users, Accounts, Transactions, Fund Transfers, Beneficiaries, Cards, Auth Sessions,** and **Audit Logs** — with JWT-based authentication and role-based access control (`ADMIN`, `MANAGER`, `CUSTOMER_SUPPORT`, `EMPLOYEE`, `CUSTOMER`). It follows a layered architecture that separates concerns cleanly:

```
Route  →  Service  →  Repository  →  Model
```

- **Route** — handles HTTP requests/responses
- **Service** — business logic and validation
- **Repository** — database queries
- **Model** — SQLAlchemy ORM schema

## ✨ Features

- Role-based user registration & login (Admin / Manager / Customer Support / Employee / Customer)
- JWT authentication for protected routes
- Role-based authorization distinguishing bank staff (Manager, Customer Support) from Customers
- Account creation with system-generated account numbers (not customer-settable)
- Frozen snapshot of customer details (name, email, phone, address, DOB, KYC status) captured at account creation time, kept separate from the live users table
- Fund transfers between accounts and beneficiary management
- Card issuance and management
- Auth session tracking and audit logging
- Passwords hashed with Werkzeug security (never stored in plain text)

----

<img align="right" width="280" src="https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif" alt="Programmer">

## 🧰 Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Framework | Flask |
| ORM | Flask-SQLAlchemy |
| Auth | Flask-JWT-Extended |
| Database | MySQL (PyMySQL driver) |
| Config | python-dotenv |

## 📂 Project Structure

```
ONLINE_BANKING_API/
├── bank/
│   ├── model/
│   │   ├── users_model/         # admin.py, manager.py, customer_support.py, employee.py, customer.py
│   │   └── account_model/       # bank_account_create.py
│   ├── repository/              # DB access layer — repo pattern per role
│   ├── extensions/              # db.py, jwt.py — extension initializers
│   ├── config.py                # Environment-based configuration
│   └── main.py                  # App factory / entry point
├── requirements.txt
```

Each role (`admin`, `manager`, `customer_support`, `employee`, `customer`) is stored in its own dedicated database table rather than through shared-table inheritance, keeping role-specific data and access cleanly separated.

## 🏦 Core Schema

- **Users** — per-role tables for Admin, Manager, Customer Support, Employee, and Customer
- **Accounts** — `BankAccount` model with primary id, `user_id`, a snapshot of the customer's full name/username/email, and account type; the account number is system-generated
- **Transactions** — records of account activity
- **Fund Transfers** — money movement between accounts
- **Beneficiaries** — saved transfer recipients
- **Cards** — issued cards linked to accounts
- **Auth Sessions** — tracked login sessions
- **Audit Logs** — records of sensitive actions for traceability

## 🔐 Authentication Flow

1. Register via the role-appropriate registration endpoint
2. Log in to receive a JWT access token
3. Pass the token as a Bearer token in the `Authorization` header for protected routes:
   ```
   Authorization: Bearer <your_jwt_token>
   ```
4. Role-based decorators restrict certain routes to `ADMIN` / `MANAGER` / `CUSTOMER_SUPPORT` / `EMPLOYEE` roles, keeping bank staff actions separate from customer-facing ones

## 👤 Author
**Deslin Simon Thiboorcies**

## 📫 Connect With Me

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/deslin-simon-94615030b)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:deslinsimon01@gmail.com)

</div>

<div align="center">

</div>

![Footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=twinkling)