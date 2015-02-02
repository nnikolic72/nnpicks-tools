from __future__ import print_function
from __future__ import division
from instagram import client, subscriptions, InstagramAPI
import sys
sys.path.append('..')
sys.path.append('C:\bin')
sys.path.append('C:\bin')

from datetime import date, timedelta
import json
import time
import datetime
import shutil
import operator
from pylab import *
import math
import matplotlib.pyplot as plt

import networkx as nx

from bottle import *

picked_pic_db = 'db_nnpicks.txt'
picked_pic_db_backup = 'db_nnpicks.txt.backup'
picked_pic_db_debug = 'db_nnpicks_debug.txt'
good_users_db = 'good_users.txt'
good_users_db_debug = 'good_users_debug.txt'
great_pics_db = "great_pics.txt"
great_pics_db_debug = "great_pics_debug.txt"
network_db = 'db_network.txt'
network_db_backup = 'db_network.txt.backup'
network_db_debug = 'db_network_debug.txt'
access_token='1529897738.2d6fe64.87556684de0d4ce1aa6afbf423a8cada'
api = InstagramAPI(access_token=access_token)
HOST = 'localhost'

debug_mode = 0
first_run = False
try:
    shutil.copyfile(picked_pic_db, picked_pic_db_backup)
except:
    print("Error during backup. Exiting.")
    print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    sys.exit(0) 
    
menu = {}
menu["HOME"] = "/"
menu["GOOD USERS"] = "/good-users"
menu["EXHIBITIONS"] = "/exhibitions"
menu["PICKED PICTURES"] = "/pictures"
menu["GOOD PICTURES"] = "/good-pictures"
menu["FIND TALENT"] = "/find_talent"
menu["SAVE"] = "/save"
menu["NETWORK"] = "/network"
menu["NN Picks Buidup"] = "/nnpicks-shadow"

categories = ["abstract", "animals", "black and white", "architecture", "concert", "family", "fashion", \
              "fine art", "photojournalism", "landscape", "macro", "nature", "people", "sport", "still life", "portrait", \
              "street", "transportation", "travel", "underwater", "urbex", "misc", "reflection", "cityscape", "minimalism"]
              
exhibitions = ["Street Clicks", "Landscape", "People", "Black and White", "Portrait"]
rooms = ["One", "Two", "Three", "Four", "Five"]



#find talent variables
get_max_followings = 500
#get_max_followings = 10
show_talents_max = 50
days_tr = 15
user_candidates = {}
my_followings = {}
my_user = 'nnenads'
essential_mode = False # da li gledamo samo one sa malo followingsa
essential_treshold = 200 # koliko najvise followingsa imamo u essential modu!
filter_good_users = True
filter_skip_users = True
skip_users = [ 'time',  'streetcolour', '24hourproject', 'instatone', 'life', 'shutdagizm', 'cityexposed', \
               'instagram', 'eucl']

#find best media variables              
tr_max_media = 100 # analyze last X pics
tr_max_media_individual = 500
skip_user = ['hikari.creative', 'tiny_collective', 'shootermag', 'wearegrryo', 'streetphotographers', 'the_corporation', 'outofthephone', \
             'causebeautiful', 'magnumphotos', 'mastersig', 'burndiary', 'streetbwcolor']
             
# network global variables
tr_network_followings = 2000
ghost_media = {}

ghost_follow_good_users = {}
               
picked_pics = {}
try:
    if not first_run:
        if debug_mode == 0:
            f_results = open(picked_pic_db, "r")
        else:
            f_results = open(picked_pic_db_debug, "r")
        
        picked_pics = json.load(f_results)
        f_results.close()
        print("Loaded picked pics: %s\n" % (len(picked_pics.keys())))
        picked_pics_cnt = len(picked_pics.keys())
except Exception as e:
    s = str(e)
    print("Error opening file %s : %s\n" % (picked_pic_db, s))
    print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    if not first_run:
        sys.exit(0)   

good_users = {}
try:
    if not first_run:
        if debug_mode == 0:
            f_results = open(good_users_db, "r")
        else:
            f_results = open(good_users_db_debug, "r")
            
        good_users = json.load(f_results)
        f_results.close()
        print("Loaded good users: %s\n" % (len(good_users.keys())))
        picked_pics_cnt = len(good_users.keys())
except Exception as e:
    s = str(e)
    print("Error opening file %s : %s\n" % (good_users_db, s))
    print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    if not first_run:
        sys.exit(0)      
        
