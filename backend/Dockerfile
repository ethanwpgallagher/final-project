# Backend Dockerfile
FROM python:3.7

WORKDIR /app

# Install API dependencies
COPY api/requirements.txt api/requirements.txt
RUN pip install --upgrade pip && pip install -r api/requirements.txt

# Install ML dependencies
COPY ml/requirements.txt ml/requirements.txt
RUN pip install --upgrade pip && pip install -r ml/requirements.txt

COPY ./ /app

# Expose ports if needed
EXPOSE 5000

CMD ["sh", "-c", "cd api && flask run --host=0.0.0.0"]
