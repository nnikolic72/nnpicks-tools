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
        
<p>Add picture "{{pic_id}}"</p>
<img id="top" src="{{ get_url('static', filename='top.png') }}" alt="">
		<h3><a>Add New Picked Picture</a></h3>
		<form method="post" action="/submit_picture/{{pic_id}}">					
			<ul >
					<li id="li_1" >
		<img src={{l_standard_resolution_url}}></img><br><br>

		</li>
		<br>
        Picture categories: <br> 
% for cat in categories:        
        <input type="checkbox" name="categories" value="{{cat}}">{{cat}}<br>
%end  

<br>Choose Exhibition: <br>
% for exi in exhibitions:        
        <input type="checkbox" name="exhibitions" value="{{exi}}">{{exi}}<br>
%end  

<br>Choose Room: <br>
% for room in rooms:        
        <input type="checkbox" name="rooms" value="{{room}}">{{room}}<br>
%end  

<br>Request sent: <br>
<input type="checkbox" name="req_sent" value="1">Sent<br>
      
		<li class="buttons">
			    <input type="hidden" name="form_id" value="946906" />
				<input id="saveForm"  type="submit" name="submit" value="Add" />
		</li>
			</ul>
		</form>	
<img id="bottom" src="{{ get_url('static', filename='bottom.png') }}" alt="">


<hr>
<br>
*** Remaining API Calls = {{api.x_ratelimit_remaining}}/{{api.x_ratelimit}}
</body>
</html>