# MoneyLens User Manual

Welcome to MoneyLens! This guide helps you configure and use the personal finance system.

## 1. Quick Setup
1. Open the signup page (`register.html`) and register a new user.
2. Log in using `login.html`.
3. You will be redirected to the main dashboard page.

## 2. Tracking Expenses Manual vs Automated
- **Manual Input**: Select "Log Transaction" from the top navigation or sidebar. Populate amount, type, date, description, and upload transaction receipts (e.g. photo of store invoice).
- **Automated Ingestion (SMS)**: 
  1. Set up an SMS forwarder app on your Android or iOS phone.
  2. Map forward conditions to forward matching text messages from banking institutions.
  3. Route the POST webhook requests to `http://localhost:5000/api/sms/webhook`.
  4. Include custom header `X-SMS-Gateway-Key` holding your API authentication key.

## 3. Controlling Spending
- Select **Budgets** from sidebar navigation.
- Set category, target monthly allocation limit, and dates.
- Watch progress bars. If spent amount exceeds 80%, yellow warnings trigger. At 100%, alerts flash.
