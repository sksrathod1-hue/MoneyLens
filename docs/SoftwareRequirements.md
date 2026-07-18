# Software Requirements Specification (SRS) - MoneyLens

## 1. Functional Requirements
- **FR1. Registration & Authentication**: Users can sign up with username, email, and password. Access token handles protected API routes.
- **FR2. Transaction Logging**: Users can log transactions manually (amount, category, type, description, date, and receipt file upload).
- **FR3. Automated SMS Webhook**: An API route `/api/sms/webhook` parses SMS payloads sent by mobile forwarders, matching them to an active user.
- **FR4. Category Budgets**: Users can set target spending limits per category. Systems must compute alerts when spent reaches 80% or 100%.
- **FR5. Analytics Reports**: Charts showing category percentage splits, income vs expense comparison, and past six-month trend lines.
- **FR6. AI Wealth Insights**: An advice generator displaying patterns recommendations (low savings warnings, high category concentration).

## 2. Non-Functional Requirements
- **NFR1. Security**: Passwords stored hashed using bcrypt. API calls require Bearer JWT.
- **NFR2. Performance**: Server must respond under 300ms for static operations. Webhook parser must execute under 500ms.
- **NFR3. UX Aesthetics**: Dark interface with modern Outfit/Inter typography, responsive layouts, hover feedback, and clear warning states.
