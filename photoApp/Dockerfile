FROM mysql/mysql-server:latest 
#comes with python3.6.8

ENV MYSQL_ROOT_PASSWORD password
ENV MYSQL_DATABASE photoDB 
ENV MYSQL_USER user
ENV MYSQL_PASSWORD photoPassword
#RUN chmod 755 /docker-entrypoint-initdb.d/docker-entrypoint.sh
EXPOSE 3306
ADD . /home/ImageLibrary/photoApp

#RUN pip3 install  --upgrade pip && \
#    pip3 install -r /home/ImageLibrary/photoApp/requirements.txt
RUN pip3 install  --upgrade pip    
RUN pip3 install -r /home/ImageLibrary/photoApp/requirements.txt
#files here get executed on start up
ADD setup.sql /docker-entrypoint-initdb.d 


#FROM ubuntu

#Install packages
#RUN apt-get -y update
#RUN apt-get -y install mysql-server
#RUN mysql_secure_installation
#RUN apt-get -y install python3.7
