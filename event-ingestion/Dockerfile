FROM python:3.12
#
WORKDIR /code
#
COPY ./requirements.txt /code/requirements.txt
#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN mkdir -p /code/app
COPY ./main.py /code/app
COPY ./main.py /code/app

#
EXPOSE 3205
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3205"]