best_media = {}
if not first_run:
    try:
        if debug_mode == 0:
            f_results = open(great_pics_db, "r")
        else:
            f_results = open(great_pics_db_debug, "r")
            
        best_media = json.load(f_results)
        f_results.close()
        print("Loaded best media keys: %s\n" % (len(best_media.keys())))
        tried_users = len(best_media.keys())
        
    except Exception as e:
        s = str(e)
        print("Error opening file %s : %s\n" % (great_pics_db, s))
        #print(s)
        if s != 'No JSON object could be decoded':
            print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
            sys.exit(0)           

user_network = {}
if not first_run:
    try:
        if debug_mode == 0:
            f_results = open(network_db, "r")
        else:
            f_results = open(network_db_debug, "r")
            
        user_network = json.load(f_results)
        f_results.close()
        print("Loaded user network keys: %s\n" % (len(user_network.keys())))
        user_network_len = len(user_network.keys())
    except Exception as e:
        s = str(e)
        print("Error opening file %s : %s\n" % (network_db, s))
        #print(s)
        if s != 'No JSON object could be decoded':
            print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
            #sys.exit(0)           




def linreg(x, y):
    regression = np.polyfit(x, y, 2)
    return regression

def prediction(regression, point):
    y = regression[0]*point + regression[1]
    return y
    
def max_distance(media_x, top_n):
    i = 0
    result = []
    media_distances = {}
    media_cnt = len(media_x)
    print ("Media count = %s" %(media_cnt))
    for x_media in media_x:
        media_distances[i] = [x_media.id, x_media.like_count, 0]
        i += 1
    
    linreg_x = []
    linreg_y = []
    for i in range (0, len(media_distances) - 1):
        linreg_x.extend([i])
        linreg_y.extend([media_distances[i][1]])
        
    regression = linreg(linreg_x, linreg_y)    
    polynomial = np.poly1d(regression) 
    predictions = polynomial(linreg_x)   
    
    hold(False)
    plot(linreg_x, linreg_y, 'o')
    hold(True)
    plot(linreg_x, predictions)
    ylabel('y')
    xlabel('x')
    savefig('static/best_pics.png')
    #show()
    
        
    print("Regression")
    print(regression)       
    skip_idx_list = []
    for c in range(1, top_n):
        max_distance_media = float("-inf")
        for i in range (0, len(media_distances) - 1):
            if i not in skip_idx_list:
                #y = prediction(regression, media_distances[i][1])
                y = predictions[i]
                
                #klasicno racunanje
                error = linreg_y[i] - y
               
                #racunanje odnosa
                if error < 0:
                    error = 0
                else:
                    error = (error*error) / y
                
                media_distances[i][2] = error
                if max_distance_media < error:
                    max_distance_media = error
                    max_distance_media_id = media_distances[i][0]
                    max_distance_media_idx = i
        
        skip_idx_list.extend([max_distance_media_idx])
        print (max_distance_media_id)
        result.append([max_distance_media_id, c])
        #print(result)
        
    return result
            
@route('/')
def main_page():
    return template('tpl_main_page', menu=menu)

    
@route('/test') 
def test():
    return '''
        <form action="/display-username" method="post">
            Username: <input name="username" type="text" />
            <input value="Display" type="submit" />
        </form>
    '''
 
@route('/save')
def savex():
    save = True
    picked_pics_db_saved = False
    if save == True:
        if debug_mode == 0:
            f_results = open(picked_pic_db, "w")
            json.dump(picked_pics, f_results, sort_keys=True, indent=4, separators=(',', ': ')) 
        else:
            f_results = open(picked_pic_db_debug, "w")
            json.dump(picked_pics, f_results, sort_keys=True, indent=4, separators=(',', ': '))     
        print("DATABASE SAVED!")
        picked_pics_db_saved = True
    
    good_users_db_saved = False
    if save == True:
        if debug_mode == 0:
            f_results = open(good_users_db, "w")
            json.dump(good_users, f_results, sort_keys=True, indent=4, separators=(',', ': ')) 
        else:
            f_results = open(good_users_db_debug, "w")
            json.dump(good_users, f_results, sort_keys=True, indent=4, separators=(',', ': '))     
        print("USERS DATABASE SAVED!") 
        good_users_db_saved = True
    
    great_pics_db_saved = False
    if save == True:
        if debug_mode == 0:
            f_results = open(great_pics_db, "w")
            json.dump(best_media, f_results, sort_keys=True, indent=4, separators=(',', ': ')) 
        else:
            f_results = open(great_pics_db_debug, "w")
            json.dump(best_media, f_results, sort_keys=True, indent=4, separators=(',', ': '))     
        print("BEST MEDIA DATABASE SAVED!") 
        great_pics_db_saved = True
        
    network_db_saved = False
    if save == True:
        if debug_mode == 0:
            f_results = open(network_db, "w")
            json.dump(user_network, f_results, sort_keys=True, indent=4, separators=(',', ': ')) 
        else:
            f_results = open(network_db_debug, "w")
            json.dump(user_network, f_results, sort_keys=True, indent=4, separators=(',', ': '))     
        print("USER NETWORK DATABASE SAVED!") 
        network_db_saved = True        
        
    return template('tpl_save_report', menux=menu, network_db_saved=network_db_saved, picked_pics_db_saved=picked_pics_db_saved, good_users_db_saved=good_users_db_saved,  great_pics_db_saved=great_pics_db_saved, debug_mode=debug_mode)
        
