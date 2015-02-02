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

    <a href="/">home</a> | 


<br> <br>           
Save report:
%if debug_mode == True:
<p><b>DEBUG MODE ON</b></p>
%end 
%if picked_pics_db_saved == True:
<p><b>NN PICKS Picked Pictures database saved!</b></p>
%end 
%if good_users_db_saved == True:
<p><b>Good Users database saved!</b></p>
%end 
%if great_pics_db_saved == True:
<p><b>Great Pics from good users database saved!</b></p>
%end 
%if network_db_saved == True:
<p><b>User network database saved!</b></p>
%end 
<hr>
