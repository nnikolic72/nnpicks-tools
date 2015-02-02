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
        
<p>Best media</p>

%for key, value in best_media.iteritems():

    User: {{value[0]}}, Top-n: {{value[1]}}, Followers: {{value[3]}}, Followings: {{value[2]}}, ratio: {{value[5]}}<br>
    <a href='http://iconosquare.com/viewer.php#/detail/{{key}}'><img src='{{value[4]}}'/></a><br>
      
    <hr> 
%end
<hr>
<br>

</body>
</html>