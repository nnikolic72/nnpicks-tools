from __future__ import print_function
from __future__ import division
from instagram import client, subscriptions, InstagramAPI
import sys
from datetime import date, timedelta
import json
import time
import datetime
import shutil
import operator
from pylab import *

#access_token='1529897738.f4dfaeb.53403a45baed421ca216921b2f136c97'
access_token='1529897738.2d6fe64.87556684de0d4ce1aa6afbf423a8cada'
api = InstagramAPI(access_token=access_token)
print_all_users = 0

def is_empty(any_structure):
    if any_structure:
        #print('Structure is not empty.')
        return False
    else:
        #print('Structure is empty.')
        return True
        
        
#open source and results files
print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))

if api.x_ratelimit_remaining == 0:
     print("Limit reached. Stopping!")
     sys.exit(0) 
         
processed_users_db = "processed_users.txt"
results_users_db = "results_users.txt"
results_users_db_backup = "results_users.txt.backup"
shutil.copyfile(results_users_db, results_users_db_backup)
processed_users_db_csv = "processed_users.csv"
results_users_db_csv = "results_users.csv"


processed_users = {}
try:
    f_processed_users = open(processed_users_db, "r")
    processed_users = json.load(f_processed_users)
    f_processed_users.close()
    print("Loaded already processed keys: %s\n" % (len(processed_users.keys())))
except Exception as e:
    s = str(e)
    print("Error opening file %s : %s\n " % (processed_users_db, s))
    #print (s)
    print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    sys.exit(0)
    
results = {}
try:
    f_results = open(results_users_db, "r")
    results = json.load(f_results)
    f_results.close()
    print("Loaded results keys: %s\n" % (len(results.keys())))
    tried_users = len(results.keys())
except Exception as e:
    s = str(e)
    print("Error opening file %s : %s\n" % (results_users_db, s))
    #print(s)
    print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    sys.exit(0)    
    
# moj nalog i njegovi followeri
my_account = 'nnenads'

user_search = api.user_search(q=my_account, count=1)
print( user_search[0].username)

if my_account == user_search[0].username:
    #print ('Username to ID success for %s' % my_account)
    user_id = user_search[0].id
    print ("Found User id for %s : %s \n" % (my_account, user_id))
else:
    print ('Username to ID failed for %s\n' % (my_account))

if not access_token:
    print ('Missing Access Token\n')
    
# load my followers
stops = 0
amt = 0
user_followed_by, next = api.user_followed_by(user_id)

try:
    while next:
        more_users, next = api.user_followed_by(with_next_url=next)
        user_followed_by.extend(more_users)
except Exception as e:
    s = str(e)
    print("Error retreiving followers for %s : %s \n" % (my_account, s))
    print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    sys.exit(0)  

    
#repack my followers
user_candidates = {}
for user in user_followed_by:
    userid = user.id.encode(sys.stdout.encoding, errors='replace')
    username = user.username.encode(sys.stdout.encoding, errors='replace')
    
    #print "Userid: %s \tUsername: %s " % (userid, username)
    if userid not in user_candidates.keys():
        user_candidates[userid] = [username];
    else:
        print("Skipping user_id %s, named '%s' -- already processed" % (userid, username))
                    
                    
amt = len(user_followed_by)
print ("Found followers for %s batch count %s \n" % (my_account, amt))
print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))

#print (processed_users)
#print(type(processed_users))
new_collowers_cnt = 0
for userid, user_struct in user_candidates.iteritems():   
    #print "Userid: %s \tUsername: %s " % (userid, username)
    is_old_follower = False
    is_candidate = False
    
    if userid in results.keys():
        old_follower = results[userid]
        is_candidate = True
    
    if (is_candidate == True) and (old_follower[0] == 1):
        is_old_follower = True
        #print ('User "%s" is already a follower\n' % (old_follower[1]))
    
    if (is_old_follower != True):
        if userid in results.keys():
            results[userid][0] = 1;
            if userid in processed_users.keys():
                processed_user = processed_users[userid]
                
                
            if processed_user.__len__() > 8:
                source_name_x = processed_user[8]
            else:
                source_name_x = "Unknown"
        
            print ('User "%s" is a new follower! (%s)\n' % (user_struct[0], source_name_x))
            new_collowers_cnt += 1
        else:
            pass
            #print("Skipping user_id %s, named '%s' -- already processed" % (userid, username))
        
        
print ("Writing final results. Found %s new followers since last analysis!\n" % (new_collowers_cnt))

f = open(results_users_db, "w")
json.dump(results, f, sort_keys=True, indent=4, separators=(',', ': '))
f.close()

