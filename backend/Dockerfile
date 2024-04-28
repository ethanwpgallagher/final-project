# Backend Dockerfile
FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libhdf5-dev  # Add the HDF5 library here

# Install API dependencies
COPY api/requirements.txt api/requirements.txt
RUN pip install --upgrade pip && pip install -r api/requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Install ML dependencies
COPY ml/requirements.txt ml/requirements.txt
RUN pip install --upgrade pip && pip install -r ml/requirements.txt

COPY ./ /app

# Expose ports if needed
EXPOSE 5000

CMD ["sh", "-c", "cd api && flask run --host=0.0.0.0"]
