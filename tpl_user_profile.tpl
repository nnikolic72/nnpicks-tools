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
        
<p>Photographer {{user_x[0]}} profile</p>
%pom_user = user_x[0]

<table class='gridtable'>

  <tr>
    <td>Username</td><td>{{pom_user}}</td>
  </tr>
  <tr>
    <td>User follows</td><td>{{pom_user_follows}}</td>
  </tr>    
  <tr>    
    <td>User followed by</td><td>{{pom_user_followed_by}}</td>
  </tr>    
  <tr>    
    <td>User media count</td><td>{{pom_user_media}}</td>
  </tr>    
  <tr>
    <td>User full name</td><td>{{pom_user_full_name}}</td>
  </tr>    

</table>
</body>
</html>