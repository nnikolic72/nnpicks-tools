from __future__ import print_function
from __future__ import division
from instagram import client, subscriptions, InstagramAPI
import sys
from datetime import date, timedelta
import json
import time
import datetime
import operator
import shutil


debug_mode = 0


processed_users_db = "processed_users.txt"
results_users_db = "results_users.txt"
good_users_db = 'good_users.txt'
good_users_db_debug = 'good_users_debug.txt'
processed_users_db_backup = "processed_users.txt.backup"
results_users_db_backup = "results_users.txt.backup"
good_users_db_backup = 'good_users.txt.backup'

categories = ["abstract", "animals", "black and white", "architecture", "concert", "family", "fashion", \
              "fine art", "photojournalism", "landscape", "macro", "nature", "people", "sport", "still life", "portrait", \
              "street", "transportation", "travel", "underwater", "urbex", "misc", "reflexion", "cityscape"]

def pick_one_category():
    cat_list = "Categories: "
    for x in categories:
        buf = "[%s] %s  | " % (categories.index(x), x) 
        cat_list +=  buf
    print (cat_list)
    chosen_cats = raw_input("    * Pick a category: ")
    chosen_cats = chosen_cats.strip()  

    #print (chosen_cats_idx)
    return (categories[int(chosen_cats)])
    
try:
    shutil.copyfile(processed_users_db, processed_users_db_backup)
    shutil.copyfile(results_users_db, results_users_db_backup)
    shutil.copyfile(good_users_db, good_users_db_backup)
except:
    print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    sys.exit(0) 
    
proc_already = {}
try:
    fproc_already = open(processed_users_db,"r")
    proc_already = json.load(fproc_already)
    fproc_already.close()
    print("Loaded already processed keys %s" % len(proc_already.keys()))
except:
    print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    sys.exit(0) 
    

    
proc_already_rez = {}
try:
    fproc_already_rez = open(results_users_db,"r")
    proc_already_rez = json.load(fproc_already_rez)
    fproc_already_rez.close()
    print("Loaded results keys %s" % len(proc_already_rez.keys()))
except:
    print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    sys.exit(0) 
    
    
good_users = {}
try:
    fgood_users = open(good_users_db,"r")
    good_users = json.load(fgood_users)
    fgood_users.close()
    print("Loaded good users %s" % len(good_users.keys()))
except:
    print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    sys.exit(0)     
    
#print (proc_already_rez)
#print (type(proc_already))

# izlazni parametri - za print u bazu
jsonpar = proc_already
jsonrez = proc_already_rez

#access_token='1529897738.f4dfaeb.53403a45baed421ca216921b2f136c97';
access_token='1529897738.2d6fe64.87556684de0d4ce1aa6afbf423a8cada'
#'9ec9b4d0464f40ca85efd8dff3fa9636'


# =================== TAGS ===============================================================================
#search_names = ['wearegrryo']
#search_name = ['bnwlife']
#search_names = ['shootermag']
#search_names = ['justgoshoot']
#search_names = ['rising_masters']
#search_names = ['jj_forum_1023']
#search_names = ['exklusive_shot', 'ig_masterpiece', 'allshots_', 'hot_shotz', 'shotaward', 'ig_captures'
#                , 'big_shotz', 'ig_exquisite', 'igworldclub']
#search_names = ['stunning_shots']
#search_names = ['instagramsrbija', 'ig_belgrade', 'ig_zemun']
#search_names = ['instagramsrbija']
#search_names = ['srbija']
#search_names = ['beograd']

search_mode = 'users' # 'users' / 'tags' / 'users_in_photo' / 'recent_likers'


min_times_analyzed = float('inf')
min_times_analyzed_search_name = ''
min_times_analyzed_userid = 0
if search_mode == 'users':
    picked_cat = pick_one_category()
    
    
    # find least analyzed good user
    for key, value in good_users.iteritems():
        if picked_cat in value[8]:
            times_analyzed = value[6]
            good_username = value[0]
            
            if times_analyzed < min_times_analyzed:
                min_times_analyzed = times_analyzed
                min_times_analyzed_search_name = good_username
                min_times_analyzed_userid = key
    

    if min_times_analyzed_search_name != '':
         search_names = [min_times_analyzed_search_name]
         print ('Found user to analyse %s (analyzed %s times before)' % (min_times_analyzed_search_name, min_times_analyzed))
         raw_input("Press Enter to continue...")
         good_users[min_times_analyzed_userid][6] += 1
    else:
        print ("Error: Did not find good user to analyse!")
        sys.exit(0)  
    
    
# treshold parameters
days_tr = 2 # pre koliko dana je postovao
tr_media_low = 50 # koliko najmanje slika mora da ima
tr_following_max = 900 # koliko njih followuje
tr_following_min = 100 # koliko njih followuje
tr_followers = 800 # koliko ga ljudi max followuje
tr_min_followers = 200 # koliko ga ljudi najmanje followuje

if debug_mode == 0:
    user_num_tr = 800 # koliko followera da ispita za "users"
else:
    user_num_tr = 10
    
