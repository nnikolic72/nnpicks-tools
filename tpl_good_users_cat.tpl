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
        
<p>Good users list {{category_name}}</p>

<br>
<div>
% for cat in categories:
<a href="/good-users/{{cat}}">{{cat}}</a>&nbsp
%end 
</div>
<br>
<table class='gridtable'>
%cnt = 0
%for key, value in good_users.iteritems():
%if category_name in value[8]:
%cnt += 1
  <tr>
    <td>{{cnt}}. <a href='http://iconosquare.com/viewer.php#/user/{{key}}/' target="_blank">{{value[0]}}</a></td>
    <td><a href='/user-profile/{{value[0]}}'>profile</a></td>
    <td><a href='/best-media/{{value[0]}}'>find best media</a></td>
    <td>Followers: {{value[4]}}</td>
    <td>
%if key not in user_network.keys():
    <a href='/network/add/{{value[0]}}' target="_blank">add to network</a>
%end
    </td>
   <td>
%already_invited=False
%for k, v in picked_pics.iteritems():
%    if v[0] == key:
%        already_invited = True
%        break
%end
%end
%if already_invited==False:
User not invited to NN Picks
%    if value[4] <= 40000:
*
%    end
%end
   </td>   
  </tr>
%end
%end   

</table>
</body>
</html>