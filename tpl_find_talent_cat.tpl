%#template to generate a HTML profile
<html>
<style>
    * {
      font-family: sans-serif;
    }
</style>
<style type="text/css">
table.gridtable {
	font-family: verdana,arial,sans-serif;
	font-size:12px;
	color:#333333;
	border-width: 1px;
	border-color: #666666;
	border-collapse: collapse;
}
table.gridtable th {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #dedede;
}
table.gridtable td {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #ffffff;
}
</style>
<body>

%for key, value in menu.iteritems():
    <a href="{{value}}">{{key}}</a> | 
%end
        
<p>Find talent in category "{{cat}}"</p>
<p>Categories</p>
%for x in categories:
<a href='/find_talent/{{x}}'>{{x}}</a><br>
%end

%if essential_mode == True:
    <p>Essential mode ON.</p><br><br>
%end
Total {{len(good_users)}} good users.<br>
Analyzed {{analyzed_good_users}} good users.<br>
Skipped {{skipped_good_users}} good users.<br>

%i = 0
%for tag_i, value in sorted_user_candidates:
    {{tag_i}} : {{value}}<br> 
%    i += 1
%    if i == show_talents_max:
%        break
%    end
%end
<hr>
<br>
*** Remaining API Calls = {{api.x_ratelimit_remaining}}/{{api.x_ratelimit}}
</body>
</html>