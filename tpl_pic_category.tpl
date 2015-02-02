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
        
<p>Pictures in category {{cat}}</p>
<p>Categories</p>
%for x in categories:
<a href='/pictures/{{x}}'>{{x}}</a><br>
%end


<table class='gridtable'>
%for key, value in picked_pics.iteritems():
%    if cat in value[4]:
    %imgstyle = "border:10px solid grey;"
    %if (value[7] == 1) and (value[8]==0):
    %    imgstyle = "border:10px solid red;"
    %end
    %if (value[7] == 1) and (value[8]==1):
    %    imgstyle = "border:10px solid green;"        
    %end

  <tr>
    <td>
    <a href='http://iconosquare.com/viewer.php#/detail/{{key}}'><img src='{{value[9]}}' style="{{imgstyle}}"/></a>
    </td>
    <td>
    <a href='http://iconosquare.com/viewer.php#/user/{{value[0]}}/'>{{value[1]}}</a>
    <br>
    Author name: '{{value[2].encode('utf-8').strip()}}'
    <br>
    Photo caption: '{{value[3].encode('utf-8').strip()}}'
    <br>
    Assigned room: '{{value[5]}}'
    <br>
    Assigned Exhibition: '{{value[6]}}'
    <br>    
    Request sent: '{{value[7]}}'
    <br>
    Request approved: '{{value[8]}}'

    </td>
  </tr>

%end
%end   
%end
</table>


</body>
</html>