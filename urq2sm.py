# coding: utf8
import re
def amp (text):
	return text.replace('& ','\r\n')
def name (text):
	return re.sub("^:(.*)\r\n",":: \\1[::]1-1-1\r\n",text)
def pln (text):
	text = re.sub("pln\s","", text)
	return text
def btn (text):
	text = re.sub("btn (.*?), (.*?)\r\n","[[\\2|\\1]]\r\n",text)
	return text
def inv (text):
	text = re.sub("inv\+ (\S*)","\\1=1",text)
	text = re.sub("inv\- (\S*)","\\1=0",text)
	return text
def ifthen (text):
	text = re.sub("if (.*?) then (.*\r\n)","<<if \\1>> \\2 <<endif>>\r\n",text)
	text = re.sub("IF (.*?) then (.*\r\n)","<<if \\1>> \\2 <<endif>>\r\n",text)
	iflist = re.findall("<<if .*?>>", text)
	ifnewlist = []
	for if1 in iflist:
		 ifnewlist.append("<<if" + re.sub(" ([A-zА-я])"," $\\1",if1[4:]))
	n = 0
	for if1 in iflist:
		ifnewlist[n] = "<<if" + ifnewlist[n][4:-2].replace('=',' eq ').replace('>',' gt ').replace(' $and ',' and ').replace(' $or ',' or ')  + ">>"
		text = text.replace(if1, ifnewlist[n])
		n = n+1	
	return text
def set (text):
	text = re.sub("(\S*?)=(.*)\r\n","<<set $\\1 = \\2>>\r\n",text)
	return text
def goto (text):
	text = re.sub("goto (\S+)","<<display '\\1'>>",text)
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
urqfile = open("hamster1.qst").read()
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
	par = inv(par)	
	par = set(par)
	par = goto(par)
	resuilt = resuilt + par + "\r\n"
resuilt = perkill(resuilt)
smfile.write(resuilt)
	
