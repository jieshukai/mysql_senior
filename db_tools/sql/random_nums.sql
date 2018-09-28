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