tag_media_count_tr = 300 # koliko slika da analizira po tagu za "tags"
max_tagged_user_pics = 10 # koliko poslednjih slika iz grupe da analizira za "users_in_photo"
max_likers_pics = 12 # koliko poslednjih slika iz grupe da analizira za "likers"
max_likers_per_photo = 13 # koliko likera po skorasnjoj slici da ispita

api = InstagramAPI(access_token=access_token)

def is_empty(any_structure):
    if any_structure:
        #print('Structure is not empty.')
        return False
    else:
        #print('Structure is empty.')
        return True

f = open("instagram_followers.html","w")
f.write("<html>\n")
f.write("<body>\n")
if debug_mode == 1:
    f.write("<h1>DEBUG MODE</h1>\n")
      
user_candidates = {}
      
      
if search_mode == 'recent_likers':
    search_names = ['x']
for search_name in search_names:
    print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    if api.x_ratelimit_remaining == 0:
         print("Limit reached. Stopping!")
         sys.exit(0) 
         
    f.write('<h2>Found for ' + search_name + '</h2><br>\n')

    user_id = 0

    try:
        if search_mode == 'users':
            # search users
            user_search = api.user_search(q=search_name, count=1)
            print( user_search[0].username)
            
            if search_name == user_search[0].username:
                print ('Username to ID success for %s' % search_name)
                user_id = user_search[0].id
                print (user_id)
            else:
                print ('Username to ID failed for %s' % search_name)
            
            if not access_token:
                print ('Missing Access Token')
            
            stops = 0
            amt = 0
            user_followed_by, next = api.user_followed_by(user_id)
            while next and (stops==0):
                more_users, next = api.user_followed_by(with_next_url=next)
                user_followed_by.extend(more_users)
                amt = len(user_followed_by)
                print ("Found followers %s  " % amt)
                if amt > user_num_tr:
                    stops = 1
            
            for user in user_followed_by:
                userid = user.id.encode(sys.stdout.encoding, errors='replace')
                username = user.username.encode(sys.stdout.encoding, errors='replace')
                
                #print "Userid: %s \tUsername: %s " % (userid, username)
                if userid not in proc_already.keys():
                    user_candidates[userid] = [username, 0, 0, 0, 0, 0, 0, 3, search_name];
                else:
                    print("Skipping user_id %s, named '%s' -- already processed" % (userid, username))
                # username, media, follows, followed_by
                
        elif search_mode == 'tags':
            # search tags
            other_tags = {}
            stops = 0
            amt = 0
            tag_search, next_tag = api.tag_search(q=search_name)
            l_tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name, count=tag_media_count_tr)
            
            while next and (stops==0):
                more_tags, next = api.tag_recent_media(tag_name=tag_search[0].name, with_next_url=next)
                #print('debug 3 ' + tag_search[0].name)
                l_tag_recent_media.extend(more_tags)
                amt = len(l_tag_recent_media)
                print ("Found tagged media %s for tag " % amt, tag_search[0].name )
                if amt > tag_media_count_tr:
                    stops = 1
            
            #print('debug 3 ' + tag_search[0].name)
            for medias in l_tag_recent_media:
                userid = medias.user.id
                username = medias.user.username
                
                if userid not in proc_already.keys():
                    user_candidates[userid] = [username, 0, 0, 0, 0, 0, 0, 2, search_name];
                else:
                    print("Skipping user_id %s, named '%s' -- already processed" % (userid, username))    

                #print('debug 4 ' + tag_search[0].name)
                try:
                    if not is_empty(medias):
                        for tag_i in medias.tags:
                            tag_name = tag_i.name
                            #print('debug 5 ' + tag_search[0].name)
                            if tag_name in other_tags.keys():
                                other_tags[tag_name] = other_tags[tag_name] + 1
                            else:
                                other_tags[tag_name] = 1 
                except:
                    pass 
                    
        elif search_mode == 'recent_likers':
            media_feed, next = api.user_media_feed()
            counter = 0
            # while next and counter >= max_likers_pics:
            #    media_feed, next = api.user_media_feed(with_next_url=next)
            #    counter = len(media_feed)
            
            print('Analyzing %s medias for likers\n' % (len(media_feed)))
            
            for medias in media_feed:
                total_likes_count = 0            
                likes_count = 0
                print ('Media by %s has %s likes' %(medias.user.username, medias.like_count))    
                #print(medias.likes)
                mediaid = medias.id 
                all_likes = api.media_likes(media_id=mediaid, count=10)
                #print (len(all_likes))
                 
                
                for likers in all_likes:
                    likes_count += 1
                    total_likes_count += 1
                    userid = likers.id
                    username = likers.username
                    
                    #print ('Processing like by %s' % username)
                    #sys.exit(0)
                    if userid not in proc_already.keys():
                        user_candidates[userid] = [username, 0, 0, 0, 0, 0, 0, 1, 'recent likers'];
                    else:
                        print("Skipping user_id %s, named '%s' -- already processed" % (userid, username)) 

                    if likes_count >= max_likers_per_photo:
                        print('Processed %s likers for this photo\n' % likes_count)
                        break;
                        
            print('Processed %s likes\n' % total_likes_count)
            
        elif search_mode == 'users_in_photo':
            counter = 1
            recent_media, next = api.user_recent_media(user_id=key, count=1)
            # max_tagged_user_pics
            while next and counter <= max_likers_per_photo:
                media_feed, next = api.user_recent_media(with_next_url=next)
                counter += 1
                
               
        print('Showing popular tags:')
        i = 0
        try:
            sorted_tags = sorted(other_tags.items(), key=operator.itemgetter(1), reverse=True)
            for tag_i, value in sorted_tags:
                print(tag_i + ' : ' + str(value))
                i += 1
                if i == 11:
                    break
        except:
            pass
       
    except Exception, e:
        print (e)
