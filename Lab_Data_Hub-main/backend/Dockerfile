FROM python:3.10-slim
WORKDIR /app 
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . . 
CMD ["gunicorn", "lab_data_project.wsgi", "--bind", "0:8000" ]