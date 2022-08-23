FROM python:3.7.13
 
WORKDIR /webhook_server

COPY ./* ./ 

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x entry.sh
ENTRYPOINT ["./entry.sh"]
