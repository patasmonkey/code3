from xml.etree.ElementTree import *
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, parseString
import xml.dom.minidom as minidom
import time
import math
import sys
import argparse
import pickle
import codecs
tree=ET.parse('a.xml')
root=tree.getroot()
n_root=ET.Element('XcodeProgram')
shu_root=ET.Element('XcodeProgram')

IO=["getchar","gets","fgets","scanf","fputc","putc","putchar","fputs","puts","fprintf","printf"]
TAG=["body","exprStatement","functionCall","function","funcAddr"]
TAG1=["breakStatement","returnStatement","gotoStatement","statementLabel"]
DAINYU=["asgPlusExpr","asgMinusExpr","asgDivExpr","asgModExpr","asgLshiftExpr","asgRshiftExpr","asgBitAndExpr","asgBitOrExpr","asgBitXorExpr","assignExpr"]

kaisou=0

#st="<yanyan>\n"

line1=[]
line2=[]
for e in root.getiterator():
    a=e.items()
    for b in a:
        if(b[0]=='file'):
            f=0
            for c in line1:
                if(len(b[1])-2!=b[1].rfind('.c')):
                    f=1
                    break
                elif(len(b[1])-2==b[1].rfind('.c') and c!=b[1]):
                    f=2
                    break
            if(f==0):
                line1.append(b[1])
                line2.append(0)

parent_map=dict((c,p)for p in tree.getiterator() for c in p)

def funkcall_body(fele,fn_root):
    for e in list(fele):
        #print ("aaa  "+e.tag+":"+parent_map.get(e).tag)
        if(e.tag==TAG[1]):
            return funkcall_body(e,fn_root)
        elif(fele.tag==TAG[1] and e.tag==TAG[2]):
            return funkcall_body(e,fn_root)
        elif(fele.tag==TAG[2] and e.tag==TAG[3]):
            return funkcall_body(e,fn_root)
        elif(fele.tag==TAG[3] and e.tag==TAG[4]):
            for l in IO:
                if(l==e.text):
                    print("kitazo "+e.text)
                    return 1
    return 0
def hikaku(rr,ll):
    return 0

KEISAN=["plusExpr","minusExpr","mulExpr","divExpr","modExpr","LshiftExpr","RshiftExpr","bitAndExpr","bitOrExpr","bitXorExpr"]

def mk(eda):#assignExpr or asg
    num=0
    ll=[]
    if(eda.tag=="arrayRef"):
        for ez in eda.getiterator():
            ll.append(ez.tag)
            ll.append(ez.text)
        l=[s for s in ll if not s.endswith("    ")]
        #print("l",l)
    return ll

def kuraberu(eda,ll):
    rr=[]
    for e in eda.getiterator():
        rr.append(e.tag)
        rr.append(e.text)
    l=[s for s in ll if not s.endswith("  ")] 
    #print("ll",l)
    
    r=[s for s in rr if not s.endswith("  ")] 
    #print("rr",r)

    for i in range(len(r)):
        if("arrayAddr"==r[i-1]):
            if(r[i]!=l[i]):
                return 0
        elif(r[i]!=l[i]):
            print("out")
            return 1
    return 0


def mm(eda,ll):
    f=0
    for ee in list(eda):
        #print(ee.tag)
        if(ee.tag=="arrayRef"):
            f=kuraberu(ee,ll);
            if(f==1):
                break
        for zz in KEISAN:
            if(ee.tag==zz):
                return mm(ee,ll)
    return f

def Array_index(fele):#exprStatement
    f=rt=0
    for e in list(fele):#list(fele):#shiki
        for z in DAINYU:
            if(e.tag==z):
                f=0
                ll=[]
                for eda in list(e):#arr or asg
                    if(f==0):
                        ll=mk(eda)
                        f=1
                    else: 
                        rt=mm(e,ll)
            if(rt==1):
                break
        if(rt==1):
            break
    return rt


