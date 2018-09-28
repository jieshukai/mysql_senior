CREATE PROCEDURE `create_table_emp`()
BEGIN
	#Routine body goes here...
CREATE TABLE `emp`(
id int unsigned PRIMARY key not null auto_increment,
eid int UNSIGNED not null DEFAULT 0,
ename varchar(255) not NULL DEFAULT "",
esalary int UNSIGNED DEFAULT 0,
pid int UNSIGNED DEFAULT 0);
END