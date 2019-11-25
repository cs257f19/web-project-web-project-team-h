# About this repository
This is the repository for the term-long database-driven web project in
CS 257, Fall 2019.

To run the website:
- $python3 webapp.py perlman.mathcs.carleton.edu PORT-NUMBER

Contents:
- Personas: directory, contains all personas developed for this project
- UserStories: directory, contains all the user stories
- Data: directory, contains the raw Airbnb in NYC data
- Backend: directory, contains all backend data query and processing functions
  - datasource.py: python file, contains database queries, data processing, and
      we applied useful data structure(s) for our data
- Webpages: directory, contains mediator and frontend code for this project
  - webapp.py: python file, contains mediator functions that translate needs
      from the frontend to the backend and translate the provided data from the
      backend to the frontend
  - static: directory, contains all css files and pictures
  - templates: directory, contains all html files
    - homePage.html: home page of the entire project about Airbnb in NYC
      ![homePage](https://github.com/cs257f19/web-project-web-project-team-h/blob/master/Screenshots/homePage.png)
    - dataPage.html: "about data" page that includes metadata and description
        of the entire dataset
    - overall.html: "visualize data" page that provides visualizations for the
        overall statistics of the NYC Airbnb data. This gives researchers and
        investigators a good overall understanding of how Airbnb performs in
        NYC in general
        ![overallPage](https://github.com/cs257f19/web-project-web-project-team-h/blob/master/Screenshots/overallPage.png)
    - hostPage.html: host page that asks hosts to enter their airbnb host id.
        Note that non-hosts can test the page by using the host id examples we
        give on the "about data" page
    - hostResult.html: host result page that displays relevant information of
        their listings and listings of the same room type in the same
        neighborhood. This allows hosts to learn more about the competitions
        associated with their listings
    - searchPage.html: listing search page that allows tourists to search for
        housing of interest by asking them for ideal price range, neighborhood
        group, and room type
        ![searchPage](https://github.com/cs257f19/web-project-web-project-team-h/blob/master/Screenshots/searchPage.png)
    - searchResult.html: listing search result page that shows the listings that
        satisfy the search criterion on a map. If there are more than 100
        listings found, we only display the first 100 listings with the most
        reviews
    - errorPage.html: error page that displays a descriptive message according
        to the error made by the user and/or the system

Here are some ways we violate MVC practice and here is why:
- There are places in javascript where we used methods from the `Datasource`
  class and `Listing` class. Both of these classes are implemented in
  Backend/datasource.py and the methods should have been called in
  Webpages/webapp.py instead of in javascript. However, we violated the MVC
  practice because:
  - We called the `getAllListingsOfType` method, because this function needs
    to be called for each listing in a list of listings that we pass from
    webapp.py to javascript. Essentially, this is a second level query, and
    to ensure our code is clean, we had to violate the MVC practice.
  - We made calls to the getters of the `Listing` class, because we need
    almost all information for the `Listing` objects. If we made these calls
    in webapp.py and restructured them into a new data structure just for
    javascript to use, it would be repetitive functionality and unclean
    coding practice. Therefore, we violated the MVC practice here as well.

NOTE: To meet the goal of our core audiences, we narrowed down the scope of
the project by removing one audience (business owners). However, we still
decided to keep our original personas and user stories because they witnessed
the development process and are features one could add if one wants to extend
our project to a wide range of audiences.
