# mysql senior
## insert mysql 1000W data
### achieved by sql
1. requirement
- 建数据库，建表
- 随机数据（随机字符串，随机数字）
- 生成数据并注入表中
2. 思路
- 两个函数（有返回值）
    1. 随机生成字符串letters（可自定义长度）
    2. 随机生成字符串digits（可自定义长度）
- 两个过程（无返回值）
    1. 创建表（emp 员工表）
    2. 注入数据（编号，姓名，部门）
3. 实现
- 两个函数
```sql
CREATE FUNCTION `random_nums`(`n` int) RETURNS varchar(20) CHARSET utf8
BEGIN
	#Routine body goes here...
	declare chars_str varchar(20) default "1234567890";
	declare return_str varchar(20) default "";
	declare i int default 0;
		while i < n do
			set return_str = CONCAT(return_str,substring(chars_str,floor(1+RAND()*10),1));
			set i = i+1;
		end while;
	return return_str;
END
```
```sql
CREATE FUNCTION `random_str`(`n` int) RETURNS varchar(255) CHARSET utf8
BEGIN
	#Routine body goes here...
	declare chars_str varchar(100) default "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM";
	declare return_str varchar(255) default "";
	declare i int default 0;
		while i < n do
			set return_str = CONCAT(return_str,substring(chars_str,floor(1+RAND()*52),1));
			set i = i+1;
		end while;
	return return_str;
END
```
- 两个过程
```sql
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
```
```sql
CREATE PROCEDURE `insert_emp`(`start_num` int,`max_length` INT)
BEGIN
	#Routine body goes here...
	declare i int default 0;
	repeat
	insert into emp(eid,ename,pid) values(start_num+i,random_str(8),random_nums(3));
		set i = i + 1;
UNTIL i >= max_length END REPEAT;

END
```
### achieved by python
1. requirement
```cmd
pip install pymysql
pip install sqlalchemy
pip install faker
```
- 连接数据库 pymysql
- 数据库操作 SQLAlchemy
- 生成假数据 faker
2. 思路
- 
- 