FROM python:3.10.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

WORKDIR /bot

COPY . /bot

RUN pip install --upgrade pip  
RUN pip install -r requirements.txt

CMD python main.py