def funkcall(fele,fn_root):#forStatement
    for e in fele.getiterator():
        #print ("bbb  "+e.tag+":"+parent_map.get(e).tag)
        for l in TAG1:
            if(e.tag==l):
                return 1
        if(e.tag==TAG[0]):
            if(funkcall_body(e,fn_root)==1):
                return 1
        if(e.tag=="exprStatement" and Array_index(e)==1):
            return 1
    return 0



def pospra(ele,pos_root):#for no nakami forStatement
    f=1
    for e in list(ele):
        if(funkcall(e,pos_root)==1):#kiken innshi ga aru 1
            f=0
    return f #ireteyoi nara 1 damenara 0


def hantei(ele,ch_root,hkaisou):#pragma in or out
    global line1
    global line2
    a=ele.items()
    sw=yan=0
    for b in a:
        if(b[0]=='file'):
            for sw,c in enumerate(line1):
                if(c==b[1]):
                    break
        if(b[0]=='lineno'):
            yan=int(b[1])
            
    if(ele.tag=="forStatement" and pospra(ele,ch_root)==1):#can 1
        ele.set("praflag",str(hkaisou))
        print("ya_one_in!")
          

def itmm(ele,i_root,ff):
    global line1
    global line2
    a=ele.items()
    asd=0
    sw=0
    for b in a:
        if(b[0]=='file'):
            for sw,c in enumerate(line1):
                if(c==b[1]):
                    break
    for b in a:
        if(b[0]=='lineno'):
            asd=int(b[1])
            i_root.set(b[0],str(line2[sw]+asd))
        elif(b[0]=='praflag' and ff==2):
            b=b
        else:
            i_root.set(b[0],b[1])
         

def clook(ele,child_root,ckaisou):
    hantei(ele,child_root,ckaisou)
    child_root=ET.SubElement(child_root,ele.tag)
    if(ele.items()):
        itmm(ele,child_root,1)
    child_root.text=ele.text
    for e in list(ele):
        clook(e,child_root,ckaisou+1)        


for ele in list(root):
    clook(ele,n_root,kaisou+1)


string = ET.tostring(n_root, 'utf-8')
pretty_string = minidom.parseString(string).toprettyxml(indent='  ')
with open('output_ce.xml','w')as f:
    #f.write(st)
    f.write(pretty_string)






    

parent_map_=dict((c,p)for p in n_root.getiterator() for c in p)
    
def mini_clook_up(ku_cele,mc_root):#pragma gaareba 1
    if(parent_map_.get(ku_cele).tag == "forStatement"):
        a=parent_map_.get(ku_cele).items()
        for b in a:
            if(b[0]=='praflag'): 
                return 0
    elif(parent_map_.get(ku_cele).tag == "XcodeProgram"):
        return 1
    return mini_clook_up(parent_map_.get(ku_cele),mc_root)

def ku_hantei(ele,ch_root):#pragma in or out
    global line1
    global line2
    a=ele.items()
    sw=yan=0
    ff=0
    for b in a:
        if(b[0]=='file'):
            for sw,c in enumerate(line1):
                if(c==b[1]):
                    break
        if(b[0]=='lineno'):
            yan=int(b[1])
        if(b[0]=='praflag'):
            ff=1
    if(ele.tag=="forStatement" and mini_clook_up(ele,ch_root)==1 and ff==1):#can 1
        sub=ET.SubElement(ch_root,'pragma')
        sub.set('lineno',str(yan+line2[sw]))
        sub.text="acc karnels"
        line2[sw]+=1
        print("one_in!")


def kuwaeru(ele,child_root):
    ku_hantei(ele,child_root)
    child_root=ET.SubElement(child_root,ele.tag)
    if(ele.items()):
        itmm(ele,child_root,2)
    child_root.text=ele.text
    for e in list(ele):
        kuwaeru(e,child_root)        
    
for ele in list(n_root):
    kuwaeru(ele,shu_root)
    
string = ET.tostring(shu_root, 'utf-8')
pretty_string = minidom.parseString(string).toprettyxml(indent='  ')
with open('output.xml','w')as f:
    #f.write(st)
    f.write(pretty_string)
