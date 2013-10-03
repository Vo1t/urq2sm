#!/usr/bin/python
# coding: utf8
import re
def name (text):
	return re.sub("^:(.*)\r\n",":: \\1[::]1-1-1\r\n",text)
def ifthen (text):
	text = re.sub("if (.*?) then (.*\r\n)","<<if \\1>>\r\n\\2<<endif>>\r\n",text)
	iflist = re.findall("<<if .*?>>", text)
	ifnewlist = []
	for i in iflist:
		newi = re.sub("(if |and |or |not )+(\S)","\\1 $\\2",i)
		newi = re.sub(" +","_",newi[5:-2])
		newi = newi.replace('_and_',' and ').replace("_or_"," or ").replace("not_","not ").replace('=','~')
		re.sub("_*([<>~])_*","\\1",newi)
		newi = "<<if " + newi.replace('~',' eq ').replace('>',' gt ').replace('<',' lt ').replace(' $and ',' and ').replace(' $or ',' or ').replace(' $not ',' !')  + ">>"
		newi = newi.replace("if _","if ").replace('.','').replace(',','')
		newi =re.sub("(eq |gt |lt )([^0-9\'])","\\1$\\2", newi)
		text = text.replace(i, newi)
	text = re.sub("\$(\d)","$_\\1",text)
	return text
def amp (text):
	return text.replace('& ','\r\n')
def pln (text):
	text = re.sub("[^\S]p ","",text)
	text = text.replace("#$","")
	text = re.sub("pln\s","", text)
	text = re.sub("^p ","", text)
	text = re.sub(" p ","", text)
	return text
def btn (text):
	text = re.sub("btn (.*?), *(.*?)\r\n","[[\\2|\\1]]\r\n",text)	
	return text
def cls (text):
	text = re.sub("cls\s","<<clrscr>>\r\n",text)
	return text
def pause (text):
	text = re.sub("pause (\d+)","",text)
	return text
def goto (text):
	text = re.sub("goto (\S+)","<<clrscr>>\r\n<<display '\\1'>>",text)
	return text
def inv (text):
	text = re.sub("inv\+ (.*)\r\n","\\1=1\r\n",text)
	text = re.sub("inv\- (.*)\r\n","\\1=0\r\n",text)
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
def start (text):
	text = ":: start[::]1-1-1\r\n<<display 'perkill'>>\r\n<<display 'начало1'>>\r\n" + text
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
	text = text.replace("perkill","<<display 'perkill'>>")
	text = text+macr
	return text	
urqfile = open("Evgeny2.qst").read()
smfile = open("hamster1.sm",'w')
paragraph = re.compile("^:[\s\S]*?^end",re.MULTILINE)
list_par = paragraph.findall(urqfile)
resuilt = ""
for par in list_par:
	par = par[:-3]
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
	resuilt = resuilt + par + "\r\n"
resuilt = perkill(resuilt)
resuilt = start(resuilt)
smfile.write(resuilt)
