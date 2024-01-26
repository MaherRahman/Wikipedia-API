# Install Flask and related libraries
```console
pip install flask
```
# Install pytest
```console
pip install pytest
```
# Start up the flask server
```console
python main.py
```
# Run tests using pytest
```console
pytest test.py
```
# Use whichever API platform you're comfortable with, I recommend Postman. You can now send API requests to these endpoints: 
<p> /most-viewed/<year>/<month>/<week>

/most-viewed/<year>/<month>

/view-count/<article>/<year>/<month>/<week>

/view-count/<article>/<year>/<month>

/most-viewed-day/<article>/<year>/<month>

Where items surrounded by angle brackets <> are variables that you must specify yourself. 
Ex: 
/most-viewed/<year>/<month>
would be: 
http://127.0.0.1:5000/most-viewed/2021/10
</p>

# Common issues:
Make sure the flask server is actually running before doing pytest, or using Postman or any of the API tools. 
If the flask server isn't up, or if it isn't refreshed, there could be odd behavior. I only emphasize this
because it caught me off guard when I accidentally turned off my server and things stopped working leaving me confused :). 

# Future improvements and next step
I began work on user_input.py which would prompt the user to submit the endpoint they wished to hit,
the article if any, the year, the month, and the week if any, and would then hit that endpoint for them. 
All for the sake of making the experience better for the user. 

All of this would be for the sake of integrating it with a react-app so that users can get the information on a web interface. 
However, depending on the usecase of the API, this would not be that useful for developers since they'd be hitting the API directly instead of visiting a site, but food for thought nonetheless.

Another improvement would be on testing. Right now, my tests call the wikipedia API, and are integration tests rather than full unit tests. I believe I could improve the tests by mocking the data and testing functionality only rather than using the wikipedia API and testing with that. With more time, I could clean up the tests, properly mock the data for testing purposes, and then of course, write more unit tests. 

The other improvement would of course be caching and improving speed. Right now, due to the nature of how the wikipedia API operates, some operations such as most-viewed require hitting the API several times, which can be rather slow. This cannot be avoided, however it can definitely be alleviated by storing the most-viewed data for hotspots of dates so that they don't need to continuously hit this API. 

Lastly, the code itself can be cleaned up, and following a MVC pattern, I could break main.py into separate files which would make future development more efficient. However, I felt that would be overboard for an application of this scale, particularly with the timeframe that I'm working under. 

All in all, plenty of improvements depending on the usecase of this API, however some would require much more effort which depending
on the usecase, might be excessive for an application like this. 
