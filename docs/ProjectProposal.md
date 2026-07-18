# Project Proposal: MoneyLens

## Executive Summary
MoneyLens is a next-generation personal finance tracker that targets the friction of manual bookkeeping. By automatically processing bank SMS alerts, seeding dynamic visual dashboards, and leveraging rules or Large Language Models (LLMs) to advise users, MoneyLens provides an accessible portal into personal wealth management.

## Goals & Objectives
1. **Zero-friction ingestion**: Automatically parse incoming transaction SMS logs to register expenses.
2. **Actionable Budgeting**: Prevent overspending via responsive, automated categories limits.
3. **AI Advising**: Yield personalized tips regarding savings rates and expenditure concentration.
4. **Intuitive UX**: Deliver an aesthetically premium, responsive, glassmorphic layout.

## Scope of Work
- **Database Engine**: SQLite storing users, budgets, transactions, notifications, and insights.
- **REST Backend API**: Python Flask with JWT-extended auth session management.
- **Web Frontend**: Single-page-like vanilla HTML/CSS/JS with Chart.js analytics.
- **Webhook Gateway**: SMS webhook to capture and record background expense forwarders.
