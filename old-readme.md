# This is Flower repo

## Flower is a ERP-CRM developed by the SI-department from Ouest-INSA (INSA Rennes J.-E.). 
It will be useful for Junior-Enterprise, and its vocation is to be simpler to improve than others ERP-CRM.

## Installation for developpement (docker)

Install `docker` and `docker-compose` and run 
```
sudo docker-compose up --build
```

## Installation for developpement (manual)

### Back-end

To install Flower, you'll need the Python 3.8 and the python libraries listed in `flower_backend/requirements.txt`  
<pre>sudo apt install python3.8 python3-pip</pre>
<pre>pip3 install -r flower_backend/requirements.txt</pre>
Then, install also the vue librairie.
<pre>npm install -g @vue/cli</pre>
Set the database settings in `flower_backend/flower_backend/setting.py` (see https://docs.djangoproject.com/fr/3.1/ref/settings/#databases if you want to use an other SGBD than mysql)  
You can now start the django server by going in the `flower_backend` directory : 
<pre>python manage.py runserver</pre>

### Front-end

Go in the `flower_frontend` directory and do :
<pre>
npm install
npm run serve
</pre>

## Installation for production

### Back-end 

See https://docs.djangoproject.com/fr/3.1/howto/deployment/ to setup the backend on a production server

### Front-end

Go in the `flower_frontend` directory and do :
<pre>
npm install
npm run build
</pre>

Don't forget to set the url routing from your web server

## Contribute to the Flower project

To contribute to the project, please follow these steps: 
- Create an issue explaining what you want to do
- Create a merge request and a branch from the issue
- Write your code
- Once you're finished, be sure that your branch is up-to-date with the `dev` branch and push the merge if necessary : 
```
git checkout dev
git pull
git checkout your_branch
git merge dev
git push [only if necessary]
```
- In gitlab, remove the Draft state
