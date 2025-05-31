FROM python:3.9

WORKDIR /app

COPY . /app

# Create necessary directories
RUN mkdir -p /app/resumes /app/results

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
