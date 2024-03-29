# mooc-fi-securing-software-projects


### Installation
```
cd .\project1\

python manage.py runserver
```

### Description

LINK: https://github.com/michmaml/securing-software-mooc-fi-projects

Installation instructions:
1. navigate to project1 directory (cd .\project1\)
2. migrate models (python manage.py makemigrations)
3. run python manage.py runserver

The project is based on one of the excercises from Securing Software

---
All flaws come from OWASP's TOP 10 Web Application Security Risks (https://owasp.org/www-project-top-ten/)

---

Flaw 1 - A2:2017 - Broken Authentication:
Issue - There is only one superuser account in this application, and unfortunately, it uses the default username (admin) and password (admin). This combination of credentials is commonly used and popular, which is not for the application's safety. If an attacker guesses the keys, it will allow him/her to interact with other users, send malicious information and request money. It can also cause dire consequences because knowing the login credentials will let the intruders into the admin's dashboard. From there, removing or adding fake users will be simple for them but also dangerous for us.

Solution - There are two main approaches to prevent the attackers. Firstly, a good idea would be to obscure the admin dashboard by hiding it behind a more unintuitive URL. Currently, it is set to '/admin/', which gives out the secure panel away. It could potentially only allow users with specified IP addresses to view the page. So no person from outside of the company/owner would be able to see the page. If an attacker manages to break through and view the login box, replacing old credentials is also a must. Replacing the original 'admin/admin' with more complex strings of characters should do. It would prevent any brute-force attempts, and paired with two-factor authentication, would make the task effortful.

---

Flaw 2 - A6:2017 - Security Misconfiguration:
LINKS - 
1. https://github.com/michmaml/securing-software-mooc-fi-projects/blob/main/project1/src/pages/templates/pages/index.html#L49

2. https://github.com/michmaml/securing-software-mooc-fi-projects/blob/main/project1/src/config/settings.py#L26

Issue - Although the web application seems to be finished, there are a couple of situations exposing its vulnerabilities. The index.html (main page) of the application has three forms, and one of them does not have a CSRF token.  From the user's perspective, it works just fine, but in reality, it can cause undesired damage. What also stayed under the radar is the debug mode. A user will not know it is not disabled unless he/she goes to a non-existent page. The 404 pages can give out internal specifications and how the internal system is wired up, so nobody should access that.

Solution - Before deploying a web application, one should pay a lot of attention to what forms and user input can expose. In this case (FIRST LINK), it seems like I forgot to include a { csrf_token } inside a form in an HTML file. It shows that an unobservant programmer can cause a lot of harm unwillingly, despite using a modern framework. It shows we should not solely rely on what comes out of the box but always be mindful of how the processes work and prevent any 'leakages'.
Switching from debug mode to production is very simple and requires replacing one value in settings.py (SECOND LINK).

---

FLAW 3 - A7:2017 - Cross-Site Scripting XSS
LINK -
https://github.com/michmaml/securing-software-mooc-fi-projects/blob/main/project1/src/pages/templates/pages/index.html#L36

Issue - 'Transfer money' form includes unsecured input field 'amount'. As the whole validation happens after the value is sent to the server, there is no certainty it is not unsafe. Although the text input is eventually converted to a numeric value, there is no parsing for the Transaction model. This does not break the process of sending money but has a critical effect on the history of transactions. This means means a user can preview confidential data of other users.

Solution - The simple solution to prevent executing dangerous queries would be to either validate the input early in the endpoint handler or a better scenario would be to specify the type in the HTML file and the backend.

---

Flaw 4 - A5:2017 - Broken Access Control
LINK - https://github.com/michmaml/securing-software-mooc-fi-projects/blob/main/project1/src/pages/views.py#L50

Issue - Sending money to other people is based on a simple rule - one person's balance decreases to make other person's richer. However, this app allows the users to send money to themselves. Although this throws no error and is technically possible, makes very little sense. As a result, by sending the money to oneself, he/she will be losing it as it will never reach the receiver account.

Solution - Authenticated users are allowed to do things they are not supposed to. Together with Flaw #1 and Flaw #2, this creates a dangerous mix giving full control over users' accounts and their balances. The line that causes problems is located in views.py (LINK). It returns all accounts instead of a filtered list (without the logged user). Replacing .all() with filter() solves the problem, but it would not be able to revert lost money, so a change needs to be introduced as quickly as possible.

---

Flaw 5 - A3:2017 - Sensitive Data Exposure
LINK - https://github.com/michmaml/securing-software-mooc-fi-projects/blob/main/project1/src/pages/templates/pages/index.html#L49-L70

Issue - Apart from the 'Transfer Money' section and the transactions history, there is one more feature. All users have the option to send friendly messages to friends from their contact list. Unfortunately, the option not only allows for sending messages, but it also does not care about the message's format. It creates a dangerous vulnerability that is present to everyone. As the list of messages is not properly validated, it displays all the messages exactly as they were sent. Everyone is free to send text messages, but an attacker might opt for an image containing a request to a suspicious endpoint (similar to the Cookie Heist exercise).

Solution - To tackle this vulnerability, all messages need to be escaped. Although it is something that Django does by default, i.e. changes some character to their text equivalents( '<' for '&lt;'), I decided to add an exemption for this project (LINK). This lack of 'input textification' is commonly not a problem when using a modern framework, but can cause serious damage when a developer decides to code everything from scratch. In this example, however, removing lines 66 and 68 will fix the issue.