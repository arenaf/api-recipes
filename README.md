# API Recipes

![api-recipes-banner](https://github.com/user-attachments/assets/5816cc56-01c5-480d-af48-337e969ea5c8)


This project has been developed with ***Python*** and the following libraries and tools: ***Flask***, ***SQLAlchemy***, ***WTForm***, ***JWT-extended***, ***Postman***, ***Bootstrap*** and ***HTML***.

This is a website that allows uploading, modifying and deleting recipes (**CRUD**). Only logged-in users can make changes to the recipe, if the user is not logged in, they will only be able to view it.

![init](https://github.com/user-attachments/assets/a22d68d2-3cf1-46ed-874a-551da12f1517)


## Application management

To start uploading recipes, a new user must access the login page. Any user who tries to post without being logged in will be redirected to the login page.

Both the login page and the registration page have correct email verifications.

Other verifications (included in the login, registration and password change pages):
- An existing user cannot re-register with the same email address.
-	On the registration and password change pages, you have to repeat the password twice, it returns an error if they do not match.
- If the email exists, but the password is incorrect, it shows a password error.
-	All fields are required.
-	A user that does not exist cannot change the password or log in, it will show an error that the email does not exist.
  

## Interact with recipes from the web and from the API

### Web

Once a user is logged in, he can upload a recipe, modify it if he has detected an error or delete it. These last two actions can only be performed on recipes in which he/she is the author.

From the main menu any user can filter by type of meal: Breakfast, Dinner, Lunch, Snack, Starters and All recipes. In addition, a logged-in user will be able to see the option ‘My Recipes’, where they will have the recipes that have been created by them.


![see-my-recipe](https://github.com/user-attachments/assets/19cadff0-51fb-4c1c-9882-7a178cb0c269)


### API

The same actions can be performed from the API as from the web, with the difference that for actions such as creating, modifying, deleting or viewing my recipes, it is necessary to enter the token.

Any user with a login can access their token from the **menu bar** - **API** and click on **‘Get Token’**.

![API-logged-in](https://github.com/user-attachments/assets/05ecfc40-4c1e-4f27-8e61-eababea955e5)

All the information on how to perform queries from the API is available at: https://documenter.getpostman.com/view/34666668/2sAXjNWqZa


## Requirements
- Python
- Flask
- SQLAlchemy
- WTForms
- Bootstrap
- Flask JWT Extended


