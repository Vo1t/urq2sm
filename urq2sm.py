#!/usr/bin/python
# coding: utf8
import codecs
import re
def comm (text):		
	text = text[text.find("\r\n:"):]
	return re.sub(";.*","",text).replace('#','').replace('$','')
def name (text):	
	text = re.sub("\s*:(.*)\r\n",":: \\1[::]1-1-1\r\n",text[:70]) + re.sub("(\r\n)+:(.*)\r\n","\r\nLABEL\\2LABEL\r\n",text[70:])		
	return text
def ifthen (text):	
	text = re.sub("then +& +if","and",text,flags=re.I)
	text = re.sub("if (.*?) then (.*\r\n)","<<if \\1>>\r\n\\2<<endif>>\r\n",text, flags=re.I)	
	iflist = re.findall("<<if .*?>>", text, flags=re.I)
	ifnewlist = []
	for i in iflist:		
		newi = re.sub("(if |and |or |not )+(\S)","\\1 $\\2",i, flags=re.I)
		newi = re.sub(" +","_",newi[5:-2], flags=re.I)
		newi = re.sub("[_\$*](and|or|not)([_ ])"," \\1 ", newi, flags=re.I).replace('=','~')
		re.sub("_*([<>~]+)_*","\\1",newi)
		newi = "<<if " + newi.replace('>~',' gte ').replace('<~',' lte ').replace('~',' eq ').replace('>',' gt ').replace('<',' lt ').replace(' $and ',' and ').replace(' $or ',' or ').replace(' $not ',' !')  + ">>"
		newi = newi.replace("if _","if ").replace('.','').replace(',','')
		newi =re.sub("(eq |gt |lt )([^0-9\'])","\\1$\\2", newi)
		text = text.replace(i, newi)
	text = re.sub("\$(\d)","$_\\1",text)
	return text
def amp (text):
	return re.sub(' *\& ','\r\n',text)
def pln (text):
	text = re.sub("[^\S]p ","",text,flags=re.I)
	text = text.replace("#$","")
	text = re.sub("pln\s","", text, flags=re.I)
	return text
def btn (text):
	text = re.sub("btn (.*?), *(.*?)\r\n","[[\\2|\\1]]\r\n",text, flags=re.I)	
	return text
def cls (text):
	text = re.sub("cls\s","<<clrscr>>\r\n",text)
	return text
def pause (text):
	text = re.sub("pause (\d+)","",text)
	return text
def goto (text):
	text = re.sub("goto (\S+)","<<goto '\\1'>>",text,flags=re.I)
	return text
def inv (text):
	text = re.sub("inv\+ (.*)\r\n","\\1=1\r\n",text,flags=re.I)
	text = re.sub("inv\- (.*)\r\n","\\1=0\r\n",text,flags=re.I)
	return text
def instr(text):
	text = re.sub("instr (.*)=(.*)\r\n","\\1='\\2'\r\n",text)
	return text
def set (text):
	text = re.sub("([^>\s=][^>=\n]+)=(.*)\r\n","<<set $\\1=\\2>>\r\n",text)
	setlist  = re.findall("\$.*?=\s*.",text)
	for i in setlist:
		newi = i.replace(' ','_').replace('=',' =')
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
	title = re.match(":.*?\r\n",text).group()
	text = re.sub("(goto|btn|[:])( *)start","\\1\\2start_old",text,flags=re.I)	
	text = "\r\n:start\r\ngoto "+title[1:]+"\r\nend\r\n"+text
	return text
def perkill (text):
	perlist = re.findall("\$[\S]+",text)
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
urqfile = open("Evgeny2.qst").read()
smfile = open("hamster1.sm",'w')
urqfile = start(urqfile)
list_par = urqfile.replace('End','end').split('\r\nend')
resuilt = "\r\n"
for par in list_par:			
	par = par + '\r\n'
	par =  comm(par)	
	par =  name(par)	
	par = ifthen(par)
	par = amp(par)
	par = pln(par)	
	par = btn(par)
	par = cls(par)
	par = pause(par)
	par = goto(par)
	par = inv(par)
	par = instr(par)
	par = set(par)
	par = rnd(par)	
	par = label(par)	
	resuilt = resuilt + par + "\r\n------------------------------------------------------------\r\n"
resuilt = perkill(resuilt)
smfile.write(resuilt)
#.decode('cp1251').encode('utf8'))
