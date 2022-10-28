FROM python:3.8-slim-buster

WORKDIR /dashboard

COPY dashboard/requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=dashboard/dashboard.py

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]