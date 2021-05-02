FROM mysql/mysql-server:latest 
# comes with python3.6.8

ENV MYSQL_ROOT_PASSWORD password
ENV MYSQL_DATABASE photoDB 
ENV MYSQL_USER user
ENV MYSQL_PASSWORD photoPassword
EXPOSE 3306
# add the repo
ADD . /home/ImageLibrary/photoApp

# get python packages
RUN pip3 install  --upgrade pip    
RUN pip3 install -r /home/ImageLibrary/photoApp/requirements.txt

# files here get executed on start up
ADD setup.sql /docker-entrypoint-initdb.d 
