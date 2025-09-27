🎥 Movies Store – Django Web Application

Movies Store is a full-stack Django web application that lets users browse movies, view details, write reviews, manage a shopping cart, and complete purchases. The project demonstrates a production-style MVC architecture with authentication, persistence, and a modern, custom-themed UI.

This project is designed as both a portfolio showcase and a practical demonstration of building a modular, scalable web application from scratch.

⸻

✨ Features
- 🔑 **User Authentication & Accounts**
  - Sign up, login, logout
  - **Forgot Password with Security Question & Answer**
  - Manage personal orders & reviews  

- 🎬 **Movies App**
  - Browse a curated movie catalog
  - View detailed pages with images, pricing, and reviews
  - Post, edit, and manage reviews  

- 🛒 **Cart & Orders**
  - Add/remove movies from the cart
  - Calculate totals automatically
  - Purchase flow with order tracking
  - Orders page with modern table design & hover effects  

- 📢 **Petitions App (New)**
  - Create petitions to suggest new movies for the store  
  - Vote **Yes/No** on petitions made by other users  
  - Live vote counts + ability to edit your vote  
  - Petitions are displayed and ordered by popularity (most votes shown first)  

- 🏠 **Home App**
  - Landing page with trending movies
  - “About” section with custom branding and visuals  

- 🎨 **Custom UI/UX Theme**
  - Gradient buttons & input fields
  - Hover animations on cards and tables
  - Gradient-border cards for Orders & Auth pages
  - Responsive, recruiter-ready design  

⸻

⸻

🏗 Architecture
<img width="703" height="508" alt="Screenshot 2025-09-07 at 10 37 04 AM" src="https://github.com/user-attachments/assets/5c22f783-9e5d-489f-a4d6-b9810c6c0a57" />
- Modular Django apps:
  - `home/` → landing & about
  - `movies/` → movie catalog & reviews
  - `cart/` → shopping cart & purchase flow
  - `accounts/` → authentication, orders, **security questions**
  - `petitions/` → user-created movie petitions & voting
- Views → Templates Flow  
  Each app has its own `views.py`, `urls.py`, and `templates/` folder for separation of concerns.  

- Models
  - **Movies App**
    - `Movie`: stores title, description, price, and image
    - `Review`: linked to a Movie and User
  - **Cart App**
    - `Order`: represents a purchase session
    - `Item`: links an Order to a Movie with quantity & price
  - **Accounts App**
    - Extends Django’s `User` with security question & answer
  - **Petitions App**
    - `Petition`: user-submitted requests for new movies
    - `PetitionVote`: tracks Yes/No votes by users  

⸻

📊 Database Design
<img width="807" height="416" alt="Screenshot 2025-09-06 at 11 42 00 AM" src="https://github.com/user-attachments/assets/d5fb8e4e-039d-4dd8-a126-6ace5413988d" />

Relational Schema (Django ORM):
- 1 User → many Orders
- 1 User → many Reviews
- 1 User → many Petitions
- 1 Petition → many PetitionVotes
- 1 Order → many Items
- 1 Movie → many Reviews
- 1 Movie → many Items

Tech: SQLite3 (development) using Django ORM.

🚀 Getting Started
1.Clone the Repository
git clone https://github.com/Joel-sari/JoelsMovieStore.git
cd JoelsMovieStore


2. Create & Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\\Scripts\\activate ****

3. Run Migrations
python manage.py migrate


4.Start Development Server
python manage.py runserver





