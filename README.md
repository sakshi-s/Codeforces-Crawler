# Codeforces-Crawler #
It scrapes Codeforces contests schedule using Beautiful Soup and displays it in a Django based website. It can extract profile and contests stats info of a given user and show them pictorially. Implements authentication features like register, login and logout and the users can chat with each other. It also shows IITG leaderboard on Codeforces.

## Tech Stack ##
* Frontend: HTML/CSS
* Backend: Django
## How to run? ##
* Fork and Clone the repo:
git clone https://github.com/<your-username>/Codeforces-Crawler.git
* Create a branch:
git checkout -b <branch-name>
* Create virtual environment:
python -m venv env
env\Scripts\activate
* Change Directory:
cd CodeforcesCrawler
* Install dependencies using : 
pip install -r requirements.txt
* Make migrations using
python manage.py makemigrations
* Migrate Database
python manage.py migrate
* Create a superuser
python manage.py createsuperuser
* Run server using
python manage.py runserver
* Push Changes
git add .
git commit -m "<your commit message>"
git push --set-upstream origin <branch_name>