#print user_candidates
#print "*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit)
    
# iteracija kroz dictionary za sve followere
print('User candidates %s' % (len(user_candidates)))
for key, value in user_candidates.iteritems():
    try:
        user_data = api.user(key)
        follows = user_data.counts['follows']
        median = user_data.counts['media']
        followed_by = user_data.counts['followed_by']
        has_recent = 0
        
        if (median >= tr_media_low) and (followed_by <= tr_followers) and (followed_by > tr_min_followers) \
        and (tr_following_min <= follows <= tr_following_max):
            recent_media, next = api.user_recent_media(user_id=key, count=1)
            # kad je poslednja slika uploadovana
            has_recent = 0
            for media in recent_media:
                #print media.created_time.date()
                #print date.today() - timedelta(days=2)
                if media.created_time.date() > (date.today() - timedelta(days=days_tr)):
                    has_recent = 1
                else:
                    has_recent = 0
               
        ts = time.time()
        orig_source = user_candidates[key][7]
        orig_source_name = user_candidates[key][8]
        user_candidates[key] = [value[0], median, followed_by, follows, has_recent, user_id, datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), orig_source, orig_source_name]
    except Exception, e:
            pass
            #print e         
     
#print "*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit)   



#################################################################################
### MAIN LOOP 
#################################################################################
for key, value in user_candidates.iteritems():
    if value[2] != 0:
        ratio = value[3]/value[2]
    else:
        ratio = 0
        
    if (value[1] >= tr_media_low) and (value[2] <= tr_followers) and (value[2] > tr_min_followers) and (tr_following_min <= value[3] <= tr_following_max) and (value[4] == 1) and (ratio > 0.85):
         buf  = "Username: %s <br>Media: %-5s Followers: %-5s Following: %-5s Ratio: %1.5f <br>" % (value[0], value[1], value[2], value[3], ratio )
         print (buf)
         
         f.write('<a href="http://iconosquare.com/viewer.php#/user/' + key + '/">' + value[0] + '</a> '  + buf + '<br>\n')
         jsonpar[key] = value
         jsonrez[key] = [0, value[0]]
         
         #Get recent popular thumbs of this user
         media_list = {}
         try:
             final_recent_media, x_next = api.user_recent_media(user_id=key, count=10)
             for x_media in final_recent_media:
                  media_list[x_media.id] = x_media.like_count
                  #buf2 = "<a href=''><img src='%s'/></a>" % (x_media.get_thumbnail_url())
                  #f.write(buf2)              
                  #print (buf2)
             sorted_media_list = sorted(media_list.items(), key=operator.itemgetter(1), reverse=True)  
         except:
             pass
         cnt = 0
         for k,v in sorted_media_list:
              mediaurl = ""
              for x_media2 in final_recent_media: 
                   if k == x_media2.id:
                       mediaurl = x_media2.get_thumbnail_url()
              buf2 = "<a href='http://iconosquare.com/viewer.php#/detail/%s'><img src='%s'/></a>\n" % (k, mediaurl)               
              f.write(buf2)
              cnt += 1
              if cnt > 4:
                  break
                  
         buf2= "<br><br>"
         f.write(buf2)
         #fparams.write(str(key) + ',' + value[0] + ',' + str(value[1]) + ',' + str(value[2]) + ',' + str(value[3]) + ',' + str(value[4]) )
         #fresults.write(str(key) + ',' + value[0] + ',0')

if debug_mode == 0:
    fparams = open(processed_users_db,"w")
    fresults = open(results_users_db,"w")  
    json.dump(jsonpar, fparams, sort_keys=True, indent=4, separators=(',', ': '))
    json.dump(jsonrez, fresults, sort_keys=True, indent=4, separators=(',', ': '))
    fgood_users = open(good_users_db,"w")
    json.dump(good_users, fgood_users, sort_keys=True, indent=4, separators=(',', ': '))    
else:
    fgood_users = open(good_users_db_debug,"w")
    json.dump(good_users, fgood_users, sort_keys=True, indent=4, separators=(',', ': '))     
    
    
#print(jsonpar)
#print(jsonrez)
 
f.write('</body>\n')
f.write('</html>\n')         
f.close()
if debug_mode == 0:  
    fparams.close()  
    fresults.close() 
    fgood_users.close()
else:
    fgood_users.close()
print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
