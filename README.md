# CRUD application
Here is a small CRUD application build with FastAPI to demonstrate what can be done with this tool. It has a list of tasks initially (as list of dictionaries), the user can get the list, details of a particular task, add a new task, edit it or/and delete. 
Before lauching it install FastAPI with 
The command to launch it is just 
```
python main.py
```

## Documentation
At http://localhost:8000/docs will be available description of all endpoints.
![Swagger documentation](SwaggerUI.png)

## Testing
How to test with "curl":
```
curl -i -X POST http://localhost:8000/tasks \     
     -H "Content-Type: application/json" \
     -d '{"title": "    "}'
```
Response will be:
```
HTTP/1.1 400 Bad Request
date: Mon, 20 Jul 2026 11:35:59 GMT
server: uvicorn
content-length: 57
content-type: application/json
{"detail":"Title cannot be empty or contain only spaces"}% 
```

```
curl -i -X POST http://localhost:8000/tasks \ 
     -H "Content-Type: application/json" \
     -d '{"title": "Buy milk"}'
```
Response:
```
HTTP/1.1 201 Created
date: Mon, 20 Jul 2026 11:36:29 GMT
server: uvicorn
content-length: 40
content-type: application/json
{"id":4,"title":"Buy milk","done":false}%
```

In order to test PUT and DELETE following curl-strings can be used:
```
curl -X PUT "http://localhost:8000/tasks/4" -H "Content-Type: application/json" -d '{"title": "Byu milk and eggs", "done": true}'

curl -i -X DELETE http://localhost:8000/tasks/4 
```
---
Some new features has been added:
### search by parameters
Searching tasks by their status
```
 curl -s "http://127.0.0.1:8000/tasks?done=true" | json_pp
```
Respose:
```
[
   {
      "done" : true,
      "id" : 2,
      "title" : "Create first endpoint"
   }
]
```
Searching tasks by any word in the title
```
curl -s "http://127.0.0.1:8000/tasks?search=FastAPI" | json_pp
```
Response:
```
[
   {
      "done" : false,
      "id" : 1,
      "title" : "Install FastAPI"
   }
]
```
To get statistic information (how many tasks are in the list) use GET /stats:
```
curl -i http://localhost:8000/stats
```
Example of responce:
```
server: uvicorn
content-length: 29
content-type: application/json

{"total":3,"done":1,"open":2}%     
```
To reset the list of tasks to initial values use POST /reset:
```
curl -X POST http://localhost:8000/reset
```