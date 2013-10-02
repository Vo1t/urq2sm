# coding: utf8
import re
def amp (text):
	return text.replace('& ','\r\n')
def name (text):
	return re.sub("^:(.*)\r\n",":: \\1[::]1-1-1\r\n",text)
def pln (text):
	text = re.sub("pln\s","", text)
	text = re.sub("^p ","", text)
	text = re.sub(" p ","", text)
	return text
def object(text):
	iflist = re.findall("if .*? then",text)	
	for i in iflist:
		newi = i[3:-5].replace(' ','_')
		newi = newi.replace('_and_',' and ').replace("_or_"," or ").replace("not_","not ").replace('=','~')
		text = text.replace(i,"if "+newi+" then")
	iflist = re.findall("(then)*.*=.*",text)
	for i in iflist:
		newi = i.replace(' ','_')
		newi = newi.replace('_=',' =').replace('=_','= ')
		text = text.replace(i,newi)
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
		 newif = re.sub("(\S+) *([\<\>\~])","$\\1\\2",if1[4:-2])
		 newif = re.sub("([\<\>\~]) *(\D+)","\\1$\\2",newif)
		 newif = newif.replace(" not "," ! ")
		 newif = re.sub("(if|and|or|!) ([^\$^!])","\\1 $\\2","<<if"+newif+">>")		 
		 ifnewlist.append(newif)
	n = 0
	for if1 in iflist:
		ifnewlist[n] = "<<if" + ifnewlist[n][4:-2].replace('~',' eq ').replace('>',' gt ').replace('<',' lt ').replace(' $and ',' and ').replace(' $or ',' or ').replace(' $not ',' !')  + ">>"
		text = text.replace(if1, ifnewlist[n])
		n = n+1	
	return text
def set (text):
	text = re.sub("([^>\s=][^>=\n]+)=(.*)\r\n","<<set $\\1 = \\2>>\r\n",text)
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
urqfile = open("Evgeny2.qst").read()
smfile = open("hamster1.sm",'w')
paragraph = re.compile("^:[\s\S]*?^end",re.MULTILINE)
urqfile = object(urqfile)
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
	par = cls(par)
	par = pause(par)
	resuilt = resuilt + par + "\r\n"
resuilt = perkill(resuilt)
smfile.write(resuilt)
	
