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

Flaw 1 - A2:2017 - Broken Authentication:
Issue - There is only one superuser account in this application, and unfortunately, it uses the default username (admin) and password (admin). This combination of credentials is commonly used and popular, which is not for the application's safety. If an attacker guesses the keys, it will allow him/her to interact with other users, send malicious information and request money. It can also cause dire consequences because knowing the login credentials will let the intruders into the admin's dashboard. From there, removing or adding fake users will be simple for them but also dangerous for us.
Solution - There are two main approaches to prevent the attackers. Firstly, a good idea would be to obscure the admin dashboard by hiding it behind a more unintuitive URL. Currently, it is set to '/admin/', which gives out the secure panel away. It could potentially only allow users with specified IP addresses to view the page. So no person from outside of the company/owner would be able to see the page. If an attacker manages to break through and view the login box, replacing old credentials is also a must. Replacing the original 'admin/admin' with more complex strings of characters should do. It would prevent any brute-force attempts, and paired with two-factor authentication, would make the task effortful.

Flaw 2 - A6:2017 - Security Misconfiguration:
LINK(S) - 
1. https://github.com/michmaml/securing-software-mooc-fi-projects/blob/main/project1/src/pages/templates/pages/index.html#L49

2. https://github.com/michmaml/securing-software-mooc-fi-projects/blob/main/project1/src/config/settings.py#L26

Issue - Although the web application seems to be finished, there are a couple of situations exposing its vulnerabilities. The index.html (main page) of the application has three forms, and one of them does not have a CSRF token.  From the user's perspective, it works just fine, but in reality, it can cause undesired damage. What also stayed under the radar is the debug mode. A user will not know it is not disabled unless he/she goes to a non-existent page. The 404 pages can give out internal specifications and how the internal system is wired up, so nobody should access that.
Solution - Before deploying a web application, one should pay a lot of attention to what forms and user input can expose. In this case (FIRST LINK), it seems like I forgot to include a { csrf_token } inside a form in an HTML file. It shows that an unobservant programmer can cause a lot of harm unwillingly, despite using a modern framework. It shows we should not solely rely on what comes out of the box but always be mindful of how the processes work and prevent any 'leakages'.
Switching from debug mode to production is very simple and requires replacing one value in settings.py (SECOND LINK).
