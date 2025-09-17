FROM python:3.13.2-slim 
WORKDIR /app 
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["streamlit", "run", "app/main.py"]
