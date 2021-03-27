# 312_project

Social space game where users will have options to both customize their profile/avatar and communicate with other players/users.
Players will be able to navigate around a social space populated by all other users online. They will then be able to click on other players in order to open a window and chat with them. Players will be able to edit their username and avatars.
Django is the framework of choice

To run django the webpage: cd into mysite, enter the command "python manage.py runserver" then navigate to http://127.0.0.1:8000/

To view Overworld cd into Game, enter command python3 server.py, and navigate to localhost:8000. The current version attempts to read a json string to parse and update all player position on screen. Once a database is established we intended to send a json string to all users where they can parse and update the Overworld on their end while sending their position as a json back to the server. 

To test json function, $ npm i -g json-server then $ json-server --watch players.json 
Any update to the file will seen when navigating to localhost:8000/Add  
This method was used to test parsing and will change. 
