# This is Flower repo

## Flower is a ERP-CRM developed by the SI-department from Ouest-INSA(INSA Rennes J.-E.). 
It will be util to Junior enterprise, and its vocation is to be simpler to enhance than others ERP-CRM.


## Installation for production
To install Flower, you'll need the python libraries : \
psutil, requests, kaleido, django-rest-passwordreset, django-cors-headers, docx, docxtpl, num2word, plotly, pandas  (use pip) 
<pre>pip install psutil requests kaleido django-rest-passwordreset djangorestframework django-cors-headers docx docxtpl num2word num2words plotly pandas mysqlclient</pre>
Then, install also the vue librairie.
<pre>npm install -g @vue/cli</pre>
set databases settings in flower_backend/flower_backend/setting.py (see https://docs.djangoproject.com/fr/3.1/ref/settings/#databases if you want to use other SGBD than mysql) \
go in flower_frontend and do :
<pre>
npm install
npm run build
</pre>
You can now start the django server going in flower_backend : 

<pre>manage.py runserver</pre>

Don't forget to set the url routing from your web server
