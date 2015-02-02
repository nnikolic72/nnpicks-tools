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
        
<p>User network important nodes</p>

<table class='gridtable'>
<tr>
    <th>User ID
    </th>
    
    <th>Links toward
    </th>  
    
    <th>Good user
    </th>    
    
    <th>Add
    </th>    
</tr>
<tr>
%network_length = len(user_network)
%for value in user_candidates:

        
        <td>
        User: <a href='http://iconosquare.com/viewer.php#/user/{{value[0]}}/'>{{value[0]}}</a>
        </td>

        <td>
        {{value[1][1]}} of {{network_length}}
        </td>
        
        <td>
%if value[0] in good_users.keys():
% m = good_users[value[0]][0]
{{m}}
%else:
Not good user
%end
        </td> 
        

        <td>
%if value[0] not in user_network.keys():        
        <a href='/network/addbyid/{{value[0]}}' target='_blank'>add to network</a>
%end
        </td>
    </tr>
%end
</table>

</body>
</html>