@route('/user-profile/<name>')
def displayusername(name):
    assert name.isalnum()
    new_username = name
    
    new_user_search = api.user_search(q=new_username, count=1)
    if new_username == new_user_search[0].username:
        print ('Username to ID success for %s' % new_username)
        photographer_id = new_user_search[0].id
    else:
        print ('Username to ID failed for %s' % new_username)
        print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    

    pom_user = api.user(photographer_id) 
    pom_user_follows = pom_user.counts[u'follows']
    pom_user_followed_by = pom_user.counts[u'followed_by']
    pom_user_media = pom_user.counts[u'media']
    pom_user_full_name = pom_user.full_name

        
    return template('tpl_user_profile', user_x=good_users[photographer_id], pom_user=pom_user, pom_user_follows=pom_user_follows, \
                    pom_user_followed_by=pom_user_followed_by, pom_user_media=pom_user_media, pom_user_full_name=pom_user_full_name, menu=menu)
    
@route('/static/<filename>', name='static')
def server_static(filename):
    return static_file(filename, root='static')

    
@get('/good-users') 
def show_good_users():    
    return template('tpl_good_users', good_users=good_users, categories=categories, menu=menu, get_url=url, user_network=user_network)   
    
@route('/exhibitions')
def show_exhibitions():    
    return template('tpl_exhibitions', exhibitions=exhibitions, menu=menu, get_url=url) 
    
@route('/exhibition/<name>')
def show_exhibition(name):    
    return template('tpl_exhibition', name=name, picked_pics=picked_pics, menu=menu, get_url=url) 

@get('/good-pictures') 
def show_good_pictures():    
    return template('tpl_good_pics', best_media =best_media, categories=categories, menu=menu, get_url=url)
    
@route('/pictures')
def show_pictures():    
    return template('tpl_pictures', picked_pics=picked_pics, good_users=good_users, menu=menu, get_url=url, categories=categories) 
    
@route('/pictures/<cat>')
def show_pictures_cat(cat):    
    return template('tpl_pic_category', cat=cat, picked_pics=picked_pics, good_users=good_users, menu=menu, get_url=url, categories=categories) 

@get('/good-users/<cat_in>') 
def show_good_users(cat_in):    
    return template('tpl_good_users_cat', category_name=cat_in, good_users=good_users, categories=categories, menu=menu, picked_pics=picked_pics, get_url=url, user_network=user_network)  

@route('/approved-pic/<pic_id>')
def set_picture_approved(pic_id):
    if pic_id not in picked_pics.keys():
        return template('tpl_error_report', api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url)
        
    picked_pics[pic_id][8] = 1
    print(picked_pics[pic_id])
    return template('tpl_picked_picture_approved', api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url,\
                                                   media_id=pic_id, username=picked_pics[pic_id][1], media_url=picked_pics[pic_id][9])
                                                   
    
    
