
﹃

第1章	按住Ctrl按鼠标左键跳转到第18行..........................18

第2节	按住Ctrl按鼠标左键跳转到第85行..........................85

第2节	按住Ctrl按鼠标左键跳转到117行..........................117

﹄

>>############### 编写了Text.tmLanguage ########################

#现了自动设置语法文件为Text on_load,on_pre_save,on_new(2013/03/18 10:14:46废弃)
重载默认的Plain Text语法，放在Packages/Text下面

>> 第1章 基本

>>>> 第1节 基本

//comment

/******************
comment
******************/

===================
comment
===================

1、 			小标题

1.2.3 			多级子标题

二、

(二)

（二）

1.

(1)

（1）

192.168.1.3 IP地址

2013-03-08	日期

2013/03/08

15:25		时间

15:25:25

http://www.baidu.com/aa.html 	URL地址

sftp://www.baidu.com/aaa.p 		FTP等其他的协议

mailto:zorodey@163.com 			邮箱地址

这是主题：						主题开头标识

AAA_BBB 						大写的特殊缩写

int function(int a);			函数名

[ -a 文件 ]						中括号标签

PS 								PS注解
P.S 
ps 
p.s

"double string"	'single string'

that's test of it's ,that's test of it'sd

that's test of it'sthat's test of it'sd

•标签型

>>############# User Macro Define ####################################
1、TM_TH_TIME

/*********************************************************************\
*  Copyright (c) 1998-2013, TH. All Rights Reserved.
*  Author :Tomhour
*  FName  :readme.txt
*  Time   :2013/03/11 23:06:28
*  Remark :File Head Remark Example
\*********************************************************************/

2、dt 			2013/03/11 23:05:29
3、date 		2013/03/11
4、time 		23:05:38

>>>特殊段,光标在此区段，按保存之后自动刷新本区段时间
//然后就可以自动更新此段的时间标签了
<<<2013/03/18 10:17:33

>>>特殊段,光标在此区段，按保存之后自动刷新本区段时间
//然后就可以自动更新此段的时间标签了
<<<2013/03/18 10:17:35

某项任务[★★☆]//在此行中按ctrl+alt+i增加等级，[★★☆]按ctrl+alt+u减少等级

... ... ... ... ... ... ... ... ... ... ... ... ... ... 其他待添加

>>############ auto_file.py ##########################################
自动设置文件语法为Text，但是必须后缀为txt（不分大小写）


(?:^[\s]*|\b[\s]+)-[^-\s]+?(?=[\s:\|@]+)//前面的子式，表现为一个元是一个整体

//ST的配置以及参数大都是以json或者xml格式传播，而xml是HTML语言，所以对于<等特殊符号应该需要做转意


create -n avl -t 1 -vnc:2 -user@zorodey -tar|grep -F '$1'
//命令行参数化支持


>>############ Sublime Text info #####################################
Default.sublime-package					-- Symbol List.tmPreferences决定哪些symbol会被加入到symbol list里面
Color Scheme - Default.sublime-package	-- 默认主题包
Theme - Default.sublime-package			-- 默认程序主题包
Packages目录下对应的默认包目录，可以自定义重载系统配置

1. Setting - User
{
	"caret_style": "phase",
	"color_scheme": "Packages/Color Scheme - Default/Monokai.tmTheme",
	"font_size": 9,
	"highlight_line": true,
	"ignored_packages":
	[
		"SFTP",
		"SublimeClang",
		"Vintage"
	],
	"margin": 4,
	"theme": "Nil.sublime-theme",
	"word_wrap": true,
	"update_check":false
}

2. Key Bindings - User

[
{
    "command": "auto_proc","args":{"ref":"pluslev"},
    "keys": ["ctrl+alt+p"]
},
{
    "command": "auto_proc","args":{"ref":"sublev"},
    "keys": ["ctrl+alt+i"]
}
]

3. Mouse Bindings

[
    {
        "button": "button1", "count": 1,
        "modifiers":["ctrl"],
        "command": "auto_proc",
        "args":{"ref":"titlego"}
    }
]

[
    {
        "button": "button1", "count": 2,//Hook双击操作
        "press_command": "drag_select",//保留系统原有操作
        "press_args": {"by": "words"},
        "command": "auto_proc",//命令接收程序
        "args":{"ref":"titlego"}//命令参数
    }
](2013/03/18 10:20:36废弃)