# Database Design - MoneyLens

## Schema Diagram (ERD Representation)

- **users**
  - `id` (PK, INTEGER, AUTOINCREMENT)
  - `username` (VARCHAR, UNIQUE, NOT NULL)
  - `email` (VARCHAR, UNIQUE, NOT NULL)
  - `password_hash` (VARCHAR, NOT NULL)
  - `created_at` (TIMESTAMP)

- **categories**
  - `id` (PK, INTEGER, AUTOINCREMENT)
  - `user_id` (FK -> users.id, NULLABLE) -- NULL indicates standard default categories
  - `name` (VARCHAR, NOT NULL)
  - `type` (VARCHAR, NOT NULL) -- 'income' or 'expense'
  - `icon` (VARCHAR)
  - `color` (VARCHAR)
  - `is_default` (BOOLEAN)

- **transactions**
  - `id` (PK, INTEGER, AUTOINCREMENT)
  - `user_id` (FK -> users.id, NOT NULL)
  - `category_id` (FK -> categories.id, NOT NULL)
  - `amount` (DECIMAL, NOT NULL)
  - `type` (VARCHAR, NOT NULL) -- 'income' or 'expense'
  - `description` (TEXT)
  - `date` (DATE, NOT NULL)
  - `sms_sender` (VARCHAR)
  - `receipt_image_path` (TEXT)

- **budgets**
  - `id` (PK, INTEGER, AUTOINCREMENT)
  - `user_id` (FK -> users.id, NOT NULL)
  - `category_id` (FK -> categories.id, NOT NULL)
  - `amount` (DECIMAL, NOT NULL)
  - `spent` (DECIMAL)
  - `period` (VARCHAR) -- 'monthly', 'weekly', 'yearly'
  - `start_date` (DATE)
  - `end_date` (DATE)

- **notifications**
  - `id` (PK, INTEGER, AUTOINCREMENT)
  - `user_id` (FK -> users.id, NOT NULL)
  - `title` (VARCHAR)
  - `message` (TEXT)
  - `type` (VARCHAR)
  - `is_read` (BOOLEAN)

- **ai_insights**
  - `id` (PK, INTEGER, AUTOINCREMENT)
  - `user_id` (FK -> users.id, NOT NULL)
  - `title` (VARCHAR)
  - `insight` (TEXT)
  - `category` (VARCHAR)
