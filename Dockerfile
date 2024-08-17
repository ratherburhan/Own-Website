# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Environment Variables
ENV FLASK_KEY=8BYkEfBA6O6donzWlSihBXox7C0sKR6bfgt5dc
ENV DB_URI=postgresql://blog_db_9fdb_user:37FX6FdukkHAztSZmZ0BJ54GlUv5hJTx@dpg-cn8dcsqcn0vc738mc34g-a.singapore-postgres.render.com/blog_db_9fdb
ENV company_mail=info@wanderwelltravels.in
ENV server_token=91593d8b-0ab1-4ae6-99da-6c4a3dbff0de
ENV sender_mail=mailtrap@wanderwelltravels.in
ENV token_mail=9e7698da93522a1d23b99d592f82b63b

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]