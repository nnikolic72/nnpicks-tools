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
import math

access_token='1529897738.2d6fe64.87556684de0d4ce1aa6afbf423a8cada'
api = InstagramAPI(access_token=access_token)

debug_mode = 0
first_run = False
picked_pic_db = 'db_nnpicks.txt'
picked_pic_db_backup = 'db_nnpicks.txt.backup'
picked_pic_db_debug = 'db_nnpicks_debug.txt'
good_users_db = 'good_users.txt'
good_users_db_debug = 'good_users_debug.txt'
report_file = "nnreport.html"

try:
    shutil.copyfile(picked_pic_db, picked_pic_db_backup)
except:
    print("Error during backup. Exiting.")
    print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
    sys.exit(0) 
    

categories = ["abstract", "animals", "black and white", "architecture", "concert", "family", "fashion", \
              "fine art", "photojournalism", "landscape", "macro", "nature", "people", "sport", "still life", "portrait", \
              "street", "transportation", "travel", "underwater", "urbex", "misc", "reflection", "cityscape"]

              
exhibitions = ["Street Clicks", "Landscape", "People", "Black and White", "Portrait"]
rooms = ["One", "Two", "Three", "Four", "Five"]

picked_pics = {}
try:
    if not first_run:
        f_results = open(picked_pic_db, "r")
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
        f_results = open(good_users_db, "r")
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
        
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def pick_categories():
    l_photo_categories = []
    cat_list = "Categories: "
    for x in categories:
        buf = "[%s] %s  | " % (categories.index(x), x) 
        cat_list +=  buf
    print (cat_list)
    chosen_cats = raw_input("        * Insert comma separated list of categories: ")
    chosen_cats = chosen_cats.strip()  
    chosen_cats_idx = chosen_cats.split(",")
    #print (chosen_cats_idx)
    cats_string = ""
    for x in chosen_cats_idx:
        #print (x)
        #print (categories[x])
        l_photo_categories.extend([categories[int(x)]])
    return (l_photo_categories)
    
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

    

def get_room():
    rooms_list = "Rooms: "
    for x in rooms:
        buf = "[%s] %s  | " % (rooms.index(x), x) 
        rooms_list +=  buf
    print (rooms_list)
    chosen_room = raw_input("        * Pick Virtual Theme Room: ")
    chosen_room = chosen_room.strip()  
    return rooms[int(chosen_room)]  
    
def get_exhibition():
    exhibition_list = "Exhibitions: "
    for x in exhibitions:
        buf = "[%s] %s  | " % (exhibitions.index(x), x) 
        exhibition_list +=  buf
    print (exhibition_list)
    chosen_exhibition = raw_input("        * Pick Exhibition: ")
    chosen_exhibition = chosen_exhibition.strip()  
    return exhibitions[int(chosen_exhibition)]      
                    
