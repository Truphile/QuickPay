FROM python:3.14.2

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies for Postgres
RUN apt-get update && apt-get
install -y libpq-dev gcc
--no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# prepare static files
RUN uv run manage.py collectstatic
--noinput

# Launch with gunicorn (QuickPay)
CMD ['gunicorn','--bind', '0.0.0.0:8000', 'QuickPay.wsgi:application']