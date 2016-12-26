import re
import sys
from os import listdir
from os.path import isfile, join

def edit_distance(s1, s2):
    s1 = re.split(' |\n|\t', s1)
    s1 = filter(None, s1)
    s2 = re.split(' |\n|\t', s2)
    s2 = filter(None, s2)
    s1 = ' '.join(s1)
    s2 = ' '.join(s2)
#    print s1
#    print s2
    l1 = len(s1)
    l2 = len(s2)
    if l2 == 0:
        return l1
    previous_row = xrange(l2 + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        flag = 0
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return (float(previous_row[-1]),float(l2))

def ocr_ans(user, ground):
    userfiles = [ f for f in listdir(user) if isfile(join(user,f)) ]
    groundfiles = [ f for f in listdir(ground) if isfile(join(ground,f)) ]
    s = 0.0
    count = 0
    outputfile = open('output.txt','w+')
    for f in userfiles:
	f2 = (f.split('_'))[:-1]
        filename = ground + '/' + '_'.join(f2) + '.txt'
	print 'user : ',user + '/'+f
	userfile = open(user+'/'+f, 'r')
    	user_text = userfile.read()
	try:
   		user_text = user_text.decode('utf-8')
	except UnicodeDecodeError:
		try:
			user_text = user_text.decode('utf-16')
		except UnicodeDecodeError:
			continue
	print "ground : ",filename
	try:
	    	groundfile = open(filename, 'r')
    		ground_text = groundfile.read()
		try:
    			ground_text = ground_text.decode('utf-8')
		except UnicodeDecodeError:
			try:
				ground_text = ground_text.decode('utf-16')
			except UnicodeDecodeError:
				continue
	except IOError:
		continue
    	e = edit_distance(user_text, ground_text)
	s += e[0]/e[1]
	outputstring = '_'.join(f2) + '\t' + str(e[1]) + '\t' + str(e[0]) + '\t' + str(float(e[0])/float(e[1])*100) + '\n'
	outputfile.write(outputstring)
	count += 1
	print s,count
    print s/float(count)

ocr_ans(sys.argv[1], sys.argv[2])
