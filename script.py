import re
ctr = 1;
title_list = []
item_list = []
placeholder_dictionary = {}
with open("sampleitemlist.txt", "r") as fp:
    for line in fp:


	if len(line) > 1 :

	    new_item_match = re.match(r'ITEM\s(\d+)', line)

	    if new_item_match:
		#print new_item_match.group(1)
	    	#print new_item_match.group()
			placeholder_dictionary["item id"] = new_item_match.group(1).strip()

            else :

	    	attr_pair = line.split("=", 1)
		if attr_pair[0] == "Title":
		    title_list.append(attr_pair[1])

	    	try:

		    placeholder_dictionary[attr_pair[0]] = attr_pair[1].strip('\n')

	    	except IndexError:

		    	#print "No such thing exist"
				print "",

	else :

	    temp_dict = placeholder_dictionary
	    item_list.append(temp_dict)
	    ctr += 1
	    placeholder_dictionary = {}
	    #print "eccentric case spotted!"

'''
min, min_id, max, max_id = 99, 0, 0, 0

for item in item_list:
    l = len(item.keys())
    if min > l : min, min_id = l, int(item["item id"])
    if max < l : max, max_id = l, int(item["item id"])

print min, min_id
print max, max_id

print 'Title' in item_list[min_id - 1].keys()
print item_list[max_id - 1].keys()

print len(item_list)
for index in range(len(item_list)):
    item_id = int(item_list[index]["item id"])
    print item_id, index+1, item_id == index+1
'''
'''
for title in title_list:
    print title

real work begins '''


import pandas as pd

#Reading users file:
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('ml-100k/u.user', sep='|', names= u_cols, encoding='latin-1')

#Reading ratings file:
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=r_cols, encoding='latin-1')

#Reading items file:
i_cols = ['movie id', 'movie title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

items = pd.read_csv('ml-100k/u.item', sep='|', names=i_cols, encoding='latin-1')


print users.shape
#print users.head()

print ratings.shape
#print ratings.head()


print items.shape
#print items.head()


r_cols = ['user_id', 'product_id', 'rating', 'unix_timestamp']

ratings_base = pd.read_csv('ml-100k/ua.base', sep='\t', names=r_cols, encoding='latin-1')
ratings_test = pd.read_csv('ml-100k/ua.test', sep='\t', names=r_cols, encoding='latin-1')

#print ratings_base.shape, ratings_test.shape

import graphlab

train_data = graphlab.SFrame(ratings_base)
test_data = graphlab.SFrame(ratings_test)

#print train_data
#print test_data

item_sim_model = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='product_id', target='rating', similarity_type='pearson')

#item_sim_recomm = item_sim_model.recommend(users=range(1,6),k=5)
#item_sim_recomm.print_rows()


print "\n\n\n\n\n \t\t\txxxxxxxxxxBEGINxxxxxxxxxx\n\n";
userid = raw_input("What user id to recommend for ?")
item_sim_recomm = item_sim_model.recommend(users=range(int(userid), int(userid)+1),k=5)

print "\n\nTOP 5 RECOMMENDATIONS FOR USER ID %s ...\n\n" %userid

print "PRODUCT ID\tPRODUCT NAME\n\n";

for i in range(5):
	print "%s\t\t%s" % (item_sim_recomm[i]['product_id'], title_list[item_sim_recomm[i]['product_id']])



#print item_list[0], item_list[1]
#item.sim.model.predict(test_data)
#item_sim_model.recommend()

'''
Recall:
What ratio of items that a user likes were actually recommended.
If a user likes say 5 items and the recommendation decided to show 3 of them, then the recall is 0.6

Precision
Out of all the recommended items, how many the user actually liked?
If 5 items were recommended to the user out of which he liked say 4 of them, then precision is 0.8
'''

