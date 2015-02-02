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
        
<p>Best media for user "{{username}}"</p>
<br><img src='{{ get_url('static', filename='best_pics.png') }}'><img><br>
%for key, value in best_media_by_user.iteritems():
%    for x in value:
        User: {{key}}, Followers: {{x[3]}}, Media likes: {{x[2]}}, Top-n: {{x[1]}}<br>
        Instagram URL: <a href='{{x[6]}}'>{{x[6]}}</a>    {{x[6]}}<br>
        <a href='http://iconosquare.com/viewer.php#/detail/{{x[0]}}'><img src='{{x[4]}}'/></a><br>
        <a href='/add-picture/{{x[0]}}' target='_blank'>add picked picture</a><br><hr>
%   end       
    <hr> 
%end
<hr>
<br>
*** Remaining API Calls = {{api.x_ratelimit_remaining}}/{{api.x_ratelimit}}
</body>
</html>