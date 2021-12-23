# Fampay Backend Assignment

### This project was made as an assignment for github externship. It is a django server which fetches youtube data and stores it and return to user when requested. It is made using django , rest_framework.
## Functionalities : 

1. GET complete list of queries required in tabulated manner.
2. Search Videos based on description and title queries.
3. Tables are updated every 10 seconds using Threading Technique

### Code Style :
    Numpy Style followed in docstring.


## Installation 
1. Install any suitable version of python. Also, ensure that pip is also installed along with it.

2. Run following commands in the same directory as <b>manage.py</b>

<br>

```
pip install < requirements.txt
python manage.py makemigrations
python manage.py migrate
```

3. Rename .env.sample to .env

4. Set the parameters <b>query</b> in the <b>query.py</b> file which is inside the *api* Directory
<ul>
<li>query - Any Query which is to be searched.</li>
</ul>

5. Run the django server using
```
python manage.py runserver
```

It runs the backend server at default port 8000. As well schedules a job on a different thread to fetch youtube videos and store it in the database after specific intervals. Open http://localhost:8000 to view it in the browser.
## Usage 
This API has two basic functionalities : 

1. View List of Videos in paginated format:
Send a <b>GET</b> Request to url: http://localhost:8000/api/videolist/
 without any params.

2. Search for Videos based on a specific query

Send a <b>GET</b> Request to url : 
http://localhost:8000/api/search/ with no params but body(in JSON format) as follows : 

To search using Title
```
{
    "title" : "Your_title_here"
}
```

To search using description
```
{
    "description" : "Your_description_here" 
}
```
