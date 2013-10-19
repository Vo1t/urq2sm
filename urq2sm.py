#!/usr/bin/python
# coding: utf8
import codecs
import re
def comm (text):				
		text = text[text.find("\r\n:"):]
		return re.sub(";.*","",text).replace('#',' ').replace('$','')
def name (text):		
		text = re.sub("\s*:(.*)\r\n",":: \\1[::]1-1-1\r\n",text[:50]) + re.sub("(\r\n)+:(.*)\r\n","\r\nLABEL\\2LABEL\r\n",text[50:])				
		return text
def ifthen (text):		
		text = re.sub("then +& +if","and",text,flags=re.I)		
		text = re.sub("if (.*?) then (.*)\r\n","<<if \\1>>\\2<<endif>>",text, flags=re.I)				
		iflist = re.findall("<<if .*?>>", text, flags=re.I)
		ifnewlist = []
		for i in iflist:						
				newi = re.sub(" *(<|>|=|<=|>=|<>) *","\\1",i)
				newi = re.sub("((if |and |or |not )+)(\S)","\\1 $\\3",newi, flags=re.I)
				newi = re.sub(" +","_",newi[5:-2], flags=re.I)
				newi = re.sub("[_\$*](and|or|not)([_ ])"," \\1 ", newi, flags=re.I).replace('=','~')
				re.sub("_*([<>~]+)_*","\\1",newi)				
				newi = "<<if " + newi.replace('>~',' gte ').replace('<>'," neq ").replace('<~',' lte ').replace('~',' eq ').replace('>',' gt ').replace('<',' lt ').replace(' $and ',' and ').replace(' $or ',' or ').replace(' $not ',' !')  + ">>"
				newi = newi.replace("if _","if ").replace('.','').replace(',','')
				newi =re.sub("(eq |gt |lt |neq |lte | gte )([^0-9\'])","\\1$\\2", newi)				
				newi =re.sub("not_([^\s\>]+)","!(\\1)",newi)
				print newi		
				text = text.replace(i, newi)
		text = re.sub("\$(\d)","$_\\1",text)
		return text
def amp (text):
		return re.sub(' *\& ','\r\n',text)
def pln (text):		
		text = re.sub("([\s>])p ([^<]*)\r\n","\\1\\2",text,flags=re.I)
		text = re.sub("([\s>])p ([^<]*)<","\\1\\2<",text,flags=re.I)
		text = re.sub("([\s>])pln ([^<]*)\r\n","\\1\\2\r\n",text,flags=re.I)
		text = re.sub("([\s>])pln ([^<]*)<","\\1\\2\r\n<",text,flags=re.I)
		text = re.sub("pln ","",text,flags=re.I)
		text = re.sub("pln\r\n","",text,flags=re.I)
		text = re.sub("pln","\r\n",text,flags=re.I)
		return text
def btn (text):
		text = text+"\r\n"
		text = re.sub("> *btn ",">\r\nbtn ",text)
		text = re.sub("btn (.*?), *(.*?)<","[[\\2|\\1]]\r\n<",text, flags=re.I)   
		text = re.sub("btn (.*?), *(.*?)\r\n","[[\\2|\\1]]\r\n",text, flags=re.I)  
		text = re.sub("(\[\[)([^\]]+\|Use[^\]]+\]\])","\\1+\\2",text)
		return text
def cls (text):
		text = re.sub("cls\s","<<clrscr>>\r\n",text)
		return text
def pause (text):
		text = re.sub("pause (\d+)","",text)
		return text
def goto (text):
		text = re.sub("goto ([^\s\<]+)","<<display '\\1'>>",text,flags=re.I)
		return text
def proc (text):
		text = re.sub("proc ([^\s\<]+)","<<display '\\1'>>",text,flags=re.I)
		return text
def inv (text):		
		text = re.sub("inv\+ (.*?)(\r\n|<)","\\1=1\\2",text,flags=re.I)
		text = re.sub("inv\- (.*?)(\r\n|<)","\\1=0\\2",text,flags=re.I)		
		return text
def instr(text):
		text = re.sub("instr (.*)=(.*)\r\n","\\1='\\2'\r\n",text)
		return text
