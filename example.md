# Example Execution
This is an example of a scan request sent to the `/scan` endpoint, followed by sample logs emitted by the containers involved in processing the job (`api`, `resolve_queue`, `http_check_queue`, `browser_capture_queue`).

## Request
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/scan' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "domain": "apple.com",
  "wildcard": true
}'
```

## Logs

```bash
resolve_queue-1          | INFO:saq:Worker starting: RedisQueue<redis=<redis.asyncio.client.Redis(<redis.asyncio.connection.ConnectionPool(<redis.asyncio.connection.Connection(host=redis,port=6379,db=0)>)>)>, name='resolve'>       
http_check_queue-1       | INFO:saq:Worker starting: RedisQueue<redis=<redis.asyncio.client.Redis(<redis.asyncio.connection.ConnectionPool(<redis.asyncio.connection.Connection(host=redis,port=6379,db=0)>)>)>, name='http_check'>
browser_capture_queue-1  | INFO:saq:Worker starting: RedisQueue<redis=<redis.asyncio.client.Redis(<redis.asyncio.connection.ConnectionPool(<redis.asyncio.connection.Connection(host=redis,port=6379,db=0)>)>)>, name='browser_capture'>
api-1                    | INFO:     Started server process [1]
api-1                    | INFO:     Waiting for application startup.
api-1                    | INFO:     Application startup complete.                                                                                                                                                                     
api-1                    | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)                                                                                                                                     
api-1                    | INFO:     172.24.0.1:37422 - "POST /scan HTTP/1.1" 200 OK                                                                                                                                                   
resolve_queue-1          | INFO:saq:Processing Job<function: resolve_domain, queue: resolve, key: e4386208-5db5-11f0-865f-0242ac180005, attempts: 1, queued: 1752169624784, started: 1752169624787, touched: 1752169624787>
resolve_queue-1          | INFO:app.tasks.resolve:Resolving domain: apple.com | wildcard=True                                                                                                                                          
resolve_queue-1          | INFO:app.tasks.resolve:Resolved root domain: apple.com                                                                                                                                                      
resolve_queue-1          | INFO:saq:Enqueuing Job<function: http_check, queue: http_check, key: e43d5092-5db5-11f0-bc50-0242ac180006, queued: 1752169624817>
http_check_queue-1       | INFO:saq:Processing Job<function: http_check, queue: http_check, key: e43d5092-5db5-11f0-bc50-0242ac180006, attempts: 1, queued: 1752169624817, started: 1752169624820, touched: 1752169624820>             
http_check_queue-1       | INFO:app.tasks.http_check:Running http_check for apple.com
resolve_queue-1          | INFO:app.tasks.resolve:Resolved subdomain: www.apple.com                                                                                                                                                    
resolve_queue-1          | INFO:saq:Enqueuing Job<function: http_check, queue: http_check, key: e443319c-5db5-11f0-bc50-0242ac180006, queued: 1752169624855>
resolve_queue-1          | INFO:app.tasks.resolve:Subdomain did not resolve: mail.apple.com                                                                                                                                            
resolve_queue-1          | INFO:app.tasks.resolve:Subdomain did not resolve: login.apple.com
resolve_queue-1          | INFO:app.tasks.resolve:Subdomain did not resolve: admin.apple.com
resolve_queue-1          | INFO:app.tasks.resolve:Subdomain did not resolve: api.apple.com
resolve_queue-1          | INFO:saq:Finished Job<function: resolve_domain, queue: resolve, key: e4386208-5db5-11f0-865f-0242ac180005, attempts: 1, completed: 1752169624989, queued: 1752169624784, started: 1752169624787, touched: 1752169624787>                                                                                                                                                                                                                           
http_check_queue-1       | INFO:app.tasks.http_check:HTTP check succeeded for apple.com with status 200
http_check_queue-1       | INFO:saq:Processing Job<function: http_check, queue: http_check, key: e443319c-5db5-11f0-bc50-0242ac180006, attempts: 1, queued: 1752169624855, started: 1752169625321, touched: 1752169625321>
http_check_queue-1       | INFO:app.tasks.http_check:Running http_check for www.apple.com                                                                                                                                              
http_check_queue-1       | INFO:app.tasks.http_check:HTTP check succeeded for www.apple.com with status 200                                                                                                                            
http_check_queue-1       | INFO:saq:Enqueuing Job<function: browser_capture, queue: browser_capture, key: e48a1f26-5db5-11f0-9af7-0242ac180004, queued: 1752169625320>
browser_capture_queue-1  | INFO:saq:Processing Job<function: browser_capture, queue: browser_capture, key: e48a1f26-5db5-11f0-9af7-0242ac180004, attempts: 1, queued: 1752169625320, started: 1752169625463, touched: 1752169625463>   
http_check_queue-1       | INFO:saq:Finished Job<function: http_check, queue: http_check, key: e43d5092-5db5-11f0-bc50-0242ac180006, attempts: 1, completed: 1752169625463, queued: 1752169624817, started: 1752169624820, touched: 1752169624820>                                                                                                                                                                                                                            
browser_capture_queue-1  | INFO:app.tasks.browser_capture:Running browser_capture for apple.com
http_check_queue-1       | INFO:saq:Enqueuing Job<function: browser_capture, queue: browser_capture, key: e49f9568-5db5-11f0-9af7-0242ac180004, queued: 1752169625461>
browser_capture_queue-1  | INFO:saq:Processing Job<function: browser_capture, queue: browser_capture, key: e49f9568-5db5-11f0-9af7-0242ac180004, attempts: 1, queued: 1752169625461, started: 1752169625477, touched: 1752169625477>   
http_check_queue-1       | INFO:saq:Finished Job<function: http_check, queue: http_check, key: e443319c-5db5-11f0-bc50-0242ac180006, attempts: 1, completed: 1752169625464, queued: 1752169624855, started: 1752169625321, touched: 1752169625321>                                                                                                                                                                                                                            
browser_capture_queue-1  | INFO:app.tasks.browser_capture:Running browser_capture for www.apple.com
browser_capture_queue-1  | INFO:app.tasks.browser_capture:Screenshot saved: /evidence/www.apple.com.png
browser_capture_queue-1  | INFO:app.tasks.browser_capture:Screenshot saved: /evidence/apple.com.png
browser_capture_queue-1  | INFO:app.tasks.browser_capture:Inserting scan result into Mongo for www.apple.com                                                                                                                           
browser_capture_queue-1  | INFO:app.tasks.browser_capture:Inserting scan result into Mongo for apple.com                                                                                                                               
browser_capture_queue-1  | INFO:saq:Finished Job<function: browser_capture, queue: browser_capture, key: e48a1f26-5db5-11f0-9af7-0242ac180004, attempts: 1, completed: 1752169628385, queued: 1752169625320, started: 1752169625463, touched: 1752169625463>
browser_capture_queue-1  | INFO:saq:Finished Job<function: browser_capture, queue: browser_capture, key: e49f9568-5db5-11f0-9af7-0242ac180004, attempts: 1, completed: 1752169628386, queued: 1752169625461, started: 1752169625477, touched: 1752169625477>                                                   
```