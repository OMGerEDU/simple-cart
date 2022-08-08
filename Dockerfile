
FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]



#Docker file creationg: docker:
# docker build -t fileName .    # . stands for current folder.
# docker run -dp 5000:5000 fileName    # Select an open port.
# docker container ls # to check current running containers.
# docker container stop containerName #check container name with the above command.


