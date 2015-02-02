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
        
<p>Ghost following panel</p>



<table class='gridtable'>
%for key, value in disp_media.iteritems():
  <tr>
      <td>
      <a href='http://iconosquare.com/viewer.php#/user/{{key}}/'>{{value[0]}} - {{value[1]}}</a>
%images_cnt = (len(value) - 9)/2
      
      Images count {{images_cnt}}
      </td>
      <td>
      
      </td>  
  </tr>
  <tr>
      <td>
%for i in range(0,images_cnt-1): 
%image_id = value[9+(i*2)]
%image_data = value[10+(i*2)]
      <a href='http://iconosquare.com/viewer.php#/detail/{{image_id}}'><img src='{{image_data[1]}}' style="border:10px solid grey;"/></a>&nbsp;
%end
      </td>
      <td>
      
      </td>
  </tr>
%end
%end
%end   
%end
</table>


</body>
</html>