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
        
<p>Network main page</p>


<table class='gridtable'>

  <tr>
    <td><a href='/network/display'>Display network</a></td>
  </tr>
  <tr>    
    <td><a href='/network/list'>List network nodes</a></td>
  </tr>  
  <tr>
    <td><a href='/network/pr'>Calculate Page Rank of users</a></td>
  </tr>    
  <tr>    
    <td>Add user to network<br>
    <form method="post" action="/network/add/nntools_form">
        <input name="usernamex" type="text" maxlength="255" value=""/>
        <input id="saveForm"  type="submit" name="submit" value="Add" />
    </form>
    </td>
  </tr>    
  <tr>    
    <td><a href='/network/discover'>Discover important nodes</a></td>
  </tr>    
  <tr>
    <td>Remove user from network
    <br>
    <form method="post" action="/network/remove">
        <input name="usernamex" type="text" maxlength="255" value=""/>
        <input id="saveForm"  type="submit" name="submit" value="Add" />
    </form>    
    </td>
  </tr>    

</table>
</body>
</html>