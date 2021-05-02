# ImageLibrary 
This application is a simple image repository. To start the application use `docker-compose up` from the root directory. 
This will create and run the docker image that initializes the MySQL database and python packages required by the application. To start using the application use `docker exec -it photoAppContainer python3 /home/ImageLibrary/photoApp/main.py`. This has been tested on a host machine running ubuntu 18.

## Registering as a User
Once the application starts you will be prompted to either login with existing credentials or register as a new user. 
Users will only be able to access images that they add the repo. Images owned by other users will be inaccessible and kept secret from the active user.

When registering, there are two user types: `admin` and `individual`. Admins can search the database and add new images, but individuals can only seach the database.

For demonstration purposes, the repository is initialized with a user: `default_user` and password: `password_1`. This already owns some images in the repository.
## Seaching for Images

## Adding new Images


