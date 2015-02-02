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
        
<p>Pictures</p>
<p>Categories</p>
%for x in categories:
<a href='/pictures/{{x}}'>{{x}}</a><br>
%end

<table class='gridtable'>
%for key, value in picked_pics.iteritems():
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
    
    <form method="post" action="/submit_picked_pic/{{value[0]}}">	
    <table class='gridtable'>
        <tr>
            <td>User profile page:</td><td><a href='http://iconosquare.com/viewer.php#/user/{{value[0]}}/'>{{value[1]}}</a></td>
        </tr>

        <tr>       
            <td>Author name:</td>       
            <td>'{{value[2].encode('utf-8').strip()}}'</td> 
        </tr>
        <tr>
            <td>Photo caption: </td> 
            <td>'{{value[3].encode('utf-8').strip()}}'</td> 
        </tr>        
        <tr>
            <td>Assigned room:</td>  
            <td>'{{value[5]}}'</td> 
        </tr>   
        <tr>
            <td>Assigned Exhibition:</td>  
            <td>'{{value[6]}}'</td> 
        </tr>         
        <tr>

     
            <td>Request sent:</td>  
            <td>
            {{value[7]}}
            <select name="request_sent">
%if value[7] == 1:
            <option value="0">Not Sent</option>
            <option selected value="1" >Sent</option>
%end  
%if value[7] == 0:
            <option selected value="0" >Not Sent</option>
            <option value="1">Sent</option>
%end  
            </select>
            </td> 
        </tr>        
        <tr>
            <td>Request approved:</td>  
            <td>'{{value[8]}}'</td> 
        </tr> 
        <tr>
        <td>
        <input id="saveForm"  type="submit" name="submit" value="Add/Update" />
        </td>
        </tr>        
    </table>
    </form>
    </td>
  </tr>


%end   
%end
</table>
</body>
</html>