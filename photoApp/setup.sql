-- Clean out the old teefile; likely this command is system specific
\! rm -f outfile.txt
tee outfile.txt;

-- Show warnings after every statement
warnings;

use photoDB;

drop table if exists Country;

select '----------------------------------------------------------------' as '';
select 'Create Photos' as '';
create table Photos
(
  photoID int not null auto_increment,
  name varchar(50) not null,
  reference varchar(100) not null,
  sizeBytes int,
  captureDate datetime,
-- Constraints
  primary key (photoID)
);