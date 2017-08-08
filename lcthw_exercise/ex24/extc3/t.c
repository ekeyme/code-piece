#include <stdio.h>
char *trim(char * str)
{
	char *buf1, *buf2;
	if (str == NULL)
	{
		return NULL;
	}
	
	// 处理字符串前面的空格	
	for (buf1=str; *buf1 && *buf1==' '; buf1++);
	// 将去掉前面空格的字符串向前复制
	for (buf2=str; *buf1;)
	{
		*buf2++ = *buf1++;
	}
	*buf2 = '\0';
	// 处理字符串后面的空格
	while (*--buf2 == ' ')
	{
		*buf2 = '\0';
	}
	return str;	
}
int main(int argc, char *argv[])
{
      printf("trim(\"%s\") ", argv[1]);
      printf("returned \"%s\"\n", trim(argv[1]));
      return 0;
}