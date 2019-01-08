FROM python:3.7.2
WORKDIR /usr/app
ADD . /usr/app
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "main_page/fastQA.py"]