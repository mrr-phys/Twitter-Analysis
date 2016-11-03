from __future__ import division
import twitter, json, sys, os, time, gzip
from pprint import pprint
from datetime import datetime
import operator
import geopy
from geopy.distance import vincenty
import tarfile, scipy.stats, math
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
from matplotlib.backends.backend_pdf import PdfPages
import networkx as nx
from scipy import integrate

####################################
#### Summary
# 1. Get the list of most popular sources
# 2. Selection of the "good" users and calculate distances
# 3. Places where users spend most of the time
# 4. Computation of travels and distances
# 5. Network representation
# 6. Various distributions 
# 7. Plots of graphs
######################################

# Raw data: tweets from Irak/Syria
data = '/Volumes//Projet2/Data/isis_tweets_full.dat.gz'

###############################
#### 1. Get the list of most popular sources (apps)
# sources = {}
# Ntweet = 0
# for line in gzip.open(data):
# 	Ntweet += 1
# 	if Ntweet % 1000000 == 0:
# 		print Ntweet
# 	try:
# 		# conversion of line in the files into json format
# 		tweet = json.loads(line.strip()) 
# 		user = tweet["user"]["id"]
# 		source = tweet["source"]
# 		if source not in sources:
# 			sources[source] = {}
# 		if user not in sources[source]:
# 			sources[source][user] = 1
# 		else:
# 			sources[source][user] += 1		
# 	except:
# 		pass 	

### Source, Nb users and Nb tweets for each line
# liste = []
# for source in sources.iterkeys():
# 	liste.append((source,len(sources[source]),sum(sources[source].values())))
# sorted_liste = sorted(liste,key=operator.itemgetter(1),reverse=True)

# file = open("Data/sources_user.dat", "w")
# for item in sorted_liste:
# 	print >> file,item[0].encode('utf8'),item[1],item[2]
# file.close()

### Remove the number of users and tweets
# file = open("Data/sources_only.dat", "w")
# for data in open("Data/sources.dat", "r"):
# 	length = len(data.strip().split())
# 	donnees = str(data.strip().split()[1:length-2])
# 	donnees = donnees.replace("'","")
# 	donnees = donnees.replace(",","")
# 	donnees = donnees.replace("[","")
# 	donnees = donnees.replace("]","")
# 	print >> file,donnees
# file.close()
#######################################


####################################
##### 2. Selection of the "good" users
# sourcelist = []
# for line in open("Data/sources_only.dat", "r"):
# 	source = line.strip()
# 	sourcelist.append(source)

# Nb = 0
# #Nbmax = 100000
# user_pos = {}
# for line in gzip.open(data):
# 	Nb += 1
# 	# print every number of lines
# 	if Nb % 1000000 == 0:
# 		print Nb
# 	#if Nb <= Nbmax:
# 	try:
# 		# conversion of line in the files into json format
# 		tweet = json.loads(line.strip()) 
# 		source = tweet["source"]

# 		if source in sourcelist:
# 			id_ = tweet["user"]["id"]		
# 			date = tweet["created_at"]
# 			# Conversion string to struct_time
# 			date = time.strptime(date,'%a %B %d %H:%M:%S +0000 %Y')
# 			# Makes the date into seconds since the epoch format
# 			date = int(time.mktime(date))
# 			# Remove users with strange coordinates (0,0)
# 			if "coordinates" in tweet and tweet["coordinates"] is not None \
# 			and (tweet["coordinates"]["coordinates"][0], \
# 			tweet["coordinates"]["coordinates"][1]) != (0.0,0.0): 
# 				x = tweet["coordinates"]["coordinates"][0]
# 				y = tweet["coordinates"]["coordinates"][1]

# 				if id_ not in user_pos:
# 					user_pos[id_] = []
# 				user_pos[id_].append((date,x,y))
# 	except:
# 		pass 
# 	#else:
# 	#	break		

