🛒 Snapshop – E-Commerce Website (Flask + MongoDB)

Snapshop is a full-stack e-commerce web application built using Flask, MongoDB Atlas, HTML, CSS, and deployed on Render.
It allows users to browse products, view categories, manage a cart, and place orders with user authentication.

🚀 Features

User Registration & Login

Product Listing & Category Filtering

Product Detail Page with Similar Products

Add to Cart / Remove from Cart

Quantity Management

Order Placement

Responsive UI

MongoDB Atlas Cloud Database

Secure Environment Variables with .env

Deployed on Render using Gunicorn

🛠 Tech Stack

Backend: Flask (Python)

Database: MongoDB Atlas

Frontend: HTML, CSS, Jinja2

Server: Gunicorn

Deployment: Render

Environment Management: python-dotenv

📁 Project Structure
ecommerce_website/
│
├── app.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── cart.html
│   ├── category.html
│   ├── product.html
│   └── place_order.html
├── static/
│   ├── css/
│   └── img/
└── README.md

🔐 Environment Variables

Create a .env file:

MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/ecommerce
SECRET_KEY=your_secret_key

▶ Run Locally
pip install -r requirements.txt
python app.py


Open:
http://127.0.0.1:5000

☁ Deploy on Render

Push code to GitHub

Create Web Service on Render

Build Command:

pip install -r requirements.txt


Start Command:

gunicorn app:app


Add environment variables in Render:

MONGO_URI

SECRET_KEY

Allow IP 0.0.0.0/0 in MongoDB Atlas

👩‍💻 Author

Developed by Likhitha
Project: Snapshop – Easy Online Shopping Platform

📜 License

This project is for educational purposes.