@get('/nnpicks-shadow')
def nnpicks_shadow():
    #display users chosen to shadow-follow
    #From a pool of good users, filter out the ones that already follow nnpicks-shadow
    
    nnpicks_user = 'nnpicks'
    nnpicks_id = -1
    display_pictures_cnt = 1
    days_tr = 5 # determine if good user is active
    debug_shadow = 1
    ghost_min_followers = 800
    ghost_max_followers = 30000
    ghost_min_followings = 90
    ghost_max_followings = 1500
    
    ghost_follow_good_users.clear()
    print (ghost_follow_good_users)
    try:
        nnpicks_search = api.user_search(q=nnpicks_user, count=1)
    except Exception as e:
        s = str(e)
        print("Error nnpicks_shadow 001 : %s\n" % (s))
        nnpicks_search = None
        
    if nnpicks_user == nnpicks_search[0].username:
        print ('Username to ID success for %s' % nnpicks_user)
        nnpicks_id = nnpicks_search[0].id
    else:
        print ('Username to ID failed for %s' % nnpicks_user)
        print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))    
        return template('tpl_error_report', api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url)
        
    #read a list of followers of nnpicks_user
    
    try:
        nnpicks_followed_by, next = api.user_followed_by(nnpicks_id)    
        while next:
            more_users, next = api.user_followed_by(with_next_url=next)
            nnpicks_followed_by.extend(more_users)
            amt = len(nnpicks_followed_by)
            print ("Found followers %s  " % amt)
    except Exception as e:
        s = str(e)
        print("Error nnpicks_shadow 002 : %s\n" % (s))
        nnpicks_followed_by = None
        
    #filter out good users which are already followers
    
    i = 0
    for key, value in good_users.iteritems():
        user_already_follower = False
        for x in nnpicks_followed_by:
            if x.id == key:
                user_already_follower = True
                break
        
        if (user_already_follower == False):
            if (debug_shadow == 1) and (i <= 100):
                if key not in ghost_follow_good_users.keys():
                    ghost_follow_good_users[key] = good_users[key]
                    i = i + 1
                else:
                    pass
            
    #we have a list of users to ghost follow

    remove_inactive_ghost_users = []
    for key, value in ghost_follow_good_users.iteritems():
        
        ghost_media.clear()
        #print(ghost_media)
        try:
            user_data = api.user(key)
        except Exception as e:
            s = str(e)
            print("Error nnpicks_shadow 004 : %s\n" % (s))
            user_data = None
            continue

        
        ghost_user_name = user_data.username
        follows = user_data.counts['follows']
        media_num = user_data.counts['media']
        followed_by = user_data.counts['followed_by']
        has_recent = 0
        
        recent_media = None
        try:
            recent_media, next = api.user_recent_media(user_id=user_data.id, count=1)
        except Exception as e:
            s = str(e)
            print("Error nnpicks_shadow 003 : %s\n" % (s))
            recent_media = None
            continue

        
        print(recent_media)
        # kad je poslednja slika uploadovana
        has_recent = 0
        for media in recent_media:
            if media.created_time.date() > (date.today() - timedelta(days=days_tr)):
                has_recent = 1
                print ("has recent %s " % (ghost_user_name))
                break
        
        #da li se korisnik kvalifikuje kao potencijal za ghost followings
        ghost_qualifies = False
        if (ghost_min_followings <= value[3] <= ghost_max_followings) and (ghost_min_followers <= value[4] <= ghost_max_followers):
            ghost_qualifies = True
        
        ghost_media.clear()
        if (has_recent == 1) and (ghost_qualifies == True):   
            recent_media, next = api.user_recent_media(user_id=key, count=10)

            for media in recent_media:
                #if media.created_time.date() > (date.today() - timedelta(days=2)):
                    ghost_media[media.id] = [ghost_user_name, media.get_thumbnail_url(), media.created_time.date()]
                    ghost_follow_good_users[key].extend([media.id])
                    ghost_follow_good_users[key].extend([ ghost_media[media.id]])
                #else:
                #    remove_inactive_ghost_users.extend([key])
                
        else:
            remove_inactive_ghost_users.extend([key])
            
    for x in remove_inactive_ghost_users:
        ghost_follow_good_users.pop(x, None)
     
    #print(ghost_follow_good_users)        
    for key, value in ghost_follow_good_users.iteritems():
        print (value)
        
    return template('tpl_pic_like', disp_media = ghost_follow_good_users, api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url) 

