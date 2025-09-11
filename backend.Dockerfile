FROM python:3.12-slim

WORKDIR /app

COPY ./flask_app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./flask_app ./

EXPOSE 80

# Run Flask directly on port 80
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=80"]
