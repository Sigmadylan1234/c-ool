from flask import Flask, render_template_string, request, redirect
import json
import datetime
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Book collection
books = [
    {"title": "The Dark Forest", "id": 1},
    {"title": "1984", "id": 2},
    {"title": "Brave New World", "id": 3},
    {"title": "Frankenstein", "id": 4}
]

# Email config
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"  # Use an app password if 2FA is on
TO_EMAIL = "to_email@gmail.com"

def send_email_notification(book_title, ip):
    msg = EmailMessage()
    msg['Subject'] = f"📖 Book Clicked: {book_title}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg.set_content(f"The book '{book_title}' was clicked by IP address: {ip}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Email sent for book '{book_title}' clicked by {ip}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# HTML Template
template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Book Collection</title>
</head>
<body>
    <h1>📚 Book Collection</h1>
    <ul>
        {% for book in books %}
            <li><a href="/book/{{book.id}}">{{book.title}}</a></li>
        {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(template, books=books)

@app.route('/book/<int:book_id>')
def book_clicked(book_id):
    user_ip = request.remote_addr
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        # Log the click with IP and timestamp
        log = {
            "book": book["title"],
            "ip": user_ip,
            "timestamp": datetime.datetime.now().isoformat()
        }
        with open("click_log.json", "a") as f:
            f.write(json.dumps(log) + "\n")

        # Send email notification
        send_email_notification(book["title"], user_ip)

    return redirect("/")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
