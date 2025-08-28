## Make the run script executable:
```
chmod +x /home/alaeddin/MCP/mcp_docker_test1/run.sh
```


## Build and start the container:
```
./run.sh --build
./run.sh --run
```


## Test the server connection:
```
curl -i http://localhost:8080/sse
```


## Run the test client:

```
python test_client.py
```

```
cd docker/ && docker-compose down && cd .. && ./run.sh --build && ./run.sh --run
```