CREATE PROCEDURE `insert_emp`(`start_num` int,`max_length` INT)
BEGIN
	#Routine body goes here...
	declare i int default 0;
	repeat
	insert into emp(eid,ename,pid) values(start_num+i,random_str(8),random_nums(3));
		set i = i + 1;
UNTIL i >= max_length END REPEAT;

END