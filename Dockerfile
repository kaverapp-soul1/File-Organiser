FROM python:3.11
WORKDIR /app

COPY . .

#Do not save the downloaded packages to pip’s local cache.-->--no-cache-dir

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD [ "streamlit", "run", "server.py"]
