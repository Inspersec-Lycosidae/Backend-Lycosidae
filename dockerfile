FROM python:3.13-slim
WORKDIR /backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x ./uvicorn.sh
ENV PYTHONPATH=/backend/app
CMD ["/bin/bash", "./uvicorn.sh"]
