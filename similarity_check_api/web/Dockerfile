FROM python:3
WORKDIR user/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install ./en_core_web_sm-2.2.5.tar.gz
CMD ["python", "app.py"]