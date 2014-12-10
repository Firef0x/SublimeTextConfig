#################################################################
# FileName:auto_file.py
# Author  :Tomhour
# Date    :2013/03/14 14:44:31
# Update  :2013/03/18 12:02:08
# Remark  :这是我的私有插件，完成一些自动化的处理过程
#		   使用参考readme.txt
#		   自动保存刷新段取时间功能(2013/03/18 12:05:45)
#		   添加自定义宏功能，手动写宏文件，定义宏名称，在处理数组加入处理方法(2013/03/16 12:05:06)
#		   更新为覆盖原Plain Text，而不是Hook更改设置(2013/03/17 12:03:10)
#		   更改等级小星星的算法，提高了效率，明显看到内存下降(2013/03/17 12:04:00)
#################################################################

import sublime, sublime_plugin
from time import time, sleep
import time
import os
import re
import threading

class gotosym(threading.Thread):
	def __init__(self,view,sym):
		threading.Thread.__init__(self)
		self.view = view
		self.sym = sym

	def run(self):
		while (self.view.is_loading()):
			sleep(0.1)
		avb=self.view.substr(sublime.Region(0,self.view.size()))
		syp=avb.find(self.sym)
		self.view.show(syp)
		self.view.sel().clear()
		self.view.sel().add(syp)
		self.stop()

	def stop(self):
		pass

class auto_file(sublime_plugin.EventListener):
	def on_pre_save(self,view):
		view.run_command('auto_proc',{'ref':'updtime'})
		pass
			
#modify time replace the TM_TH_TIME macro
	def on_modified(self,view):
		view.run_command("auto_proc",{'ref':'alltime'})
		pass

#command auto proc call
class AutoProcCommand(sublime_plugin.TextCommand):
	edit=None
	def procautoflush(self):
		view=self.view
		edit=self.edit
		curtime=time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
		sel=view.sel()[0]
		reg=r"^>{3}[^>][\r\n\S\s]*?[^<]<{3}\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}"
		reg_bb=view.find(reg,0)
		while not reg_bb.empty():
			if reg_bb.begin()<sel.begin() and reg_bb.end()>sel.end():
				treg=sublime.Region(reg_bb.end()-19,reg_bb.end())
				view.replace(edit,treg,curtime)
			reg_bb=view.find(reg,reg_bb.end())

	def proclv(self,add=True):
		view=self.view
		edit=self.edit

		sel=view.sel()[0]
		reg_l=view.line(sel)
		ppos=sel.begin()-reg_l.begin()
		pref=reg_l.begin()

		reg1=r"\[★*?(★|☆)\]"
		abuf=view.substr(sublime.Region(reg_l.begin(),reg_l.end()))
		if add:
			msg="Increase attention level!"
		else:
			msg="Decrease attention level!"

		for match in re.finditer(reg1,abuf):
			pstart=match.start(1)
			pend=match.end(1)
			cmatch=abuf[pstart:pend]

			if ppos<=pend:
				if cmatch=='★' and add:
					view.insert(edit,pref+pend,'☆')
				elif cmatch=='☆' and add:
					view.replace(edit,sublime.Region(pref+pstart,pref+pend),'★')
				elif cmatch=='☆' and not add:
					view.replace(edit,sublime.Region(pref+pstart,pref+pend),'')
				elif cmatch=='★' and not add:
					view.replace(edit,sublime.Region(pref+pstart,pref+pend),'☆')
				else:
					pass
				break
		sublime.status_message(msg)

	def procdt(self,args=None):
		view=self.view
		edit=self.edit
		dicdt={'dt':'TM_TH_DTTM','date':'TM_TH_DATE','time':'TM_TH_TIME'}
		ctime=time.localtime(time.time())
		dicvl={'dt':time.strftime('%Y/%m/%d %H:%M:%S',ctime),'date':time.strftime('%Y/%m/%d',ctime),'time':time.strftime('%H/%M/%S',ctime)}
		if not args==None:
			mcdt='#'+dicdt[args]
			reg_bb=view.find(mcdt,0)
			view.replace(edit, reg_bb, dicvl[args])

#when we db-click title goto the pos
	def proctitle(self):
		view=self.view
		edit=self.edit
		sel=view.sel()[0]
		reg_l=view.line(sel)
		reg1=r"(?<=[^\n])+(?<=\.)+\d+$"
		reg_bb1=view.find(reg1,reg_l.begin())

		#title go
		if reg_bb1.begin()>=reg_l.begin() and reg_bb1.end()<=reg_l.end():
			lnum=view.substr(reg_bb1)
			lnum=int(lnum)-1
	
			pt=view.text_point(lnum,0)
			view.show(pt)
			view.sel().clear()
			view.sel().add(sublime.Region(pt))

	def gotosym(self):
		view=self.view
		edit=self.edit
		sel=view.sel()[0]
		reg_l=view.line(sel)
		symbol=view.substr(view.word(sel.begin()))
		reg_sm_fun=r"\s*invoke[^\n]+\s+[A-Z](\S+);->(\S+\([A-Z]*\S*\))[A-Z]"#smali function
		reg_sm_cpth=r"\.class\s+[a-z]+\s+[A-Z](\S+);"
		sline=view.substr(reg_l)
		fmatch=re.match(reg_sm_fun,sline)

		fs_pos=sublime.Region(0,0)
		fs_line=view.line(fs_pos)
		s_fs_line=view.substr(fs_line)
		pmatch=re.match(reg_sm_cpth,s_fs_line)

		cfp=None
		pkg=None
		fun=None
		tfp=None
		if pmatch and fmatch:
			cfp=pmatch.group(1)
			pkg=fmatch.group(1)
			fun=fmatch.group(2)
		if cfp!=None and pkg!=None and fun!=None:
			cf=view.file_name()
			tfp=cf[0:cf.find(cfp+".smali")]+pkg+".smali"
		if tfp!=None and os.path.isfile(tfp):
			tfv=sublime.active_window().open_file("%s"%tfp)#集成的方法现在还不行
			waitgoto=gotosym(tfv,fun)
			waitgoto.start()
			return
		#print(symbol)
		#view.run_command("goto_definition",{"symbol":symbol})

#auto generate tile list
	def gentitile(self):
		pass

	def run(self, edit, ref=None,val=None):
		self.edit=edit
		# print(ref)
		if ref=="updtime":
			self.procautoflush()
			return
		elif ref=="pluslev":
			self.proclv(True)
			return
		elif ref=="sublev":
			self.proclv(False)
			return
		elif ref=="dt":
			self.procdt(ref)
			return
		elif ref=="date":
			self.procdt(ref)
			return
		elif ref=="time":
			self.procdt(ref)
			return
		elif ref=="alltime":
			self.procdt("dt")
			self.procdt("date")
			self.procdt("time")
			return
		elif ref=="titlego":
			self.proctitle()
			return
		elif ref=="gentitle":
			self.gentitle()
			return
		elif ref=="gotosym":
			self.gotosym()
			return
		else:
			pass