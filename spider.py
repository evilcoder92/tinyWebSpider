import os
import sys
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin
import argparse
def canbeadded(url):
       rx = True
       j = 0
       limit = len(expaths)
       while j < limit:
              path = expaths[j]
              if len(path) < len(url):
                     i = 0
                     test = True
                     while i < len(path):
                            if path[i] != url[i]:
                                   test = False
                            i = i + 1
                     if test == True:
                            rx = False
              j = j + 1
       return rx
def trueurl(url):
       char = '#'
       if char in url:
              ps = url.split(char)
              rx = ps[0]
       else:
              rx = url
       return rx
def InScope(url):
       parsed = urlparse(url)
       if parsed.netloc == netlocation:
              return True
       else:
              return False
def isinternal(url):
       parsed = urlparse(url)
       if parsed.scheme == '':
              return True
       else:
              return False
def getstatuscode(url):
       r = requests.get(url, headers = headers, allow_redirects=False)
       statuscode = str(r.status_code)
       return statuscode
def extractx(url):
       parsed = urlparse(url)
       basepath1 = parsed.scheme + '://' + parsed.netloc + '/'
       pathx = parsed.path
       pathy = pathx.split('/')
       ex = pathy[len(pathy) - 1]
       basepath2 = parsed.scheme + '://' + parsed.netloc + pathx
       basepath2 = basepath2.replace(ex, "")
       r = requests.get(url, headers = headers)
       html_doc = r.content
       soupx = BeautifulSoup(html_doc, 'html.parser')
       out = []
       for a in soupx.findAll('a'):
              atostring = a.encode('utf-8')
              if 'href' in atostring:
                     try:
                            href = a.attrs['href']
                     except Exception:
                            sdjfosidf = 0
                     hreftostring = href.encode('utf-8')
                     IsAbsolute = False
                     if isinternal(hreftostring) == True:
                            if len(hreftostring) > 0:
                                   if hreftostring != '/':
                                          if hreftostring != '//':
                                                 while hreftostring[0] == '/':
                                                        IsAbsolute = True
                                                        hreftostring = hreftostring[1:]
                                                 if IsAbsolute == True:
                                                        hreftostring = urljoin(basepath1, hreftostring)
                                                 else:
                                                        hreftostring = urljoin(basepath2, hreftostring)
                     if InScope(hreftostring) == True:
                            hreftostring = trueurl(hreftostring)
                            if canbeadded(hreftostring) == True:
                                   out.append(hreftostring)
       for form in soupx.findAll('form'):
              formtostring = form.encode('utf-8')
              if 'action' in formtostring:
                     action = form.attrs['action']
                     actiontostring = action.encode('utf-8')
                     IsAbsolute = False
                     if isinternal(actiontostring) == True:
                         if len(hreftostring) > 0:
                            if actiontostring != '/':
                                   if actiontostring != '//':
                                          while actiontostring[0] == '/':
                                                 IsAbsolute = True
                                                 actiontostring = actiontostring[1:]
                                          if IsAbsolute == True:
                                                 actiontostring = urljoin(basepath1, actiontostring)
                                          else:
                                                 actiontostring = urljoin(basepath2, actiontostring)
                     if InScope(actiontostring) == True:
                            actiontostring = trueurl(actiontostring)
                            if canbeadded(actiontostring) == True:
                                   out.append(actiontostring)
       count = len(out)
       j = 0
       limit = 0
       out2 = []
       while j < count:
              ee = out[j]
              i = 0
              duplicate = False
              while i < limit:
                     if ee == out2[i]:
                            duplicate = True
                     i = i + 1
              if duplicate == False:
                     out2.append(ee)
              limit = len(out2)
              j = j + 1
       return out2
                     
def tab2tab(entry):
       l = len(entry)
       i = 0
       back = []
       while i < l:
              x = extractx(entry[i])
              ll = len(x)
              j = 0
              while j < ll:
                     back.append(x[j])
                     j = j + 1
              i = i + 1
       returnx = []
       limit = 0
       k = 0
       count = len(back)
       while k < count:
              duplicate = False
              ee = back[k]
              kk = 0
              while kk < limit:
                     if ee == returnx[kk]:
                            duplicate = True
                     kk = kk + 1
              if duplicate == False:
                     returnx.append(ee)
              limit = len(returnx)
              k = k + 1
       return returnx

def crawlx(go, level):
       if level < maxlevel:
              if len(go) > 0:
                     gocount = len(go)
                     k = 0
                     while k < gocount:
                            scode = getstatuscode(go[k])
                            string = "['" + go[k] + "', '" + scode + "']"
                            command1 = 'echo "' + go[k] + '" >> targets/' + targetname + '/crawled.txt'
                            command2 = 'echo "' + string + '" >> targets/' + targetname + '/crawled2.txt'
                            if scode == '200':
                                   command3 = 'echo "' + go[k] + '" >> targets/' + targetname + '/200.txt'
                                   os.system(command3)
                            elif scode == '302':
                                   command4 = 'echo "' + go[k] + '" >> targets/' + targetname + '/302.txt'
                                   os.system(command4)
                            elif scode == '301':
                                   command5 = 'echo "' + go[k] + '" >> targets/' + targetname + '/301.txt'
                                   os.system(command5)
                            os.system(command1)
                            os.system(command2)
                            k = k + 1
                     crawled = []
                     imge = []
                     filex = 'targets/' + targetname + '/crawled.txt'
                     with open(filex, "r") as ins:
                            for line in ins:
                                   line = line.strip()
                                   crawled.append(line)
                     count = len(crawled)
                     back = tab2tab(go)
                     backcount = len(back)
                     i = 0
                     while i < backcount:
                            new = True
                            j = 0
                            while j < count:
                                   if back[i] == crawled[j]:
                                          new = False
                                   j = j + 1
                            if new == True:
                                   imge.append(back[i])
                            i = i + 1
                     imgecount = len(imge)
                     k = 0
                     content = ''
                     while k < imgecount:
                            content = content + imge[k] + '\n'
                            k = k + 1
                     filez = 'targets/' + targetname + '/image.txt'
                     with open(filez, 'w') as text_file:
                            text_file.write(content)
                     level = level + 1
                     crawlx(imge, level)
              else:
                     end_message1 = 'FINISHED'
                     print end_message1
       else:
              end_message2 = 'MAX LEVEL'
              print end_message2

useragentx = 'Mozilla/5.0 (X11; Linux i686; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4'
maxlevel = 100
DescriptionX = '''
Tiny Web Spider
Author : Saber Guenichi - saberguenichi92@gmail.com
'''
parser = argparse.ArgumentParser(description=DescriptionX)
parser.add_argument('-u','--url', help='starting url', required=True)
parser.add_argument('-n','--name', help='the target name', required=True)
parser.add_argument('-e','--execlude', help='the location of the file that contains paths they will execluded from the crawling process', default='e.txt')
parser.add_argument('-ua','--useragent', help='the UserAgent string', default=useragentx)
args = vars(parser.parse_args())

url = args['url']
targetname = args['name']
execludefile = args['execlude']
useragent = args['useragent']
headers = {
         'User-Agent': useragent
}
command00 = 'mkdir targets'
os.system(command00)
command0 = 'mkdir targets/' + targetname
os.system(command0)
expaths = []
with open(execludefile, 'r') as expathsx:
       for expathx in expathsx:
              expathx = expathx.strip()
              expaths.append(expathx)
parsed = urlparse(url)
netlocation = parsed.netloc
go = []
go.append(url)
try:
       crawlx(go, 0)
except KeyboardInterrupt:
       end_execution = True
       print 'finished by the user ..'