# #### Remove the users with fake speed and calculate distances
# distances = []
# for user in user_pos.iterkeys():
# 	Npos = 0
# 	for pos in user_pos[user]:
# 		Npos += 1
# 		if Npos == 1:
# 			t1 = pos[0]
# 			place1 = pos[1:2]
# 		else:
# 			t2 = pos[0]
# 			if t2 != t1:
# 				place2 = pos[1:2]
# 				# In kms
# 				distance = vincenty(place1,place2).kilometers
# 				duration = (t2-t1)/3600
# 				speed = distance/duration
# 				# Remove users going faster than 900 km/h
# 				if speed <= 900:
# 					distances.append(distance)
# 					t1 = t2
# 					place1 = place2
# 				else:
# 					del user_pos[user][Npos-1]
# 			else:
# 				place2 = pos[1:2]
# 				distance = vincenty(place1,place2).kilometers	
# 				# Remove users going faster than 900 km/h = 250 m/s
# 				if distance <= 250:
# 					distances.append(distance)
# 					place1 = place2
# 				else:	
# 					del user_pos[user][Npos-1]

# file = open('Data/distances.dat','w')
# for dist in distances:
# 	print >> file,dist
# file.close()

# ### One file with one line per user : 
# file = open("Data/users_good.dat", "w")
# print >> file,"# ID , time , x , y , time , x , y ..."
# for user in user_pos.iterkeys():
# 	donnees = str(user_pos[user])
# 	donnees = donnees.replace(",","")
# 	donnees = donnees.replace("(","")
# 	donnees = donnees.replace(")","")
# 	donnees = donnees.replace("[","")
# 	donnees = donnees.replace("]","")
# 	print >> file,user,donnees
# file.close()	
##############################


###############################
#### 3. Places where users spend most of the time
# places = {}
# Nline = 0
# for line in open("Data/users_good.dat", "r"):
# 	Nline += 1
# 	if Nline > 1:
# 		data = line.strip().split()
# 		user = data[0]
# 		# list of beginning of periods indices
# 		period = []
# 		places[user] = []
# 		Nctot = int(len(data)/3)
# 		month = 3600*24*30.5
# 		duree = (int(data[3*(Nctot-1)+1]) - int(data[1]))/month
# 		thmo = 3*month
# 		n = 1
# 		while n < Nctot:
# 			t1 = int(data[3*(n-1)+1])
# 			t2 = int(data[3*n+1])
# 			dt = t2-t1
# 			if dt > thmo:
# 				period.append(n)
# 				n += 1
# 			else:
# 				while dt < thmo:
# 					n += 1
# 					if n == Nctot:
# 						break
# 					else:	
# 						t2 = int(data[3*n+1])
# 						dt = t2-t1
# 				period.append(n)	
# 				n += 1
# 		Nperiod = len(period)
# 		# remove last period which is less than 3 months
# 		if Nperiod > 2:
# 			period.remove(period[Nperiod-1])
# 		for index in period:
# 			dic = {}
# 			for n in range(index):
# 				x = round(float(data[3*n+2]),1)
# 				y = round(float(data[3*n+3]),1)
# 				place = (x,y)
# 				if place not in dic:
# 					dic[place] = 1
# 				else:
# 					dic[place] += 1 
# 			sorted_dic = sorted(dic.items(),key=operator.itemgetter(1),reverse=True)
# 			places[user].append(sorted_dic[0][0])

# placebis = {}
# for user in places.iterkeys():
# 	if len(places[user]) > 1 and places[user][0] != places[user][1]:
# 		if len(places[user]) == 3 and places[user][1] != places[user][2]:
# 			placebis[user] = (places[user][0],places[user][1])
# 			placebis[str(user+"bis")] = (places[user][1],places[user][2])
# 		else:
# 			placebis[user] = (places[user][0],places[user][1])
		
# placeter = {}
# for user1 in placebis.iterkeys():
# 	edge = placebis[user1]
# 	if edge not in placeter:
# 		placeter[edge] = 1
# 		for user2 in placebis.iterkeys():
# 			if user2 != user1 and placebis[user2] == edge:
# 				placeter[edge] += 1

