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
-- Constraints
  unique(name),
  unique(reference),
  foreign key (ownerID) references Users(userID),
  primary key (photoID)
);
