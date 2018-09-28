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