#
# Analysis part ========================================================================================================
#
'''
total_accepted = 0
total_has_followers = 0
total_is_following = 0

total_ratio = 0
total_asked = 0

total_by_source_type = {}
total_by_source_name = {}

total_accepted_by_source_type = {}
total_accepted_by_source_name = {}

ratio_distribution = {}
ratios_list = []
bucket = ['1-1.5', '1.5-2', '2-2.5', '2.5-3', '3-3.5', '3.5-4', '4+']
for b in bucket:
    ratio_distribution[b] = 0
'''
total_posts = 0
list_of_accepted = []
list_of_accepted.extend(['<table border="1" style="width:60%">\n'])
for key, rez in results.iteritems():
    
    seventh = ""
    eight = ""
    try:
        seventh = processed_users[key][7]
        eight = processed_users[key][8]
    except:
        pass
    
    ''' 
    if seventh not in total_by_source_type.keys():
        total_by_source_type[seventh] = 1
    else:
        total_by_source_type[seventh] += 1
        
    if eight not in total_by_source_name.keys():
        total_by_source_name[eight] = 1
    else:
        total_by_source_name[eight] += 1
    
       
    total_asked += 1 
    '''
    if rez[0] == 1:
        '''
        if seventh not in total_accepted_by_source_type.keys():
            total_accepted_by_source_type[seventh] = 1
        else:
            total_accepted_by_source_type[seventh] += 1
            
        if eight not in total_accepted_by_source_name.keys():
            total_accepted_by_source_name[eight] = 1
        else:
            total_accepted_by_source_name[eight] += 1
         
          
        total_accepted += 1
        total_has_followers += processed_users[key][2]
        total_is_following += processed_users[key][3]
        pom_ratio = processed_users[key][3]/processed_users[key][2]
        ratios_list.extend([pom_ratio])
        total_ratio += pom_ratio
        
        if (pom_ratio >= 1) and (pom_ratio < 1.5):
            ratio_distribution[bucket[0]] += 1
        if (pom_ratio >= 1.5) and (pom_ratio < 2):
            ratio_distribution[bucket[1]] += 1
        if (pom_ratio >= 2) and (pom_ratio < 2.5):
            ratio_distribution[bucket[2]] += 1
        if (pom_ratio >= 2.5) and (pom_ratio < 3):
            ratio_distribution[bucket[3]] += 1
        if (pom_ratio >= 3) and (pom_ratio < 3.5):
            ratio_distribution[bucket[4]] += 1
        if (pom_ratio >= 3.5) and (pom_ratio < 4):
            ratio_distribution[bucket[5]] += 1
        if (pom_ratio >= 4):
            ratio_distribution[bucket[6]] += 1               
            
        '''
        total_posts += processed_users[key][1]
        buf = "<td>%s </td> <td>%s </td>, <td>%s </td> <td>Followers: %s </td> <td>Following: %s </td>" % (processed_users[key][0], seventh, eight, processed_users[key][2], processed_users[key][3])
        list_of_accepted.extend(['<tr>'])
        list_of_accepted.extend([buf])
        list_of_accepted.extend(['</tr>'])
        if print_all_users == 1:
            buf = "User: %s, Source: %s, Source Name: %s" % (processed_users[key][0], seventh, eight)
            print (buf)

list_of_accepted.extend(['</table>\n'])

