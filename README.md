# astronomyNotifier
This will be a app that can tell you information about what you can see in the sky, and send notifications about big events. 


To run the project, use 
'''bash
poetry run python src/main.py
'''
you can then visit http://localhost:5000 to query the api


To run all tests and generate a html coverage report, use
'''bash
poetry run pytest --cov=src/ --cov-report=html tests/
'''

For deployment you may use the Docker file. To build run

```
sudo docker build -t astronomynotifier .
```

and then to run
```
docker run -p 80:80 astronomynotifier
```

