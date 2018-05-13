drop table if exists cardsets;
create table cardsets (
  id int(10) unsigned not null auto_increment,
  code varchar(8) not null,
  name varchar(50) not null,
  reldate date not null,
  type varchar(20),
  block varchar(50),
  primary key(id),
  index code_i(code)
) Engine=InnoDB DEFAULT CHARSET=utf8;

drop table if exists inventory;
create table inventory (
  id int unsigned not null auto_increment,
  cid varchar(40) not null,
  price decimal(8,2),
  cond tinyint(2) unsigned,
  indeck tinyint(1),
  isfoil tinyint(1),
  primary key(id),
  index icid(cid)
) Engine=InnoDB DEFAULT CHARSET=utf8;

drop table if exists cardcondition;
create table cardcondition (
  id tinyint unsigned not null primary key,
  condval char(2) not null,
  condext varchar(30)
) Engine=InnoDB DEFAULT CHARSET=utf8;

insert into cardcondition values(10,'NM','Near Mint');
insert into cardcondition values(20,'LP','Lightly Played');
insert into cardcondition values(30,'MP','Moderately Played');
insert into cardcondition values(40,'HP','Heavily Played');
insert into cardcondition values(50,'DM','Damaged');

drop table if exists cards;
create table cards (
  id int unsigned not null auto_increment,
  cid varchar(40) not null,
  layout varchar(20),
  name varchar(150) not null,
  manacost varchar(50),
  cmc decimal(9,2),
  type varchar(50),
  rarity varchar(20),
  ctext varchar(1024),
  ftext varchar(1024),
  artist varchar(128),
  num varchar(10),
  p varchar(6),
  t varchar(6),
  l varchar(6),
  mid int,
  imagename varchar(200),
  imgpath varchar(2000),
  setcode varchar(8) not null,
  primary key(id),
  index name_i(name),
  index cmc_i(cmc),
  index setcode_i(setcode),
  index cid(cid)
) Engine=InnoDB DEFAULT CHARSET=utf8;

drop table if exists rulings;
create table rulings (
  id int(10) unsigned not null auto_increment,
  cid varchar(40) not null,
  rdate date,
  rtext varchar(2048),
  primary key(id),
  index cid_i(cid)
) Engine=InnoDB DEFAULT CHARSET=utf8;

drop table if exists altnames;
create table altnames (
  id int(10) unsigned not null auto_increment,
  cid varchar(40) not null,
  name varchar(150) not null,
  primary key(id),
  index altcid(cid)
) Engine=InnoDB DEFAULT CHARSET=utf8;

drop table if exists colors;
create table colors (
  id int(10) unsigned not null auto_increment,
  cid varchar(40) not null,
  color varchar(50) not null,
  primary key(id),
  index ccid(cid),
  index color_i(color)
) Engine=InnoDB DEFAULT CHARSET=utf8;

drop table if exists colorids;
create table colorids (
  id int(10) unsigned not null auto_increment,
  cid varchar(40) not null,
  colorid varchar(10) not null,
  primary key(id),
  index cicid(cid),
  index colorid_i(colorid)
) Engine=InnoDB DEFAULT CHARSET=utf8;

drop table if exists cardtypes;
create table cardtypes (
  id int(10) unsigned not null auto_increment,
  cid varchar(40) not null,
  ctype varchar(50) not null,
  primary key(id),
  index ctcid(cid),
  index ctype_i(ctype)
) Engine=InnoDB DEFAULT CHARSET=utf8;

drop table if exists cardsupertypes;
create table cardsupertypes (
  id int(10) unsigned not null auto_increment,
  cid varchar(40) not null,
  csuptype varchar(50) not null,
  primary key(id),
  index ctcid(cid),
  index csuptype_i(csuptype)
) Engine=InnoDB DEFAULT CHARSET=utf8;

drop table if exists cardsubtypes;
create table cardsubtypes (
  id int(10) unsigned not null auto_increment,
  cid varchar(40) not null,
  csubtype varchar(50) not null,
  primary key(id),
  index ctcid(cid),
  index csubtype_i(csubtype)
) Engine=InnoDB DEFAULT CHARSET=utf8;

drop table if exists cardvariations;
create table cardvariations (
  id int(10) unsigned not null auto_increment,
  cid varchar(40) not null,
  cvars varchar(200) not null,
  primary key(id),
  index ctcid(cid),
  index cvars_i(cvars)
) Engine=InnoDB DEFAULT CHARSET=utf8;
