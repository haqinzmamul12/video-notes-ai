FROM python:3.13.2-slim 
WORKDIR /app 
COPY . . 
ENV PYTHONPATH=/app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["streamlit", "run", "app/main.py"]