@post('/submit_picture/<pic_id>')
def submit_picked_picture(pic_id):
    picture_id = pic_id     
    picture_id = picture_id.strip()

    try:
        add_media = api.media(media_id = picture_id)
        media_found = True
    except:
        print("    * media search for ID = %s failed." % (picture_id))
        return template('tpl_error_report', api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url)
        media_found = False
        
    if picture_id in picked_pics.keys():
        print("    * Picture %s already in the database! Updating." % (pic_id))
        #return template('tpl_picture_already_added', x = pic_id, api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url)
    else:    
        if media_found:
            #print("debug 1")
            #print (type(add_media))
            l_media_id = add_media.id
            l_username = add_media.user.username
            l_full_name = add_media.user.full_name
            l_userid = add_media.user.id
            l_thumbnail_url = add_media.get_thumbnail_url()
            l_low_resolution_url = add_media.get_low_resolution_url()
            l_standard_resolution_url = add_media.get_standard_resolution_url()
            l_room_number = 0
            l_exhibition_name = ""
            l_photo_categories = []
            l_request_sent = 0
            l_approved = 0
            l_caption = ""
            try:
                l_caption = add_media.caption.text
            except:
                pass
            l_link = add_media.link
            
            picked_pics[l_media_id] = [l_userid, l_username, l_full_name, l_caption, l_photo_categories, l_room_number, \
                                       l_exhibition_name, l_request_sent, l_approved, l_thumbnail_url, \
                                       l_low_resolution_url, l_standard_resolution_url, l_link ]
           
            
            l_photo_categories = request.forms.getlist('categories')
            l_exhibition_name_list = request.forms.getlist('exhibitions')
            for x in l_exhibition_name_list:
                l_exhibition_name = x
                
               
            
            l_room_number_list = request.forms.getlist('rooms')
            for x in l_room_number_list:
                l_room_number = x
                
            l_request_sent_list = request.forms.getlist('req_sent')    
            
            l_request_sent = 0            
            for x in l_request_sent_list:
                l_request_sent = 1                 
                
            picked_pics[l_media_id][4] = l_photo_categories
            picked_pics[l_media_id][5] = l_room_number
            if debug_mode == 1:
                print(l_room_number)
            picked_pics[l_media_id][6] = l_exhibition_name
            if debug_mode == 1:
                print(l_exhibition_name)    

            picked_pics[l_media_id][7] = l_request_sent
            if debug_mode == 1:
                print(l_request_sent) 
                
            return template('tpl_picked_picture_added', media_id = l_media_id, username = l_username, media_url = l_low_resolution_url, api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url)
        else:
            print("    * media search for ID = %s failed." % (picture_id))
            return template('tpl_error_report', api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url)    
    
@post('/submit_good_user')
def submit_good_user():
    new_username = request.forms.get('usernamex')      
    new_username = new_username.strip()
    photographer_id = -1
    
    
    new_user_search = api.user_search(q=new_username, count=1)
    if new_username == new_user_search[0].username:
        print ('Username to ID success for %s' % new_username)
        photographer_id = new_user_search[0].id
    else:
        print ('Username to ID failed for %s' % new_username)
        #print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
        return template('tpl_error_report',api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url)
        
    if photographer_id in good_users.keys():
        print("    * photographer %s already in the database! Skipping." % (photographer_id))
        return template('user_already_added', x = new_username, api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url)
            
    #print('')
    #print('Adding %s' % (new_user_search[0].username))    
    
    pom_user = api.user(photographer_id) 
    pom_user_follows = pom_user.counts[u'follows']
    pom_user_followed_by = pom_user.counts[u'followed_by']
    pom_user_media = pom_user.counts[u'media']
    pom_user_full_name = pom_user.full_name
    analyzed_for_network = 0
    analyzed_for_folowers = 0
    user_rank = 0
    user_categories = []

    
    good_users[photographer_id] = [new_user_search[0].username, pom_user_full_name, pom_user_media, pom_user_follows, \
                                   pom_user_followed_by, analyzed_for_network, analyzed_for_folowers, user_rank, user_categories]   
    
    l_photo_categories = request.forms.getlist('categories')
    good_users[photographer_id][8] = l_photo_categories
    
    return template('user_added', x = new_username, y = pom_user_follows, z = pom_user_followed_by, api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url)
    
    
@route('/find_talent')
def find_talent():    
    return template('tpl_find_talent', good_users=good_users, menu=menu, get_url=url, categories=categories) 
    
