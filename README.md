## Eventbrite Intern Challenge App

### Decisions, Decisions, Decisions
I decided not to include any models in the site. Since I was getting all of my data from the API, I figured that it wasn't necessary to store anything in a database. Using models could have had some benefits, but I didn't think it was worth the drawbacks.

Making calls to the events/search/ portion of the API causes a noticeable delay. I could have made one longer call to the API for multiple pages when the user selected their categories, stored them, and then served the pages from the database more quickly than I could have by making an API call each time. One of the major downsides to this approach (and ultimately why I decided against it) is that it wouldn't allow the site to respond to changes on the API.

If I'm using a model to load pages 1 through 5 of a query for music events in New York City, then I will miss new events that get added or altered while the user is browsing those pages. It's unlikely that there would be a ton of activity, but since the delay for making the API call each time was relatively short, the slight speed increase didn't seem worth the risk of displaying outdated and therefore incorrect information to the user.

The events display page operates completely on GET requests. While POST requests are more secure and the standard way for a user to access the events page is through a form which ultimately involves a POST request, the get request allows users to interact with the site via the URL which I think is a great benefit. I often find myself passing values directly through the URLs of websites (including Eventbrite) to get results more quickly than finding a button.

I thought it would add a lot of value to search the events based on location, so I added a location field to the front page.

### The Nitty Gritty
Most of the interaction with the API is handled in the evbrite.py module. Perhaps the most noticeable aspect of evbrite is the ```safe_request``` wrapper. ```safe_request``` makes sure that errors due to API interaction don't crash the server by catching any errors and passing a custom ```error``` object that can be handled by the module that called it.

The ```CategoryForm``` (in eventfinder/forms.py) is populated with data from the API when the front page is requested. This is so that if there is a change on the API then the form will adapt with it.

I store the API key in an environment variable on the heroku server so that it isn't directly readable from the code.

### Acknowledgements
This site was made with Django 1.9, the Foundation front-end framework, and the heroku getting started distribution to make the site easier to host and to start with a basic Django app structure
