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
        
<p>User network list</p>

%for key, value in user_network.iteritems():
    User: {{value[0][0]}} (id {{key}}), Followers: {{value[0][2]}}, Followings: {{value[0][1]}}, Rank: {{value[0][4]}}<br>

%end

</body>
</html>