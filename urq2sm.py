import re
import sys
keywords = ['if','btn','p','pln','instr']
def clear (filename):
	slist = open(filename).readlines()
	i = 0
	for s in slist:		
		n = s.lower().count(" then ")
		s = s + " & <<endif>>" * n			
		s = re.sub(" then "," & ",s,flags=re.I)		
		s = re.sub(" else ","& <<else>> &",s,flags=re.I)
		s = re.sub("perkill","<<display 'perkill'>>",s,flags=re.I)
		s = re.sub("invkill","<<display 'perkill'>>",s,flags=re.I)
		s = re.sub("inv_","",s,flags=re.I)
		alist = s.split('&')
		j = 0
		for a in alist:
			alist[j] = a.strip()
			j = j+1
		s = " & ".join(alist)
		slist[i] = s.strip()
		i = i+1
	text = "\n".join(slist)
	text = re.sub(";.*$","",text,flags=re.M)
	text = re.sub("\n+","\n",text)	
	return text
def start (text):
	title = re.findall("^:.*$",text,flags=re.M)[0]
	text = re.sub("(goto|btn|:)( *)start","\\1\\2start_old",text,flags=re.I)		
	text = "\n" + ":start" + "\n" + "<<display 'perkill'>>" + '\n' + "goto "+ title[1:] + '\n' + "end" + "\n" + text
	return text
def btnuse(text):
	text = re.sub("^: ",":",text,flags=re.M)
	text = re.sub("^:Use",":use",text,flags=re.M)
	uselist = re.findall("^:use_[^_\n]*$",text,flags=re.M)
	actlist = re.findall("^:use_.*_.*$",text,flags=re.M)
	for a in actlist:
		newuse = re.sub("(:use_.*)_.*","\\1",a)
		if newuse not in uselist:		
			name = re.sub(":use_","",newuse)
			text = text + "\n" + newuse + "\n" + "pln " + name + '\n' + "end" + '\n'
	plist = re.findall("^:use_[^_\n]*\n[\s\S]*?\nend",text,flags=re.I|re.M)
	for p in plist:
		pname = p.split('\n')[0]
		pname = re.sub(":use_","",pname)		
		alist = re.findall(":use_"+pname+"_.*$",text,flags=re.M)		
		newp = p[:-3]
		for a in alist:						
			bname = a[1:]
			btext =a.split('_')[2]
			newp = newp + "btn " + bname + ',' + btext + '\n'		
		newp = newp + "end"		
		text = text.replace(p,newp)
	return text
def inventory(text):
	res = "::StoryMenu[::]1-1-1\n"
	invlist = re.findall(":use_[^_\n]*\n",text)
	for i in invlist:
		pred = re.sub(".*use_","",i.strip())			
		btntext = i.strip()[1:]
		predname = pred.replace(' ','_').replace('.','')
		res = res + "<<if $"+predname+" gt 0>>[[+"+pred+"|"+btntext+"]] <<endif>>"	
	res = res + '\n'
	return res
def perkill (text):	
	perlist = re.findall("<<set \$.*?=",text)
	plist = []
	macr = ":: perkill[::]1-1-1\n"
	for p in perlist:
		p = p[6:-1]
		if p not in plist:
			plist.append(p)	
	for i in plist:
		macr = macr + "<<set " + i + "=0>>\n"		
	return macr		
def end (text):
	text = re.sub("^end$","endendend",text,flags=re.I|re.M)
	return text
def name (text):
	text = re.sub(":(.*)","::\\1[::]1-1-1",text)
	return text
def ifthen (text):			
	if text[:3].lower() <> "if ": return text
	newi = re.sub(" *(<|>|=|<=|>=|<>) *","\\1",text)
	newi = re.sub(" +"," ",newi)
	newi = re.sub("\)(\S)",") \\1",newi)
	newi = re.sub("((if |and |or |not |\()+)(\S)","\\1$\\3",newi, flags=re.I)		
	newi = re.sub(" +","_",newi[3:])	
	newi = re.sub("[_ ](and|or|not)([_ ])"," \\1 ", newi, flags=re.I).replace('=','~')		
	re.sub("_*([<>~]+)_*","\\1",newi)		
	newi = "if " + newi.replace('>~',' gte ').replace('<>'," neq ").replace('<~',' lte ').replace('~',' eq ').replace('>',' gt ').replace('<',' lt ').replace(' $and ',' and ').replace(' $or ',' or ').replace(' $not ',' !') 
	newi = newi.replace("if _","if ").replace('.','').replace(',','')
	newi =re.sub("(eq |gt |lt |neq |lte | gte )([^0-9\'])","\\1$\\2", newi)				
	newi =re.sub("not_([^\s\>]+)","!(\\1)",newi)		
	newi = re.sub("\$(\d)","$_\\1",newi)
	text = "<<" + newi + ">>"
	return text
