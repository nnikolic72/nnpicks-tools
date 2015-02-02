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
        
<p>Good users list</p>

<img id="top" src="{{ get_url('static', filename='top.png') }}" alt="">
		<h3><a>Add New User</a></h3>
		<form method="post" action="/submit_good_user">					
			<ul >
					<li id="li_1" >
		<label  for="element_1">New Good user </label>
		<div>
			<input name="usernamex" type="text" maxlength="255" value=""/> 
		</div> 
		</li>
		<br>
        User categories: <br> 
% for cat in categories:        
        <input type="checkbox" name="categories" value="{{cat}}">{{cat}}<br>
%end        
		<li class="buttons">
			    <input type="hidden" name="form_id" value="946904" />
				<input id="saveForm"  type="submit" name="submit" value="Add" />
		</li>
			</ul>
		</form>	
<img id="bottom" src="{{ get_url('static', filename='bottom.png') }}" alt="">

<br>
<div>
% for cat in categories:
<a href="/good-users/{{cat}}">{{cat}}</a>&nbsp
%end 
</div>
<br>
<table class='gridtable'>
%for key, value in good_users.iteritems():
  <tr>
    <td><a href='http://iconosquare.com/viewer.php#/user/{{key}}/' target="_blank">{{value[0]}}</a></td>
    <td><a href='/user-profile/{{value[0]}}'>profile</a></td>
    <td><a href='/best-media/{{value[0]}}'>find best media</a></td>
    <td>Followers: {{value[4]}}</td>
    <td>
%if key not in user_network.keys():
    <a href='/network/add/{{value[0]}}' target="_blank">add to network</a>
%end
    </td>
    <td>Categories: 
%    for x in value[8]:
     {{x}},  
%    end
    </td>
   <td>
   ID: {{key}}
   </td>
  </tr>
%end   

</table>
</body>
</html>