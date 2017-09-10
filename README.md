Example config.json:
```json
{
  "phatText": "Example scrolling banner text",
  "endpoint": "http://your.endpoint.url",
  "username": "rustyShackleFerd",
  "password": "hunter2"
}
```

Make sure to include relevant properties in the Jenkins job list:
```json
/job/ui/api/json?pretty=true&tree=jobs[name,color,lastBuild[timestamp]]
```
