FROM python:3.6-stretch

WORKDIR /var/gdtb

COPY app/ /var/gdtb/app
COPY connectors/ /var/gdtb/connectors
COPY wapi.py /var/gdtb/wapi.py

COPY requirements.txt /var/gdtb/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python" ]