def btn (text):
	if text[:4].lower() <> 'btn ': return text
	text = re.sub("btn (.*?), *(.*)","[[\\2|\\1]]",text, flags=re.I)     
	text = re.sub("(\[\[)([^\]]+\|use[^\]]+\]\])","\\1+\\2",text)
	text = text + '\n'
	return text
def set (text):
	t1 = text.split(' ')[0]
	if t1 in keywords: return text
	tlist = text.split('=')
	if len(tlist) <> 2: return text
	tlist[0] = '$' + tlist[0].strip().replace(' ','_')
	newi = '=' + tlist[1].strip()
	newi = re.sub(" *(=\*|\+|\-) *","\\1",newi)
	newi = newi.replace(' ','_')
	newi = re.sub("([=\*\-\+])([^0-9\'])","\\1$\\2",newi)
	newi = newi.replace('.','').replace(',','')				
	tlist[1] = newi
	newi = tlist[0]+tlist[1]
	newi = re.sub("\$(\d)","$_\\1",newi)
	text = "<<set " + newi + ">>"
	return text
def inv (text):		
	if text[:3].lower() <> "inv": return text
	count = text.find(',')
	if count == -1:
		text = re.sub("inv\+ (.*)","\\1=1",text,flags=re.I)
		text = re.sub("inv\- (.*)","\\1=0",text,flags=re.I)	
		return text
	else:
		text = re.sub("inv\+ (.*), *(.*)","\\2=\\2+\\1",text,flags=re.I)
		text = re.sub("inv\- (.*), *(.*)","\\2=\\2-\\1",text,flags=re.I)	
		return text		
def instr(text):
	if text[:5].lower <> "instr": return text
	text = re.sub("instr (.*)=(.*)","\\1='\\2'",text)
	text = "<<set " + text + ">>"
	return text
def goto(text):
	text = re.sub("goto (.*)","<<display '\\1'>>\n<<display '_break'>>",text,flags=re.I)
	return text
def rnd (text):
	text = re.sub("<<set (.*)=\$rnd\*(.*)>>","<<random \\1 = \\2>>",text)
	return text
def proc (text):
	text = re.sub("proc (.*)","<<display '\\1'>>",text,flags=re.I)
	return text
def cls (text):
	if text.lower() == "cls":
		text = "<<clrscr>>"
	return text
def pause (text):
	text = re.sub("pause (\d+)","",text)
	return text
def label (text):
	if text == "": return text
	if text[0] == ':':
		text = re.sub(":(.*)","<<display '\\1'>>\n::\\1[::]1-1-1\n",text)
	return text
def pln (text):
	if text.lower() == "pln": text = "\n"
	if text[:4].lower() == "pln ":
		text = text[4:] + '\n'	
	if text[:2].lower() == "p ":
		text = text[2:].replace('#$',' ')
	return text
def btnstr (text):
	text = re.sub("^(.*)\[\[","\\1\n[[",text,flags=re.M)
	return text
def podst (text):
	text = re.sub("\#(\S+)\$","<<print $\\1>>",text)
	text = text.replace("#$","")
	return text
urqfile = clear(sys.argv[1])
smfile = open("hamster1.sm",'w')
urqfile = start(urqfile)
urqfile = btnuse(urqfile)
urqfile = end(urqfile)
list_par = urqfile.split("endendend")
resuilt = "\n"
resuilt = resuilt + inventory(urqfile)
for par in list_par:
	plist = par.strip().split('\n')
	plist[0] = name(plist[0])
	i = 1
	for ptext in plist[1:]:
		alist = ptext.split(" & ")
		j = 0
		for a in alist:
			a = ifthen(a)
			a = btn(a)
			a = inv(a)
			a = set(a)
			a = rnd(a)
			a = goto(a)
			a = proc(a)
			a = cls(a)
			a = pause(a)
			a = label(a)
			a = podst(a)
			a = pln(a)
			alist[j] = a
			j = j+1
		plist[i] = ' '.join(alist)
		i = i+1
	resuilt = resuilt + plist[0] + '\n' + ' '.join(plist[1:]) + '\n' + '\n'
resuilt = btnstr(resuilt)
resuilt = resuilt + perkill(resuilt)
resuilt = resuilt + "\n::_break[::]1-1-1\n-------------------\n"
smfile.write(resuilt.decode('cp1251').encode('utf8'))