@route('/find_talent/<cat>')
def find_talent_cat(cat):
    user_candidates = {}
    out_good_users = good_users
    analyzed_good_users = 0
    skipped_good_users = 0
    #for good_user in good_users:
    
    #pick a category:
    picked_cat = cat

    for key, value in good_users.iteritems():
        if picked_cat in value[8]:
            good_username = value[0]
            try:
                user_search = api.user_search(q=good_username, count=1)
            except:
                print ('Username search failed for %s' % good_username) 
                continue          
                
                
            if good_username == user_search[0].username:
                print ('Username to ID success for %s' % good_username)
                user_id = user_search[0].id
            else:
                print ('Username to ID failed for %s' % good_username) 
                continue        
            
            print('')    
            print('Analyzing %s' % (user_search[0].username))
            try:
                pom_user = api.user(user_id) 
                pom_user_follows = pom_user.counts[u'follows']
                pom_user_followed_by = pom_user.counts[u'followed_by']
                pom_user_media = pom_user.counts[u'media']
                pom_user_full_name = pom_user.full_name
            except:
                print ('Username data not accessible for %s' % good_username) 
                pom_user_follows = 0
                pom_user_followed_by = 0
                pom_user_media = 0
                pom_user_full_name = ''
                continue  
                
            analyzed_for_network = 0
            analyzed_for_folowers = 0
            user_rank = 0
            # ===============================================================================================================================
            if user_id not in out_good_users.keys():
                out_good_users[user_id] = [user_search[0].username, pom_user_full_name, pom_user_media, pom_user_follows, \
                                           pom_user_followed_by, analyzed_for_network, analyzed_for_folowers, user_rank]   
            else:
                out_good_users[user_id][2] = pom_user_media
                out_good_users[user_id][3] = pom_user_follows
                out_good_users[user_id][4] = pom_user_followed_by
                
            print('User %s follows %s users and followed by %s users.' % (user_search[0].username, pom_user_follows, pom_user_followed_by))
            
            stops = 0
            discard = 0
            
            try:
                if ((essential_mode == True) and (pom_user_follows <= essential_treshold)) or (essential_mode == False):
                    user_follows_x, next = api.user_follows(user_id)
                    amt = len(user_follows_x)
                    print ("Found followings %s  " % amt)
                    analyzed_good_users += 1
                    while next and (stops==0):
                        more_users, next = api.user_followed_by(with_next_url=next)
                        user_follows_x.extend(more_users)
                        amt = len(user_follows_x)
                        print ("Found followings %s  " % amt)
                        if essential_mode == True:
                            if amt >= essential_treshold + 100:
                                stops = 1
                        else:
                            if amt >= get_max_followings:
                                stops = 1
                    
                    for uf in user_follows_x:
                        userid = uf.id.encode(sys.stdout.encoding, errors='replace')
                        username = uf.username.encode(sys.stdout.encoding, errors='replace')
                        
                        skip_user = False
                        if (filter_good_users == True) and (username in good_users):
                            skip_user = True
                            
                        if (filter_skip_users == True) and (username in skip_users):
                            skip_user = True
                            
                        if (essential_mode == True) and (amt > essential_treshold):
                            skip_user = True
                            #print("User skipped amt = %s\n" % (amt))
                            
                        
                        if not skip_user:
                            if (userid not in out_good_users.keys()):        
                                if (userid not in user_candidates.keys()):
                                    user_candidates[userid] = [username, 1]
                                else:
                                    user_candidates[userid][1] += 1
                else:
                    skipped_good_users += 1
                    print("Skipping user / Essential mode on")    
            
            except:
                print ('User analysis failed for %s' % good_username) 
                continue 
                
    users_list = {}

    for key, value in user_candidates.iteritems():
        users_list[value[0]] = value[1]
     
    sorted_user_candidates = sorted(users_list.items(), key=operator.itemgetter(1), reverse=True) 

    return template('tpl_find_talent_cat', cat=cat, good_users=good_users, menu=menu, get_url=url, categories=categories, \
                    analyzed_good_users=analyzed_good_users, skipped_good_users=skipped_good_users, essential_mode=essential_mode, \
                    sorted_user_candidates=sorted_user_candidates, show_talents_max=show_talents_max, api=api)     

                    
@route('/best-media/<username>')
def bestmedia(username):
    number_of_suggestions = 20
    new_username = username
    best_media = {}
    #normalize number of followers            
    max_followers = -1 
    min_followers = 99999999
    for key, value in good_users.iteritems():
        f = value[4]
        if f > max_followers:
            max_followers = f
        if f < min_followers:
            min_followers = f
    max_min_diff = max_followers - min_followers  

    if debug_mode == 0:
        tr_max_media = tr_max_media_individual    
    else:
        tr_max_media = 30 
    '''
    if new_username != '':
        tr_max_media = tr_max_media_individual # analyze last X pics
        for key, value in good_users.iteritems():
            if value[0] == new_username:
                good_users = {}
                good_users[key] = value
    '''    
    for key, value in good_users.iteritems():
        if ((value[0] not in skip_user) and (value[0] == username)):
            
            print ("Processing user %s %s" % (key, value[0]))
            gu_followers = value[4]
            gu_followers_norm = (gu_followers - min_followers) / max_min_diff
             
            # media_list = {}
            recent_media, x_next = api.user_recent_media(user_id=key)
            buf = "Reading %s pics..." % (len (recent_media))
            while x_next:
                buf = "Reading %s pics..." % (len (recent_media))
                print (buf)            
                media_feed, x_next = api.user_recent_media(with_next_url = x_next)
                recent_media.extend(media_feed)
                if len (recent_media) >= tr_max_media:
                    break
                
            best_media_ids = max_distance(recent_media, number_of_suggestions)
            
            for i in range(0, len(best_media_ids)):
                if (best_media_ids[i][0] not in best_media.keys()):
                    #x_media = []
                    for x in recent_media:
                        #print (x.id)
                        #print(best_media_ids)
                        if x.id == best_media_ids[i][0]:
                            x_media = x
                    #x_media = recent_media[best_media_ids[i]]
                    max_ratio_media_id = x_media.id
                    max_ratio_likes = x_media.like_count
                    max_ratio_mediaurl = x_media.get_thumbnail_url()      
                    ig_mediaurl = x_media.link                     
                    best_media[x_media.id] = [value[0], best_media_ids[i][1], max_ratio_likes, gu_followers, max_ratio_mediaurl, gu_followers_norm, ig_mediaurl] 
                    #best_media[x_media.id] = [value[0], best_media_ids[i][1], max_ratio_likes, gu_followers, max_ratio_mediaurl, gu_followers_norm] 
                    
    best_media_by_user = {}
    best_media_sorted = best_media
    for key, value in best_media_sorted.iteritems():
        if (new_username == "") or ((new_username != "") and (value[0] == new_username)):
            if value[0] not in best_media_by_user.keys():
                #add new user
                best_media_by_user[value[0]] = [[key, value[1], value[2], value[3], value[4], value[5], value[6]]]
                #best_media_by_user[value[0]] = [[key, value[1], value[2], value[3], value[4], value[5]]]
            else:
                best_media_by_user[value[0]].append([key, value[1], value[2], value[3], value[4], value[5], value[6]])
                #best_media_by_user[value[0]].append([key, value[1], value[2], value[3], value[4], value[5]])
            
                            
    return template('tpl_best_media', username = new_username, best_media=best_media, good_users=good_users, menu=menu, get_url=url, categories=categories, \
                    api =api, best_media_by_user=best_media_by_user)