# file = open('Data/users_most_time.dat','w')					
# for place in placeter.iterkeys():
# 	data = str(place)
# 	data = data.replace(",","")
# 	data = data.replace("(","")
# 	data = data.replace(")","")
# 	print >> file,data,placeter[place]
# file.close()						
		

#### in and out edges from Iraq/Syria	
inSI = []
outSI = []
for line in open('Data/users_most_time.dat','r'):
	data = line.strip().split()
	depart = (data[0],data[1])
	arrive = (data[2],data[3])
	poids = data[4]
	if float(depart[0]) > 25 and float(depart[1]) > 10 and \
	float(depart[0]) < 60 and float(depart[1]) < 45:
		outSI.append((depart,arrive,poids))
	if float(arrive[0]) > 25 and float(arrive[1]) > 10 and \
	float(arrive[0]) < 60 and float(arrive[1]) < 45:
		inSI.append((depart,arrive,poids))

file = open('Data/users_most_time_in.dat','w')
for edge in inSI:
	print >> file,edge[0][0],edge[0][1],edge[1][0],edge[1][1],edge[2]

file = open('Data/users_most_time_out.dat','w')
for edge in outSI:
	print >> file,edge[0][0],edge[0][1],edge[1][0],edge[1][1],edge[2]

# file = open("Data/most_visit_01.dat", "w")
# for user in places.iterkeys():
# 	print >> file,user,places[user][0][0],places[user][0][1],places[user][1]
# file.close()	
################################


###############################
#### 4. Computation of travels and distances
# travel = {}
# Nbpos = []
# times = []
# Nbtrav = 0

# Nline = 0
# for line in open("Data/users_ME.dat", "r"):
# 	Nline += 1
# 	if Nline > 1:
# 		data = line.strip().split()
# 		Nctot = int(len(data)/3)
# 		Nbpos.append(Nctot)
# 		Nc = 0
# 		for n in range(Nctot):
# 			Nc += 1
# 			if Nc == 1:
# 				t1 = int(data[3*n+1])
# 				i = round(float(data[3*n+2]),1)
# 				j = round(float(data[3*n+3]),1)
# 	        else:
# 	        	t2 = int(data[3*n+1])
# 	        	dt = (t2-t1)/3600/24
# 	        	times.append(dt)
# 	        	t1 = t2
# 	        	k = round(float(data[3*n+2]),1)
# 	        	l = round(float(data[3*n+3]),1)
# 	        	Nbtrav += 1
# 	        	trav = (i,j,k,l)
# 	        	if trav not in travel:
# 	        		travel[trav] = 1
# 	        	else:
# 	        		travel[trav] += 1
# 	        	i = k
# 	        	j = l

## Writing in a file
# file = open('Data/times.dat','w')
# for time in times:
# 	print >> file,time
# file.close()

# file = open('Data/Nbpos.dat','w')
# for Npos in Nbpos:
# 	print >> file,Npos
# file.close()

# file = open('Data/network_ME_users.dat','w')
# for trav in travel.iterkeys():
# 	# To remove the loops (people not moving)
# 	if trav[0] != trav[2] and trav[1] != trav[3]: 
# 	#and trav[0] > 25 and trav[0] < 60 and trav[2] > 25 and trav[2] < 60 \
# 	#and trav[1] > 10 and trav[1] < 45 and trav[3] > 10 and trav[3] < 45:
# 		print >> file,trav[0],trav[1],trav[2],trav[3],travel[trav]
# file.close()
####################################

#################################
#### 5. Network representation
#G = nx.DiGraph()
# G = nx.Graph()
# #in_G = nx.Graph()
# #out_G = nx.Graph()
# for line in open('Data/network_ME_users.dat','r'):
# 	trav = line.strip()
# 	x0 = float(trav.split()[0])
# 	y0 = float(trav.split()[1])
# 	x1 = float(trav.split()[2])
# 	y1 = float(trav.split()[3])
# 	poids = int(trav.split()[4])
# 	depart = (x0,y0)
# 	arrive = (x1,y1)
# 	# # All edges coming from Syria/Irak
# 	# if depart > (35,28) and depart < (48,37):
# 	# 	out_G.add_edge(depart,arrive,weight=1/poids)
# 	# # All edges going to Syria/Irak	
# 	# if arrive > (35,28) and arrive < (48,37):
# 	# 	in_G.add_edge(depart,arrive,weight=1/poids)	
# 	# By taking 1/poids, one obtains the Maximum Spanning Tree
# 	G.add_edge(depart,arrive,weight=1/poids)

