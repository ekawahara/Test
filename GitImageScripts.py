import sys
import os
import re
import subprocess


f = open("images.txt", "w")
f.close()
f = None
'''
def findImages(top_directory):
    """Walk the 'top_directory' recursively and find all pngs and jpgs"""
    
    paths = []
    l = [(root, dirs, files) for root, dirs, files in os.walk('.') if not (('.svn' in root) or ('build' in root))]
    
    for s in l:
        fnames = s[2]
        paths += [ os.path.join(s[0], name) for name in fnames if ( name.endswith(".jpg") or name.endswith(".JPG") or name.endswith(".png") or name.endswith(".PNG")) ]
    
    return paths
'''

def getImages():
    image_types = ['jpg', 'JPG', 'png', 'PNG', 'gif', 'tif', 'tiff']
    image_paths =[]

    cmd = 'git show --diff-filter=AM --pretty=\"format:\" --name-only HEAD'
    x = os.popen(cmd)
    y = x.readlines()
    c = ''.join(y)
    d = c.split('\n')

    for fName in d:
        if fName.rsplit(".")[-1] in image_types:
            image_paths.append(fName)

    return image_paths

def getModifiedImages():
    image_types = ['jpg', 'JPG', 'png', 'PNG', 'gif', 'tif', 'tiff']
    image_paths =[]

    cmd = 'git show --diff-filter=M --pretty=\"format:\" --name-only HEAD'
    x = os.popen(cmd)
    y = x.readlines()
    c = ''.join(y)
    d = c.split('\n')

    for fName in d:
        if fName.rsplit(".")[-1] in image_types:
            image_paths.append(fName)

    return image_paths

def checkRatio(pathList):
    """Compare the file extension with the format of the actual image and see if they match"""
    c = 0
    for f in pathList:
        print f
        if('@2x' in f):
            f1 = f.replace('@2x', '')
            f2 = f
        else:
            x = f.rsplit('.', 1)
            f2 = x[0]+'@2x.'+x[1]
            f1 = f
        
        if os.path.exists(f1) and os.path.exists(f2):
              
            cmd1 = 'sips -g pixelHeight -g pixelWidth %s' % (f1)
            cmd2 = 'sips -g pixelHeight -g pixelWidth %s' % (f2)

            
            info1 = os.popen(cmd1).readlines()
            info2 = os.popen(cmd2).readlines()
            
            h1 = int(info1[1].strip('pixelHeight: '))
            w1 = int(info1[2].strip('pixelWidth: '))
            
            h2 = int(info2[1].strip('pixelHeight: '))
            w2 = int(info2[2].strip('pixelWidth: '))
        
            if (h2 != 2*h1) or (w2 != 2*w1):
                if c == 0:
                    out = "The following images do not have a pixel ratio of 2.0:\n"
                    g = open("images.txt","a")
                    g.write(out)
                    g.close()
                    g=None
                    c += 1
                g = open("images.txt","a")
                new_f = f + "\n"
                g.write(new_f)
                g.close()
                g=None
                



def checkExtension(pathList):
    """Compare the file extension with the format of the actual image and see if they match"""
    c = 0
    for f in pathList:
        '''
        print f
        f = re.sub('\ ', ' ', f)
        f = re.sub(' ', '\ ', f)
        f = re.sub('\(', '\(', f)
        f = re.sub('\)','\)',f)
        '''
        cmd = 'sips -g format \"%s\"' % (f)
        j = os.popen(cmd).readlines()
        f1 = f.rsplit(".")
        #print f1
        #print j
        ext = j[1].strip('format: ').strip('\n')
        if ext.lower() == 'jpeg':
            ext = 'jpg'
        if ext != f1[-1].lower():
            if c == 0:
                out = "The following images have a file extension that doesn't match its actual format:\n"
                g = open("images.txt","a")
                g.write(out)
                g.close()
                g=None
                c += 1
            g = open("images.txt","a")
            new_f = f + "\n"
            g.write(new_f)
            g.close()
            g=None


def checkMatch(pathList):
    """Compare the 2x  extension with the format of the actual image and see if they match"""
    c = 0
    for f in pathList:
        print f
        if('@2x' in f):
            f1 = f.replace('@2x', '')
        
            if os.path.exists(f) and not os.path.exists(f1):
                if c == 0:
                    out = "The following 2x images do not have a matching 1x image:\n"
                    g = open("images.txt", "a")
                    g.write(out)
                    g.close()
                    g = None
                    c += 1
                g = open("images.txt", "a")
                new_f = f + "\n"
                g.write(new_f)
                g.close()
                g = None


def checkIt(fileName, revNumber):
    '''
    f = re.sub('\ ', ' ', fileName)
    f = re.sub(' ', '\ ', fileName)
    f = re.sub('\(', '\(', fileName)
    f = re.sub('\)','\)',fileName)
    '''
    #print f
    cmd = 'git checkout %s \"%s\"' % (revNumber, fileName)
    #cmd
    #print cmd
    os.popen(cmd)
    #subprocess.call(["git checkout", '%s' % (revNumber), '%s' % (fileName)], shell=True)

def get_size(fileName):
    b = os.path.getsize(fileName)
    result = int(b)
    return result

def comparison(fileName, ext, rev):
    MAX_PERCENT_DIFFERENCE = 20
    MAX_SIZE_DIFFERENCE = 102400
    print fileName
    
    new_size = get_size(fileName)
    print new_size

    checkIt(fileName, rev)
    old_size = get_size(fileName)
    print old_size

    cmd = 'git checkout HEAD \"%s\"' % (fileName)
    #subprocess.call(["git checkout", "HEAD", "%s" % (fileName)], shell=True)
    os.popen(cmd)
    
    if(new_size > old_size):
        size_difference = new_size - old_size
        print size_difference
        percent_difference = ((new_size - old_size)/float(old_size))*100
        print percent_difference
        if percent_difference > MAX_PERCENT_DIFFERENCE and size_difference > MAX_SIZE_DIFFERENCE:
            out = "The following images have a dramatic increase in size and may want to be reviewed:\n%s\nThe file is now %d bytes\nBut previously, it was %d bytes\n" % (fileName, new_size, old_size)
            g = open("images.txt","a")
            g.write(out)
            g.close()
            g = None
                 
    else:
        size_difference = old_size - new_size
        print size_difference
        percent_difference = ((old_size - new_size)/float(old_size))*100
        print percent_difference
        if percent_difference > MAX_PERCENT_DIFFERENCE and size_difference > MAX_SIZE_DIFFERENCE:
            out = "The following images have a dramatic increase in size and may want to be reviewed:\n%s\nThe file is now %d bytes\nBut previously, it was %d bytes\n" % (fileName, new_size, old_size)
            g = open("images.txt","a")
            g.write(out)
            g.close()
            g = None


def final_check(pathList):
    cmd = 'git log'
    f = os.popen(cmd)
    log = f.readlines()
    f.close()
    f = None
    count = 1
    for row in log:
        if row[0:6] == 'commit':
            if count == 2:
                previous = row.split()[-1]
                break
            else:
                count += 1

    
    for f in pathList:
        ext = f.rsplit('.')[-1]
        comparison(f, ext, previous)


p = getImages("Test")
g = getModifiedImages()

print p
print g

if len(p):
    checkRatio(p)
    checkExtension(p)
    checkMatch(p)
if len(g):
    final_check(g)

