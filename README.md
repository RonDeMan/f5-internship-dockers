# f5-internship-dockers

**running the project**:

docker compose up --build (there you will see at the end that the tests have passed)

open up https://localhost::8080 (ignore the self signed error and enter)

open up https://localhost:9090 (will show as an error page since its designed to be that)




**implimentation explanation**:

I have two different docker files that will build our images, on for nginx and one for the Python script that tests the implemenations.

In the nginx one I set daemon to off to have nginx run on the foreground so that the docker knows not to shut down the container.


in nginx.config I set the servers that nginx will run on https, with only the 8080 server having a rate limit of 1 per second (for testing purposes) and 10mb of storage for ip addresses (a huge amount for the scope of this test)


In the python test code I just ran the two different tests in different sections of the same test function (thought about splitting them but decided that they both use base_url and serve the base functionality of testing the implementation of the servers. could also split into two functions)

Had to disable warnings since we used a self signed ssl that would throw an error (and if you try to open localhost:8080 in your browser you will see the warning that the site uses a self signed ssl)
