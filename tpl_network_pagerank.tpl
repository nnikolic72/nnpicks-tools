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
        
<p>User pagerank</p>

<table class='gridtable'>
%for value in gr:  
  <tr>
    <td>{{value[0]}}</td>
    <td>{{value[1]}}</td>   
  </tr>
%end   

</table>
</body>
</html>