@route('/add-picture/<pic_id>')
def add_picked_picture(pic_id):
    picture_id = pic_id        
    picture_id = picture_id.strip()
    
    try:
        add_media = api.media(media_id = picture_id)
        media_found = True
    except:
        print("    * media search for ID = %s failed." % (picture_id))
        media_found = False
        
        
    if media_found:
        l_media_id = add_media.id
        l_username = add_media.user.username
        l_full_name = add_media.user.full_name
        l_userid = add_media.user.id
        l_thumbnail_url = add_media.get_thumbnail_url()
        l_low_resolution_url = add_media.get_low_resolution_url()
        l_standard_resolution_url = add_media.get_standard_resolution_url()
        l_room_number = 0
        l_exhibition_name = ""
        l_photo_categories = []
        l_request_sent = 0
        l_approved = 0
        l_caption = ""
        try:
            l_caption = add_media.caption.text
        except:
            pass
        l_link = add_media.link

        #print (add_media.get_standard_resolution_url())
        if l_media_id in picked_pics.keys():
            print("    * media with ID = %s already in the database! Skipping." % (picture_id))
   
    return template('tpl_add_picked_pic', pic_id = pic_id, menu=menu, api=api, categories=categories, exhibitions=exhibitions, rooms=rooms, \
                    l_userid=l_userid, l_username=l_username, l_full_name=l_full_name, l_caption=l_caption, l_photo_categories=l_photo_categories\
                    , l_room_number=l_room_number, \
                    l_exhibition_name=l_exhibition_name, l_request_sent=l_request_sent, l_approved=l_approved, l_thumbnail_url=l_thumbnail_url, \
                    l_low_resolution_url=l_low_resolution_url, l_standard_resolution_url=l_standard_resolution_url, l_link=l_link, get_url=url)

@get('/network')
@get('/network/')
def network_main_page():
    return template('tpl_network_main', menu=menu)
    
@route('/network/addbyid/<userid>')
def add_node_by_id(userid):
    pom_user = api.user(userid) 
    username = pom_user.username
    pom_user_follows = pom_user.counts[u'follows']
    pom_user_followed_by = pom_user.counts[u'followed_by']
    pom_user_media = pom_user.counts[u'media']
    pom_user_full_name = pom_user.full_name    
    add_node_to_network(username)   
    return("Done. User %s (%s) added. user follows {{%s}} users and is followed by {{%s}} users." % (username, pom_user_full_name, pom_user_follows, pom_user_followed_by ))

