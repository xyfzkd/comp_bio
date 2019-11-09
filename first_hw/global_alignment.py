#!/usr/bin/env python
import sys
__author__  = 'wangyingjie'
__date__    = '2019/11/04'
__version__ = 'v1.0' 

def main(subject, query):
	import pdb
	match, mismatch, gap = 0, 1, 2

	pos_dict = {(i, j): 0 for i in range(len(subject)+1) for j in range(len(query)+1)}

	# Got the evaluation matrix
	for k in pos_dict:
		if not k[0] and not k[1]: 
			pos_dict[k] = 0
		elif not k[0] and k[1]: 
			pos_dict[k] = k[1] * gap
		elif not k[1] and k[0]:
			pos_dict[k] = k[0] * gap
	# print pos_dict
	import numpy as np
	pos_mat = np.ones((len(subject)+1,len(query)+1))
	# Dynamic programing for each position
	for i in range(1, len(subject)+1):
		for j in range(1, len(query)+1):
			
			up2down = pos_dict[(i-1, j)] + gap
			left2right = pos_dict[(i, j-1)] + gap
			if subject[i-1] == query[j-1]:
				topleft2bottomright = pos_dict[(i-1, j-1)] + match 
			else:
				topleft2bottomright = pos_dict[(i-1, j-1)] + mismatch
			pos_dict[(i, j)] = min(up2down, left2right, topleft2bottomright)
			pos_mat[i,j] = min(up2down, left2right, topleft2bottomright)
		
	
	# print matrix
	'''
	for i in range(len(subject)+1):
		temp = []
		for j in range(len(query)+1):
			temp.append(str(pos_dict[(i, j)]))
		print "\t".join(temp)
	'''

	# Backtracking
	out_subject, out_query = '', ""
	x, y = len(subject),len(query)
	initial = True
	while 1:
		if initial:
			out_subject += subject[x-1]
			out_query += query[y-1]
			initial = False
			x -= 1
			y -= 1	
		else:
			
			if not x and not y: break
			direct_dict = {      "up" : pos_dict[(x, y+1)]+2,
							"left" : pos_dict[(x+1, y)]+2,
						"top_left" : pos_dict[(x, y)]+1-(subject[x-1]==query[y-1])}
			#print direct_dict
			order = sorted(direct_dict.items(), key=lambda o:o[1], reverse=False)
			# only get one best path at this program, 
			# you can get all best path if you like
			
			if order[0][0] == "up":	  
				out_subject += subject[x-1]		
				out_query += "-"
				x -= 1
			elif order[0][0] == 'left': 
				out_query += query[y]
				out_subject += "-"
				y -= 1
			else:
				out_subject += subject[x-1]
				out_query += query[y-1]
				x -= 1
				y -= 1
	print(out_subject,out_query)		

##symbol and edit distance
	symbol = [] 
	gang = 0
	xing = 0
	kong = 0
	for i in range(len(out_subject)):
		if out_subject[i] == out_query[i]:
			symbol.append("|")
			gang += 1
		elif out_subject[i] != out_query[i] and out_subject[i] != "-" and out_query[i] != "-" :
			symbol.append("*")
			xing += 1
		else:
			symbol.append(" ")
			kong += 1
	ed_dis = gang * 0 + xing * 1 + kong * 2
	print(out_subject[::-1])
	print("".join(symbol[::-1]))
	print (out_query[::-1])
	print(ed_dis)

def fasta_to_list(filename='BJ01.fasta'):
    with open(filename) as f:
        a = f.readlines()
    return "".join([i[:-1] for i in a[1:]])






if __name__ == '__main__':
	# if len(sys.argv) == 1:
	# 	sys.exit("[usage] global_align.py <subject> <query>")
	# main(*sys.argv)
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--subject',type=str,default='BJ01.fasta')
	parser.add_argument('--query',type=str,default='TOR2.fasta')
	opt = parser.parse_args()
	main(fasta_to_list(opt.subject), fasta_to_list(opt.query))


