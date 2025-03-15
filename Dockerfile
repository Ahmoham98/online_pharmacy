FROM python:latest
WORKDIR /app
ADD . .
RUN pip install --upgrade pip
RUN pip install "fastapi[standard]"
RUN pip install sqlmodel
RUN pip install pydantic
RUN pip install bcrypt
RUN pip install jwt

CMD [ "fastapi", "dev", "main.py" ]