# degrees = list(G.degree().values())
# #in_degrees = G.in_degree().values()
# #out_degrees = G.out_degree().values()

# MST = nx.minimum_spanning_tree(G)

# file = open("Data/network_ME_users_MaxST.dat", "w")
# for edge in MST.edges():
# 	x0 = edge[0][0]
# 	y0 = edge[0][1]
# 	x1 = edge[1][0]
# 	y1 = edge[1][1]
# 	poids = MST.get_edge_data(*edge)
# 	print >> file,x0,y0,x1,y1,poids['weight']
# file.close()
# degrees_MST = list(MST.degree().values())

#### Backbone graph
# def backbone(g, alpha):
#   backbone_graph = nx.Graph()
#   for node in g:
#       k_n = len(g[node])
#       if k_n > 1:
#           sum_w = sum( g[node][neighbor]['weight'] for neighbor in g[node] )
#           for neighbor in g[node]:
#               edgeWeight = g[node][neighbor]['weight']
#               pij = float(edgeWeight)/sum_w
#               if (1-pij)**(k_n-1) <= alpha: # equation 2
#               	backbone_graph.add_edge(node,neighbor,weight=edgeWeight)
#   return backbone_graph	
# bb = backbone(G,1)  

# file = open("Data/backbone_01.dat", "w")
# for edge in bb.edges():
# 	x0 = edge[0][0]
# 	y0 = edge[0][1]
# 	x1 = edge[1][0]
# 	y1 = edge[1][1]
# 	poids = bb.get_edge_data(*edge)
# 	print >> file,x0,y0,x1,y1,poids['weight']
# file.close()

#### List of normalized weights
Nbtrav = {}
for line in open('Data/network_world_01.dat','r'):
	travel = line.strip().split()
	origine = tuple(travel[0:2])
	arrival = tuple(travel[2:4])
	poids = int(travel[4])
	if origine not in Nbtrav:
 		Nbtrav[origine] = {}
 	if arrival not in Nbtrav[origine]:	
 		Nbtrav[origine][arrival] = poids 	
 
distance = [] 
norm_weights = [] 	
for origine in Nbtrav.iterkeys():
	sum_poids = sum(Nbtrav[origine].values())
	for arrival in Nbtrav[origine].iterkeys():
		distance.append(vincenty(origine,arrival).kilometers)	
		norm_weights.append(Nbtrav[origine][arrival]/sum_poids) 	

mat = zip(norm_weights,distance)

# # All weights
# dic = {}
# for line in mat:
# 	norm_weight = line[0]
# 	distance = line[1]
# 	if norm_weight not in dic:
# 		dic[norm_weight] = []
# 	dic[norm_weight].append(distance)

# 5 boxes of weights
dic = {}
for line in mat:
	norm_weight = line[0]
	distance = line[1]
	if norm_weight >= 0 and norm_weight < 0.2:
		if "0.1" not in dic:
			dic["0.1"] = []
		dic["0.1"].append(distance)		
	if norm_weight >= 0.2 and norm_weight < 0.4:
		if "0.3" not in dic:
			dic["0.3"] = []
		dic["0.3"].append(distance)	
	if norm_weight >= 0.4 and norm_weight < 0.6:
		if "0.5" not in dic:
			dic["0.5"] = []
		dic["0.5"].append(distance)	
	if norm_weight >= 0.6 and norm_weight < 0.8:
		if "0.7" not in dic:
			dic["0.7"] = []
		dic["0.7"].append(distance)	
	if norm_weight >= 0.8 and norm_weight <= 1:
		if "0.9" not in dic:
			dic["0.9"] = []
		dic["0.9"].append(distance)					
	
