# Capstone One Project Proposal:  Adopt-A-Pet

## PhilipB[NOV20]

### Project Proposal

1. What goal will your website be designed to achieve?

        The website will be designed to help website visitors search for a potential pet within a specified distance and evaluate those potential pets. A method for recording evaluations of each animal will be provided as well as methods for changing or deleting such evaluations.Once a decision has been made the visitor can obtain the contact information to adopt the pet.

2. What kind of users will visit your site? In other words, what is the demographic of your users?

        The visitor to this web site will be looking for an individual or family pet for adoption. They will be looking for animals within a reasonable distance, want to see photos / videos of the potential pet, and having trouble making a decision on which pet to adopt.

3. What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain.

        I plan on using the Petfinder API. The API allows:

        * Search for and display pet listings based on pet characteristics, location, and status.
        * Search for and display animal welfare organizations based on organization name, ID, and location.
4. In brief, outline your approach to creating your project (knowing that you may not know everything in advance and that these details might change later). Answer questions like the ones below, but feel free to add more information:

        a. What does your database schema look like?

![schema ERD](\imgs\markdown\dbschema.jpg)

        b. What kinds of issues might you run into with your API? 

        There are two issues with the API that might lead to delays in project completion. The first is using OAuth for authentication and authorization which I have not used before. I will have to research, understand, utilize OAuth in this project. The second issue is the volume and format of the information returned by the API. This could also lead to delays to understand the operation of the API.

        c. Is there any sensitive information you need to secure? 

        The only information to secure is a password associated with a username. The username is used to login to the website so that a list of pets under consideration may be associated with a particular username.

        d. What functionality will your app include? 

        * Register
        * Login
        * Display animals meeting criteria
        * Select animal to display more information
        * Add animal to “favorites” list
        * Add evaluation to animal in “favorites” list
        * Edit evaluation of animal in “favorites” list
        * Delete evaluation of animal in “favorites” list
        * Delete animal from “favorites” list
        * Display information about animal offering animal

        e. What will the user flow look like?

![User Flow](\imgs\markdown\userflow.jpg)

        f. What features make your site more than CRUD? Do you have any stretch goals?

        The selection of a pet for inclusion in the “favorites” list and the ability to provide an evaluation of the desirability / suitability of the potential pet extends this website beyond simple CRUD. The Petfinder API will be queried based on visitor requirements and return animals meeting visitor criteria. These animals would be stored ( if interesting enough) in the website database (along with evaluation information) and used to compare potential pets so that the visitor could make a decision to adopt a particular animal as a pet.

        Future goals could be the inclusion of more information from the API particularly about the organization that is offering the animal for adoption.
