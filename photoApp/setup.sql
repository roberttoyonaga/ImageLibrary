-- Clean out the old teefile; likely this command is system specific
\! rm -f outfile.txt
tee outfile.txt;

-- Show warnings after every statement
warnings;

use photoDB;

drop table if exists Photos;
drop table if exists Users;

select '----------------------------------------------------------------' as '';
select 'Create Users' as '';
create table Users
(
  userID int not null AUTO_INCREMENT,
  username varchar(20) not null,
  password varchar(20) not null,
  userType enum('admin', 'individual'),
  -- Constraints
  unique(username),
  primary key (userID)
);

select '----------------------------------------------------------------' as '';
select 'Create Photos' as '';
create table Photos
(
  photoID int not null auto_increment,
  name varchar(50) not null,
  reference varchar(100) not null,
  sizeBytes int,
  captureDate datetime,
  ownerID int not null,
  format varchar(3) not null,
-- Constraints
  check (format = "png" or format = "jpg"), -- only accept these formats for now
  unique(name),
  unique(reference),
  foreign key (ownerID) references Users(userID),
  primary key (photoID)
);

select '----------------------------------------------------------------' as '';
select 'Create Tags' as '';
create table Tags
(
  tagID int not null auto_increment,
  tagName varchar(50) not null,
-- Constraints
  unique(tagName),
  primary key (tagID)
);

select '----------------------------------------------------------------' as '';
select 'Create PhotoTags' as '';
create table PhotoTags
(
  tagID int not null ,
  photoID int not null,
-- Constraints
  unique(tagID,photoID),
  foreign key (tagID) references Tags(tagID),
  foreign key (photoID) references Photos(photoID)
);


-- add some data so our database isn't completely empty
INSERT INTO Users (username, password, userType) VALUES ("shopify", "challenge", "individual");
INSERT INTO Users (username, password, userType) VALUES ("robert", "toyonaga", "individual");

INSERT INTO Photos (name, reference, sizeBytes,captureDate,ownerID, format) 
VALUES ("dog", "/home/ImageLibrary/images/collection/dog.png", 19216, NULL,1, "png");

INSERT INTO Photos (name, reference, sizeBytes,captureDate,ownerID, format) 
VALUES ("flower", "/home/ImageLibrary/images/collection/flower.png", 62645, NULL,2, "jpg");

INSERT INTO Tags (tagName) VALUES ("dog");
INSERT INTO Tags (tagName) VALUES ("flower");
INSERT INTO Tags (tagName) VALUES ("life");

INSERT INTO PhotoTags (tagID,photoID) VALUES (1,1);
INSERT INTO PhotoTags (tagID,photoID) VALUES (2,2);
INSERT INTO PhotoTags (tagID,photoID) VALUES (3,1);
INSERT INTO PhotoTags (tagID,photoID) VALUES (3,2);