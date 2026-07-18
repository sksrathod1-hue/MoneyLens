# API Documentation - MoneyLens

All endpoints are hosted at prefix `/api` (default port `5000`).

## 1. Authentication
### `POST /auth/register`
Creates user profile and default categories.
- **Payload**: `{"username": "name", "email": "user@mail.com", "password": "securepwd"}`
- **Response**: `211 Created` on success.

### `POST /auth/login`
Checks credentials and returns access token.
- **Payload**: `{"username": "name", "password": "securepwd"}`
- **Response**: `200 OK` with `{"access_token": "JWT_TOKEN", "user": {...}}`

---

## 2. Transactions
### `GET /transactions`
List user transactions. Supports filters `?type=expense` and `?category_id=X`.
- **Headers**: `Authorization: Bearer JWT_TOKEN`
- **Response**: `200 OK` with lists.

### `POST /transactions`
Log a transaction.
- **Payload**: `{"amount": 10.50, "type": "expense", "category_id": 1, "date": "2026-07-16", "description": "Coffee"}`
- **Response**: `201 Created`.

---

## 3. Budgets
### `GET /budgets`
Get budgets with computed `spent` details.

### `POST /budgets`
Set target limit.
- **Payload**: `{"category_id": 2, "amount": 500, "start_date": "2026-07-01", "end_date": "2026-07-31"}`

---

## 4. SMS Integration Webhook
### `POST /sms/webhook`
SMS forwarder callback webhook.
- **Headers**: `X-SMS-Gateway-Key: SECRET_GATEWAY_KEY`
- **Payload**: `{"body": "Debited Rs. 50 at Coffee House", "sender": "BANK-TX", "user": "demo"}`
- **Response**: `201 Created` with logged transaction object.
