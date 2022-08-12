FROM python:3.8.6-slim
WORKDIR /app
COPY backend/ ./
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]