exit_flag = False
while not exit_flag:
    print('')
    print('Menu:')
    print('=====')
    print('')
    print('[1] Add new candidate picture')
    print('[2] Mark approved picture')
    print('[3] Mark unapproved picture')
    print('[4] Request for feature sent for picture')
    print('[5] Add categories to picture')
    print('[6] Assign picture to exhibition')
    print('----------------------------------------')    
    print('[R1] Report: Pictures in category')
    print('[R2] Report: Unassigned pictures in category')
    print('[R3] Report: Exibition report')    
    print('----------------------------------------') 
    print('[P1] Add new photographer')    
    print('----------------------------------------')     
    print('[9] Save')
    print('[0] Exit')

    user_choice = raw_input("Pick a menu item: ")
    user_choice = user_choice.strip()
    
    if user_choice == "0":
        exit_flag = True
        
    if user_choice == "1":
        # Add new candidate picture
        picture_id = raw_input("    * Enter the picture ID: ")        
        picture_id = picture_id.strip()

        try:
            add_media = api.media(media_id = picture_id)
            media_found = True
        except:
            print("    * media search for ID = %s failed." % (picture_id))
            continue
            media_found = False
            
            
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

            #print (add_media.get_standard_resolution_url())
            if l_media_id in picked_pics.keys():
                print("    * media with ID = %s already in the database! Skipping." % (picture_id))
                continue
            add_cats = ""
            add_cats = query_yes_no("    * Do you want to add categories?")

            
            picked_pics[l_media_id] = [l_userid, l_username, l_full_name, l_caption, l_photo_categories, l_room_number, \
                                       l_exhibition_name, l_request_sent, l_approved, l_thumbnail_url, \
                                       l_low_resolution_url, l_standard_resolution_url, l_link ]
    
            if (add_cats == True):
                #print("debug 2")
                l_photo_categories = pick_categories()
                    
                picked_pics[l_media_id][4] = l_photo_categories

    if user_choice == "2":    
        # Mark approved picture
        picture_id = raw_input("    * Enter the approved picture ID: ")        
        picture_id = picture_id.strip()        
 
        if picture_id in picked_pics.keys():
            picked_pics[picture_id][8] = 1
            print("    * OK!")
        else:
            print("    * media with ID = %s not found in the database! Add it first!" % (picture_id))
            continue            

    if user_choice == "3":    
        # Mark unapproved picture
        picture_id = raw_input("    * Enter the unapproved picture ID: ")        
        picture_id = picture_id.strip()        
 
        if picture_id in picked_pics.keys():
            picked_pics[picture_id][8] = -1
            print("    * OK!")
        else:
            print("    * media with ID = %s not found in the database! Add it first!" % (picture_id))
            continue             
            
    if user_choice == "4":    
        # Request for feature sent for picture
        picture_id = raw_input("    * Enter the requested for approval picture ID: ")        
        picture_id = picture_id.strip()        
 
        if picture_id in picked_pics.keys():
            picked_pics[picture_id][7] = 1
            print("    * OK!")
        else:
            print("    * media with ID = %s not found in the database! Add it first!" % (picture_id))
            continue   
     
     
    if user_choice == "5":     
        # Add categories to picture
        picture_id = raw_input("    * Enter the picture ID: ")        
        picture_id = picture_id.strip()

        if picture_id not in picked_pics.keys():
            print("    * media with ID = %s not in database! Skipping." % (picture_id))
            continue
        
        l_photo_categories = pick_categories()
        picked_pics[picture_id][4] = l_photo_categories
    
    
    if user_choice == "6":        
        #Assign picture to exhibition
        picture_id = raw_input("    * Enter the picture ID: ")        
        picture_id = picture_id.strip()

        if picture_id not in picked_pics.keys():
            print("    * media with ID = %s not in database! Skipping." % (picture_id))
            continue        
        
        l_room = get_room()
        picked_pics[picture_id][5] = l_room
        
        l_exhibition = get_exhibition()
        picked_pics[picture_id][6] = l_exhibition
    
    
    if user_choice == "P1":     
        # Add categories to picture
        new_username = raw_input("    * Enter the photographer username: ")        
        new_username = new_username.strip()
        
        new_user_search = api.user_search(q=new_username, count=1)
        if new_username == new_user_search[0].username:
            print ('Username to ID success for %s' % new_username)
            photographer_id = new_user_search[0].id
        else:
            print ('Username to ID failed for %s' % new_username)
            print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))
            continue
            
        if photographer_id in good_users.keys():
            print("    * photographer %s already in the database! Skipping." % (photographer_id))
            continue
                
        print('')
        print('Adding %s' % (new_user_search[0].username))    
        
        pom_user = api.user(photographer_id) 
        pom_user_follows = pom_user.counts[u'follows']
        pom_user_followed_by = pom_user.counts[u'followed_by']
        pom_user_media = pom_user.counts[u'media']
        pom_user_full_name = pom_user.full_name
        analyzed_for_network = 0
        analyzed_for_folowers = 0
        user_rank = 0
        user_categories = []
        # ===============================================================================================================================

        good_users[photographer_id] = [new_user_search[0].username, pom_user_full_name, pom_user_media, pom_user_follows, \
                                       pom_user_followed_by, analyzed_for_network, analyzed_for_folowers, user_rank, user_categories]   
    
        print('User %s follows %s users and followed by %s users.' % (new_user_search[0].username, pom_user_follows, pom_user_followed_by))
        
        print('')
        l_photo_categories = pick_categories()
        good_users[photographer_id][8] = l_photo_categories
        
    if user_choice == "9":
        save = True
        if save == True:
            if debug_mode == 0:
                f_results = open(picked_pic_db, "w")
                json.dump(picked_pics, f_results, sort_keys=True, indent=4, separators=(',', ': ')) 
            else:
                f_results = open(picked_pic_db_debug, "w")
                json.dump(picked_pics, f_results, sort_keys=True, indent=4, separators=(',', ': '))     
            print("DATABASE SAVED!")
        
        if save == True:
            if debug_mode == 0:
                f_results = open(good_users_db, "w")
                json.dump(good_users, f_results, sort_keys=True, indent=4, separators=(',', ': ')) 
            else:
                f_results = open(good_users_db_debug, "w")
                json.dump(good_users, f_results, sort_keys=True, indent=4, separators=(',', ': '))     
            print("USERS DATABASE SAVED!")        
        
    if user_choice == "R1":    
        # Report: Pictures in category
        cat = pick_one_category()
        
        f = open(report_file, "w")
        f.write("<html>\n")
        f.write("<style>\n")
        f.write("    * {\n")
        f.write("      font-family: sans-serif;\n")
        f.write("    }\n")
        f.write("</style>\n")
        f.write("<body>\n")
        buf = "<h2>Report: Pictures in category %s</h2>" % (cat)
        f.write(buf + "<br>\n")     
        for key, value in picked_pics.iteritems():
            if cat in value[4]:
                buf = "Author: <a href='http://iconosquare.com/viewer.php#/user/%s/'>%s</a>" % (value[0], value[1])
                f.write(buf + "<br>\n") 
                buf = "Author name: '%s'" % (value[2].encode('utf-8').strip())
                f.write(buf + "<br>\n") 
                buf = "Photo caption: '%s'" % (value[3].encode('utf-8').strip())
                f.write(buf + "<br>\n")
                buf = "Assigned room: '%s'" % (value[5])
                f.write(buf + "<br>\n")    
                buf = "Assigned exhibition: '%s'" % (value[6])
                f.write(buf + "<br>\n")  
                buf = "Request sent: '%s'" % (value[7])
                f.write(buf + "<br>\n")    
                buf = "Request approved: '%s'" % (value[8])
                f.write(buf + "<br>\n")                  
                buf = "<a href='http://iconosquare.com/viewer.php#/detail/%s'><img src='%s'/></a>\n" % (key, value[9])
                f.write(buf + "<br>\n") 
                f.write("<hr>\n") 

        f.write('</body>\n')
        f.write('</html>\n')         
        f.close()    
        print ("Report generated.")        
    
    if user_choice == "R2":    
        # Report: Pictures in category
        cat = pick_one_category()
        
        f = open(report_file, "w")
        f.write("<html>\n")
        f.write("<style>\n")
        f.write("    * {\n")
        f.write("      font-family: sans-serif;\n")
        f.write("    }\n")
        f.write("</style>\n")
        f.write("<body>\n")
        buf = "<h2>Report: Pictures in category %s</h2>" % (cat)
        f.write(buf + "<br>\n")     
        for key, value in picked_pics.iteritems():
            if (cat in value[4]) and (value[7] == 0):
                buf = "Author: <a href='http://iconosquare.com/viewer.php#/user/%s/'>%s</a>" % (value[0], value[1])
                f.write(buf + "<br>\n") 
                buf = "Author name: '%s'" % (value[2].encode('utf-8').strip())
                f.write(buf + "<br>\n") 
                buf = "Photo caption: '%s'" % (value[3].encode('utf-8').strip())
                f.write(buf + "<br>\n")
                buf = "Assigned room: '%s'" % (value[5])
                f.write(buf + "<br>\n")    
                buf = "Assigned exhibition: '%s'" % (value[6])
                f.write(buf + "<br>\n")  
                buf = "Request sent: '%s'" % (value[7])
                f.write(buf + "<br>\n")    
                buf = "Request approved: '%s'" % (value[8])
                f.write(buf + "<br>\n")                  
                buf = "<a href='http://iconosquare.com/viewer.php#/detail/%s'><img src='%s'/></a>\n" % (key, value[9])
                f.write(buf + "<br>\n") 
                f.write("<hr>\n") 

        f.write('</body>\n')
        f.write('</html>\n')         
        f.close() 
        print ("Report generated.")        
     
    if user_choice == "R3":   
        # Report: Exibition report
        exib = get_exhibition()
        f = open(report_file, "w")
        f.write("<html>\n")
        f.write("<style>\n")
        f.write("    * {\n")
        f.write("      font-family: sans-serif;\n")
        f.write("    }\n")
        f.write("</style>\n")
        f.write("<body>\n")
        buf = "<h2>Report: Pictures in exibition %s</h2>" % (exib)
        f.write(buf + "<br>\n")     
        for key, value in picked_pics.iteritems():
            if (exib == value[6]):
                buf = "Author: <a href='http://iconosquare.com/viewer.php#/user/%s/'>%s</a>" % (value[0], value[1])
                f.write(buf + "<br>\n") 
                buf = "Author name: '%s'" % (value[2].encode('utf-8').strip())
                f.write(buf + "<br>\n") 
                buf = "Photo caption: '%s'" % (value[3].encode('utf-8').strip())
                f.write(buf + "<br>\n")
                buf = "Assigned room: '%s'" % (value[5])
                f.write(buf + "<br>\n")    
                buf = "Assigned exhibition: '%s'" % (value[6])
                f.write(buf + "<br>\n")  
                buf = "Request sent: '%s'" % (value[7])
                f.write(buf + "<br>\n")   
                fontcol = "black"
                if (value[8] == 0):
                    fontcol = "red"
                if (value[8] == 1):
                    fontcol = "green"                    
                buf = "<font color='%s'>Request approved: '%s' </font>" % (fontcol, value[8])
                f.write(buf + "<br>\n")                  
                buf = "<a href='http://iconosquare.com/viewer.php#/detail/%s'><img src='%s'/></a>\n" % (key, value[9])
                f.write(buf + "<br>\n") 
                f.write("<hr>\n") 

        f.write('</body>\n')
        f.write('</html>\n')         
        f.close() 
        print ("Report generated.")        
        
    
    #print (picked_pics)
save = query_yes_no("DO YOU WANT TO SAVE?")    
if save == True:
    if debug_mode == 0:
        f_results = open(picked_pic_db, "w")
        json.dump(picked_pics, f_results, sort_keys=True, indent=4, separators=(',', ': ')) 
    else:
        f_results = open(picked_pic_db_debug, "w")
        json.dump(picked_pics, f_results, sort_keys=True, indent=4, separators=(',', ': '))     
    print("DATABASE SAVED!")
    
#fix for good users categories
#for key, value in good_users.iteritems():
#    if len(value) == 8:
#        good_users[key].append(categories[16])
    
if save == True:
    if debug_mode == 0:
        f_results = open(good_users_db, "w")
        json.dump(good_users, f_results, sort_keys=True, indent=4, separators=(',', ': ')) 
    else:
        f_results = open(good_users_db_debug, "w")
        json.dump(good_users, f_results, sort_keys=True, indent=4, separators=(',', ': '))     
    print("USERS DATABASE SAVED!")

    
f_results.close() 
print ("*** Remaining API Calls = %s/%s" % (api.x_ratelimit_remaining,api.x_ratelimit))