file = open('Data/distance_VS_normweight_box.dat','w')
for nw in dic.iterkeys():
	distances = str(dic[nw])
	distances = distances.replace(",","")
	distances = distances.replace("[","")
	distances = distances.replace("]","")
	print >> file,nw,distances	
file.close()

# file = open('Data/norm_weights_01.dat','w')
# for weight in norm_weights:
# 	print >> file,weight
# file.close()		
########################################


# ########################################
#### 6. Various distributions 
# choix = 8
# if choix == 0:
# 	distances = []
# 	for line in open("Data/distances.dat","r"):
# 		distances.append(float(line.strip()))
# 	vector = distances
# 	name = "distances"
# 	tbox = 10

# if choix == 1:
# 	times = []
# 	for line in open("Data/times.dat","r"):
# 		times.append(float(line.strip()))
# 	vector = distances
# 	name = "times"
# 	tbox = 20	

# if choix == 2:
# 	Nbpos = []
# 	for line in open("Data/Nbpos.dat","r"):
# 		Nbpos.append(int(line.strip()))
# 	vector = Nbpos
# 	name = "Nbpos"
# 	tbox = 1

# if choix == 3:
# 	weights = []
# 	for line in open("Data/network_world_01.dat","r"):
# 		weight = line.strip().split()[4]
# 		weights.append(int(weight))
# 	vector = weights
# 	name = "weights_01"
# 	tbox = 1	

# if choix == 4:
# 	norm_weights = []
# 	for line in open("Data/norm_weights_01.dat","r"):
# 		norm_weights.append(float(line.strip()))
# 	vector = norm_weights
# 	name = "norm_weights_01"
# 	tbox = 0.01

# if choix == 5:
# 	vector = in_degrees
# 	name = "in_degrees_01"
# 	tbox = 1

# if choix == 6:
# 	vector = out_degrees
# 	name = "out_degrees_01"
# 	tbox = 1	

# if choix == 7:
# 	vector = degrees	
# 	name = "degrees_01"
# 	tbox = 1

# if choix == 8:
# 	vector = degrees_MST
# 	name = "degrees_MST_01"
# 	tbox = 1			


##### Distributions computed by hand
### Log binning
# maximum = max(vector)
# minimum = min(vector)
# pas = np.logspace(math.log10(minimum),math.log10(maximum),num=100)
# dist = np.histogram(vector,bins=pas)

# with PdfPages("Graphs/logdist_"+name+".pdf") as pdf:
# 	plt.plot(dist[1][:-1], dist[0])
# 	plt.xscale('log')
# 	plt.yscale('log')
# 	plt.xlabel('Weights')
# 	plt.ylabel('Probability')

# 	pdf.savefig()
# 	plt.close()

##### Normal binning
# length = len(vector)
# maximum = max(vector)
# minimum = min(vector)
# Nbox = (maximum-minimum)/tbox
# distrib = {}
# for vect in vector:
#     boite = vect//tbox
#     if boite not in distrib:
#         distrib[boite] = 1
#     else:
#         distrib[boite] += 1

# x = []
# y = []

# for key in distrib.iterkeys():
#     x.append(tbox*(key+1/2))
#     y.append(distrib[key]/length)

# mat = zip(x,y)
# # to sort mat by x
# def getKey(item):
#     return item[0]
# mat = sorted(mat, key=getKey)

# # Writing them in a file
# file = open("Data/dist_"+name+".dat", "w")
# for coord in mat:
#     print >> file,coord[0],coord[1] 
# file.close()
################################################


#################################
### 7. Plots of graphs
# file = open("Data/dist_"+name+".dat", "r")

# x = []
# y = []

# for line in file:
# 	coord = line.strip()
# 	x.append(float(coord.split()[0]))
# 	y.append(float(coord.split()[1])) 

# with PdfPages("Graphs/dist_"+name+".pdf") as pdf:
# 	plt.plot(x,y)
# 	plt.xscale('log')
# 	plt.yscale('log')
# 	#plt.ylim(10**(-7),1.1)
# 	plt.xlabel('Degrees MST')
# 	plt.ylabel('Probability')

# 	pdf.savefig()
# 	plt.close()



