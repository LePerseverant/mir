FROM python:3.11-alpine

WORKDIR /flask-api

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP  ./project
CMD [ ".", "./.venv/bin/activate"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]


EXPOSE 5000