'''
acceptance_rate = 0.0
if tried_users != 0:
    acceptance_rate = ((total_accepted / tried_users) * 100)

rep1 = 'Tries %s | Accepted %s | Rate %3.2f %%' % (tried_users, total_accepted, acceptance_rate)
rep2 = 'Accepted stats: Avg media %3.2f | Avg followers %3.2f | Avg followings %3.2f | Avg Ratio %3.2f' % (total_posts/total_accepted, total_has_followers/total_accepted, total_is_following/total_accepted, total_ratio/total_accepted)
rep3 = 'Ratio distribution:<br> %s : %s <br> %s : %s <br> %s : %s <br> %s : %s <br> %s : %s <br> %s : %s <br> %s : %s <br>' % \
       (bucket[0], ratio_distribution[bucket[0]], bucket[1], ratio_distribution[bucket[1]], bucket[2], ratio_distribution[bucket[2]], \
       bucket[3], ratio_distribution[bucket[3]], bucket[4], ratio_distribution[bucket[4]], bucket[5], ratio_distribution[bucket[5]], \
       bucket[6], ratio_distribution[bucket[6]])
       


       
#figure(1, figsize=(6,6))
#ax = axes([0, 8, 0, 80])
#labels = '1', '2', '3', '4','5', '6', '7', '8', '9'
#fracs = [1,1.5,2,2.5,3,3.5,4,4.5,5]


def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

        
bins_x=(1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10)        
#hist(ratios_list, bins=50, normed=True)
#formatter = FuncFormatter(to_percent)
#gca().yaxis.set_major_formatter(formatter)
#show()
#savefig('foo.png')
#rep4 = "<img src=foo.png></img><br>"

#hold(False)
#for i in range(0, len(ratios_list)-1):
#    ratios_list[i] /= total_asked
#hist(ratios_list, bins=bins_x, normed=True)
#formatter = FuncFormatter(to_percent)
#gca().yaxis.set_major_formatter(formatter)
#show()
#savefig('foo1.png')
#rep7 = "<img src=foo1.png></img><br>"


#print (rep1)
#print (rep2)

f_results_csv = open(results_users_db_csv, "w")
for key, rez in results.iteritems():
    seventh = "999"
    eight = "x"
    try:
        seventh = processed_users[key][7]
        eight =  processed_users[key][8]       
    except:
        pass
    str = '%s,%s,%s,%s,%s,%s,%s\n' % (key,processed_users[key][1],processed_users[key][2], processed_users[key][3], seventh, eight, rez[0])
    f_results_csv.write(str)
f_results_csv.close()    


#print (total_by_source_type)
#print (total_by_source_name)

#print (total_accepted_by_source_type)
#print (total_accepted_by_source_name)
'''
f = open("results_page.html","w")
f.write("<html>\n")
f.write("<style>\n")
f.write("    * {\n")
f.write("      font-family: sans-serif;\n")
f.write("    }\n")
f.write("</style>\n")
f.write("<body>\n")
f.write("<h2>Report</h2><br>\n")
'''
f.write("<b>Overall report:</b><br>\n")
f.write(rep1 + "<br>\n")
f.write(rep2 + "<br>\n")
f.write(rep3 + "<br>\n")
#f.write(rep4 + "<br>\n")
f.write("<br>\n")

f.write("<b>Ratio by source type:</b><br>\n")
ratio = "1. By users : %s / %s (%2.2f %%)" % (total_accepted_by_source_type[3], total_by_source_type[3], (total_accepted_by_source_type[3]/total_by_source_type[3])*100)
f.write(ratio + "<br>\n")
ratio = "2. By tags : %s / %s (%2.2f %%)" % (total_accepted_by_source_type[2], total_by_source_type[2], (total_accepted_by_source_type[2]/total_by_source_type[2])*100)
f.write(ratio + "<br>\n")
ratio = "3. Recent likers : %s / %s (%2.2f %%)" % (total_accepted_by_source_type[1], total_by_source_type[1], (total_accepted_by_source_type[1]/total_by_source_type[1])*100)
f.write(ratio + "<br>\n")
ratio = "4. Unknown : %s / %s (%2.2f %%)" % (total_accepted_by_source_type[''], total_by_source_type[''], (total_accepted_by_source_type['']/total_by_source_type[''])*100)
f.write(ratio + "<br>\n")

f.write("<br>\n")
f.write("<b>Breakdown by accepted source name:</b><br>\n")
i = 0
#print (total_accepted_by_source_name)

for k,v in total_accepted_by_source_name.iteritems():
    i += 1
    source_name_pom = k
    if k == '':
        source_name_pom = 'Unknown'
    ratio = "%s. %s : %s / %s (%2.2f %%)" % (i, source_name_pom, v, total_by_source_name[k], (v / total_by_source_name[k] )*100)
    f.write(ratio + "<br>\n")

f.write("<br>\n")
f.write("<b>Breakdown by all source names:</b><br>\n")
i = 0
#print (total_accepted_by_source_name)
for k,v in total_by_source_name.iteritems():
    i += 1
    source_name_pom = k
    if k == '':
        source_name_pom = 'Unknown'
    total_pom = 0
    total_ratio = 0
    if k in total_accepted_by_source_name.keys():
        total_pom = total_accepted_by_source_name[k] 
        total_ratio = total_accepted_by_source_name[k] / v
    ratio = "%s. %s : %s / %s (%2.2f %%)" % (i, source_name_pom, total_pom, v, (total_ratio )*100)
    f.write(ratio + "<br>\n")

f.write('<br><b>Followers and following acceptance (red=no, green=yes):</b> <br>\n')    
hold(False)
# plot first success

plot_data_x = []
plot_data_y = []
for key, value in processed_users.iteritems():
    plot_color = 'green'
    if results[key][0] == 1:
        plot_data_x.extend([processed_users[key][2]])
        plot_data_y.extend([processed_users[key][3]])
    
scatter(plot_data_x, plot_data_y, c=plot_color, label='accepted', alpha=0.3, edgecolors='none')
savefig('bar2.png')
f.write("<img src=bar2.png></img><br>")

hold(False)
plot_data_x = []
plot_data_y = []
for key, value in processed_users.iteritems():
    plot_color = 'red'
    if results[key][0] == 0:
        plot_data_x.extend([processed_users[key][2]])
        plot_data_y.extend([processed_users[key][3]])
    
scatter(plot_data_x, plot_data_y, c=plot_color, label='refused', alpha=0.3, edgecolors='none')

savefig('bar1.png')
f.write("<img src=bar1.png></img><br>")
'''    
f.write('<br><b>List of accepted users:</b> <br>\n')
for lm in list_of_accepted:
    f.write(lm + '\n')
    
f.write('</body>\n')
f.write('</html>\n')         
f.close()