@route('/network/add/<name>')    
@post('/network/add/<name>')
def add_node_to_network(name):
    if name == 'nntools_form':
        new_username = request.forms.get('usernamex')      
        new_username = new_username.strip()
    else:
        new_username = name

    photographer_id = -1

    new_user_search = api.user_search(q=new_username, count=1)
    if new_username == new_user_search[0].username:
        print ('Username to ID success for %s' % new_username)
        photographer_id = new_user_search[0].id
    else:
        print ('Username to ID failed for %s' % new_username)
        #print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
        return template('tpl_error_report',api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url)
        
    if photographer_id in user_network.keys():
        print("    * photographer %s already in the network database! Skipping." % (photographer_id))
        #return template('tpl_user_already_added_to_network', x = new_username, api1 = api.x_ratelimit_remaining, api2 = api.x_ratelimit, menu=menu, get_url=url)
        followings_list = user_network[photographer_id][1]
    else:
        followings_list = []
            
    #print('')
    #print('Adding %s' % (new_user_search[0].username))    
    api_limit_start = api.x_ratelimit_remaining
    
    pom_user = api.user(photographer_id) 
    pom_user_follows = pom_user.counts[u'follows']
    pom_user_followed_by = pom_user.counts[u'followed_by']
    pom_user_media = pom_user.counts[u'media']
    pom_user_full_name = pom_user.full_name
    analyzed_for_network = 1
    analyzed_for_folowers = 0
    user_rank = 0
    follows_in_network = 0 # counter how many users user follows that are already in our network
    network_size = len(user_network)
    user_categories = []
    in_good_users = False
    if photographer_id in good_users.keys():
        in_good_users = True
            
    user_network[photographer_id] = [[new_user_search[0].username, pom_user_follows, pom_user_followed_by, analyzed_for_network, user_rank, in_good_users], followings_list]
    
#
    stops = False 
    
    user_follows_x, next = api.user_follows(photographer_id)
    amt = len(user_follows_x)
    print ("Found followings %s  " % amt)
    while next and (stops==False) and (amt < tr_network_followings):
        more_users, next = api.user_followed_by(with_next_url=next)
        user_follows_x.extend(more_users)
        amt = len(user_follows_x)
        print ("Found followings %s  " % amt)
        if amt >= tr_network_followings:
            stops = True
    
    followings_id_list = []
    for uf in user_follows_x:
        userid = uf.id.encode(sys.stdout.encoding, errors='replace')
        if userid in user_network.keys():
            follows_in_network += 1      
            
        skip_user = False
        
        if not skip_user:       
            if (userid not in followings_id_list):
                followings_id_list.extend([userid])
    
    user_network[photographer_id][1] = followings_id_list
    
    api_limit_end = api.x_ratelimit_remaining
    api_cost = int(api_limit_end) - int(api_limit_start)
    api_rate = 0
    if pom_user_follows != 0:
        api_rate = int(api_cost) / int(pom_user_follows) 
    
    return template('tpl_user_added_to_network', x = new_username, y=pom_user_follows, z=pom_user_followed_by, menu=menu, api=api, get_url=url, \
        api_limit_end=api_limit_end, api_limit_start=api_limit_start, api_cost=api_cost, api_rate=api_rate, \
        follows_in_network=follows_in_network, network_size=network_size)
    
@route('/network/list') 
@route('/network/list/')   
def network_list():
    print("Debug1")
    return template('tpl_network_list', menu=menu, user_network=user_network)

@route('/network/discover')
def network_discover():
    user_candidates = {}
    for key, value in user_network.iteritems():
        followings = value[1]
        for x in followings:
            if x in user_candidates.keys():
                user_candidates[x][1] += 1
            else:
                user_candidates[x] = [x ,1]
    user_candidates = sorted(user_candidates.iteritems(), reverse=True, key=lambda i: i[1][1])

    return template('tpl_discover_network' , user_candidates=user_candidates, menu=menu, good_users=good_users, user_network=user_network)
    
    
@route('/network/pr')
def calc_page_rank():
    gr = nx.DiGraph(followings=0)
    for key, value in user_network.iteritems():
        username = key
        if key in good_users.keys():
            username = good_users[key][0]
        
        gr.add_node(username, followings=value[0][1]) 

        vertices = value[1]
        #print (vertices)
        for x in vertices:
            if x in user_network.keys():
                username_to = x
                if x in good_users.keys():
                    username_to = good_users[x][0]            
                # user in network, add vertice
                #if value[0][1] == 0:
                #    pom_weight = 0
                #else:
                #    pom_weight = 1/value[0][1]
                gr.add_edge(username, username_to)
                #print ("Edge added %s  to  %s" % (username, username_to))
                
    
    #pr = pagerank(gr, damping_factor=0.85, max_iterations=50, min_delta=1e-05)
    pr = nx.pagerank(gr, alpha=0.85, personalization=None, max_iter=50, tol=1e-08)
    prl = sorted(pr.iteritems(), reverse=True, key=lambda i: i[1])
    
    #print (pr)
    #nx.draw_networkx(gr)
    #plt.show()
    #print("Draw complete")
    print(sorted(nx.degree(gr).values()))
    return template("tpl_network_pagerank", menu=menu, gr=prl, good_users=good_users, user_network=user_network)

run(host=HOST, port=8080, debug = True,reloader=True)