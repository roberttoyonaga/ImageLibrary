# ImageLibrary 
This application is a simple image repository to practice using Docker, MySQL, and Python unittest. To start the application use `docker-compose up` from the root directory. 
This will create and run the docker image that initializes the MySQL database and python packages required by the application. To start using the application use `docker exec -it photoAppContainer python3 /home/ImageLibrary/photoApp/main.py` (prepend `sudo` if on linux). This has been tested on a host machine running ubuntu 18. This project uses Python3 and a MySQL database.

## Registering as a User
Once the application starts you will be prompted to either login with existing credentials or register as a new user. User credentials include a unique username and password that is hashed and kept in the Users table. 
Users will only be able to access images that they own. Images owned by other users will be inaccessible and kept secret from the active user.

When registering, there are two user types: `admin` and `individual`. Admins can search the database and add new images, but individuals can only seach the database. All users can change their password or delete their accounts.

For demonstration purposes, the repository is initialized with an `admin` user: `default_user` and password: `password_1`. This user already owns some images in the repository.

## Seaching for Images
Users can search for images using two methods: by name or by tags. Users cannot search for and will not be shown images belonging to other users.

When searching by name, the user can ask for a list of photos they have access to. They then provide the name of the photo they want to retrieve. 

When seaching by tags, users can provide a list of tags. All images matching the desired tags will be output (if the active user has access permissions to them)

Images are output to `images/results_Current_Time`.
## Adding new Images
Admin users can add new images using two methods: From their local machine, or from the internet. Images will be added to `images/collection`. When adding an image, users can choose to add tags as well. Images added from a local machine should be added from the mounted docker container volume. For simplicity, images can be first dropped into the `images/images_to_add` folder. This is not ideal, but it allows for an easy transfer of files between the docker container and the host machine's filesystem.

## Testing
Unit tests can be found in `photoApp/test_photoApp.py` and can be run using `docker exec -it photoAppContainer python3 -m unittest /home/ImageLibrary/photoApp/test_photoApp.py` (prepend `sudo` if on linux).


