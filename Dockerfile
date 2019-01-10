FROM python:3.7.2
ADD . /usr/app
WORKDIR /usr/app
ENV PYTHONPATH=/usr/app
RUN pip install -r requirements.txt
EXPOSE 80
COPY . /
RUN ls -la /
CMD ["python", "main_page/fastQA.py"]