FROM python:3.5

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "check_sites_health.py", "/data/sites.txt"]