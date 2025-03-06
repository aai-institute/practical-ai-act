FROM python:3.12-slim

RUN pip install fastapi uvicorn plotly

ADD main.py main.py

CMD ["uvicorn", "--reload", "main:app", "--host", "0.0.0.0", "--port", "4040"]
