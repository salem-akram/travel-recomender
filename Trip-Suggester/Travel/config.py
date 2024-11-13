class Config:
    SECRET_KEY = 'your_secret_key_here'  # Replace with your own secret key
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://username:password@localhost:5000/YourDatabase'  # Replace username, password, and database name
    SQLALCHEMY_ECHO = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'your_email@example.com'  # Replace with your email
    MAIL_PASSWORD = 'your_email_password_here'  # Replace with your email password
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    OPENAI_API_KEY = 'your_openai_api_key_here'  # Replace with your OpenAI API key
