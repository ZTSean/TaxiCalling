# Create Database

To create the database, you have to enter the data first. Open the **terminal**(Mac) or **Command Prompt**(Windows)

Type the command: `mysql -u root -p` 

**Notice:** if you do not need to enter the password after execute the command, you need to the update the password by command `ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';` . After update, you `root` 's password will be set to `password`.



#### Create Database for the TaxiCalling

To create database for the taxicalling project, you have to run the command below after you enter the mysql as a root user

`CREATE DATABASE taxicalling;`

(How to determine whether you've enter the mysql in the terminal:

you will see `mysql > ` )





#### Create table for caller
**Notice**: to enter the database taxicalling, do command `\u taxicalling;`
run the following SQL sentence when you enter the database `taxicalling`

```
CREATE TABLE request(
 id INT NOT NULL AUTO_INCREMENT,
 date DATE NOT NULL,
 time TIME NOT NULL,
 from_x DECIMAL(10, 8) NOT NULL,
 from_y DECIMAL(11, 8) NOT NULL,
 name VARCHAR(255) NOT NULL,
 phone VARCHAR(20),
 destination VARCHAR(255) ,
 to_x DECIMAL(10, 8) NOT NULL,
 to_y DECIMAL(11, 8) NOT NULL,
 PRIMARY KEY(id)
);

```



#### Create table for driver

run the following SQL sentence when you enter the database `taxicalling`

```
CREATE TABLE driver(
 id INT NOT NULL AUTO_INCREMENT,
 date DATE NOT NULL,
 time TIME NOT NULL,
 location_x DECIMAL(10, 8) NOT NULL,
 location_y DECIMAL(11, 8) NOT NULL,
 name VARCHAR(255) NOT NULL,
 status INT,
 PRIMARY KEY(id)
);
```