def set (text):
		text = re.sub("([^<>\s=][^<>=\n]+)=([^<\r\n]*)(\r\n|\<)","<<set $\\1=\\2>>\\3",text)		
		setlist  = re.findall("\$[^>]*?=\s*.",text)
		for i in setlist:				
				newi = re.sub(" *(\=|\+|\-) *","\\1",i)
				newi = newi.replace(' ','_').replace('=',' =')
				newi = re.sub("([=\-\+])([^0-9\'])","\\1 $\\2",newi)
				newi = newi.replace('=','= ').replace('.','').replace(',','')				
				text = text.replace(i,newi)
		text = re.sub("\$(\d)","$_\\1",text)
		text = re.sub("(\$\S+)([\-\+])","\\1 \\2",text)
		return text
def rnd (text):
		text = re.sub("<<set (.*)= *\$rnd\*(.*)>>","<<random \\1 = \\2>>",text)
		return text
def label (text):
		text = re.sub("LABEL(.*)LABEL","<<goto '\\1'>>\r\n\r\n:: \\1[::]1-1-1\r\n",text)
		return text
def start (text):
		m = re.findall(":.*?\r\n",text)
		title = m[0]
		text = re.sub("(goto|btn|[:])( *)start","\\1\\2start_old",text,flags=re.I)		
		text = "\r\n:start\r\ngoto "+title[1:]+"\r\nend\r\n"+text
		return text
def perkill (text):
		perlist = re.findall("\$[^\s\)\[\<>]+",text)
		plist = []
		for p in perlist:
				p = p.replace('>','')
				if p not in plist:
						plist.append(p)
		macr = ":: perkill[::]1-1-1\r\n"
		for i in plist:
				macr = macr + "<<set " + i + "=0>>\r\n"
		text = re.sub("perkill","<<display 'perkill'>>",text,flags=re.I)
		text = re.sub("invkill","",text,flags=re.I)
		text = text+macr
		return text		
def btnuse(text):
	uselist = re.findall(": *Use_[^_\r]*\r\n",text)
	print uselist
	actlist = re.findall(": *Use_.*_.*\r\n",text)
	for a in actlist:
		newuse = re.sub("(: *Use_.*)_.*\r\n","\\1\r\n",a)
		print newuse
		if newuse not in uselist:
			name = re.sub(": *Use_","",newuse)
			text = text + "\r\n" + newuse + "pln " + name + '\r\nend\r\n'
	plist = re.findall(": *Use_[^_]*\r\n.*\r\n\s*end",text,flags=re.I|re.MULTILINE)
	for p in plist:
		pname = p.split('\r\n')[0]
		pname = re.sub(".*Use_","",pname.strip())		
		alist = re.findall(": *Use_"+pname+"_.*",text,flags=re.I)		
		newp = p[:-3]
		for a in alist:			
			a1 = a.split('\r\n')[0]			
			bname = a1[1:].strip()
			btext =a1.split('_')[2].strip()
			newp = newp+"btn "+bname+','+btext+'\r\n'		
		newp = newp + '\r\nend'		
		text = text.replace(p,newp)
	return text
def inventory(text):
	res = ""
	invlist = re.findall(": *Use_[^_\r]*\r\n",text,flags=re.I)
	for i in invlist:
		pred = re.sub(".*Use_","",i.strip())			
		btntext = i.strip()[1:]
		predname = pred.replace(' ','_').replace('.','')
		res = res + "<<if $"+predname+" gt 0>>[[+"+pred+"|"+btntext+"]] <<endif>>"	
	return res
urqfile = open("or.qst").read()
smfile = open("hamster1.sm",'w')
urqfile = start(urqfile)
urqfile = btnuse(urqfile)
preds = inventory(urqfile)
list_par = urqfile.replace('End','end').replace("\r\nend","\r\nendendend").split("endendend")
resuilt = "\r\n"
for par in list_par:						
		par =  comm(par)		
		par =  name(par)		
		par = ifthen(par)
		par = pln(par)
		par = amp(par)				
		par = btn(par)
		par = cls(par)
		par = pause(par)
		par = goto(par)
		par = proc(par)
		par = inv(par)
		par = instr(par)
		par = set(par)
		par = rnd(par)		
		par = label(par)	
#		par = input(par)
		resuilt = resuilt + par + "\r\n" 
resuilt = perkill(resuilt)
resuilt += "::StoryMenu[::]1-1-1\r\n"+preds
smfile.write(resuilt.decode('cp1251').encode('utf8'))
