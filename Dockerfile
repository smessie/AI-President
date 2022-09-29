FROM python:3.9.14-slim-bullseye

COPY requirements.txt .

ENV PIP_NO_CACHE_DIR=false
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "main_discord.py" ]
