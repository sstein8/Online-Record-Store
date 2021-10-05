-- add drop table for all your tables if they exist

DROP TABLE IF EXISTS cart CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS genre CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS customer CASCADE;



-- add create table for all your tables

-- add insert statements to populate your tables


CREATE TABLE customer (
FirstName   varchar(30) not null, 
LastName    varchar(30) not null,
UserName    varchar(30) not null,
Password    varchar(30) not null,
primary key (UserName)
);

CREATE TABLE genre (
genreName    varchar(15) not null, 
primary key (genreName)
);

CREATE TABLE product (
pname    varchar(50) not null, 
price    double(4,2) not null,
genre    varchar(15) not null, 
ID       int         not null, 
quantity int(2)      not null,
primary key (ID),
foreign key (genre) references genre(genreName)
);

CREATE TABLE cart (
rowNum      int         not null auto_increment, 
pname       varchar(50) not null, 
productID   int         not null, 
sumPrice    double      not null, 
quantity    int         not null,
primary key (rowNum),
foreign key (productID) references product(ID)
);

CREATE TABLE orders (
orderID    int          not null auto_increment, 
UserName   varchar(20)  not null, 
totPrice   double        not null, 
primary key (orderID),
foreign key (UserName) references customer(UserName)
);


INSERT INTO customer VALUES('Test', 'User', 'testuser', 'testpass');

INSERT INTO genre VALUES('ROCK');
INSERT INTO genre VALUES('Pop');
INSERT INTO genre VALUES('HipHop');
INSERT INTO genre VALUES('Disco');

INSERT INTO product VALUES('Stadium Arcadium', 35.00, 'Rock', 1, 5);
INSERT INTO product VALUES('Wasting Light', 24.99, 'Rock', 2, 5);
INSERT INTO product VALUES('Rumours', 23.99, 'Rock', 3, 5);

INSERT INTO product VALUES('Room For Squares', 17.25, 'Pop', 4, 5);
INSERT INTO product VALUES('It Wont Be Soon Before Long', 14.50, 'Pop', 5, 5);
INSERT INTO product VALUES('The END', 12.75, 'Pop', 6, 5);

INSERT INTO product VALUES('Graduation', 15.00, 'HipHop', 7, 5);
INSERT INTO product VALUES('Pink Friday', 16.39, 'HipHop', 8, 5);
INSERT INTO product VALUES('Ready To Die', 24.58, 'HipHop', 9, 5);

INSERT INTO product VALUES('Saturday Night Fever', 30.74, 'Disco', 10, 5);
INSERT INTO product VALUES('I Am', 26.44, 'Disco', 11, 5);
INSERT INTO product VALUES('We Are Family', 25.50, 'Disco', 12, 5);


