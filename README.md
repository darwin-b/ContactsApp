# ContactsApp

> Language : python
> FrameWork : Django
> Databse : Mysql

> Configure DB settings in settings.py file in ContactsApp directory. {Refer the DB configurations Screenshot}
> Create Database manually in mysql with DB name as "Contacts". {Execute Below comands in mysql}
	DROP Database contacts;
	CREATE Database contacts;

> Execute following commands from terminal in ContactsApp folder:
	python manage.py migrate
	python manage.py runserver

> open:
	http://localhost:{portnumber}

> portnumber-->from development server started by executing runserver command above


> Assumptions:
>> First Name is required
>> Working & general assumptions are analogus to a typical contact app in our mobile phone.
	eg: We can save a contact with just first name & other empty fields.
	
