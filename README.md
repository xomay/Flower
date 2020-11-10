#This is Flower repo

##Flower is a ERP-CRM developed by the SI-department from Ouest-INSA(INSA Rennes J.-E.). 
It will be util to Junior enterprise, and its vocation is to be simpler to enhance than others ERP-CRM.


##Installation for production
To install Flower, you'll need the python libraries : \
psutil, requests, kaleido, django-rest-passwordreset, django-cors-headers, docx, docxtpl, num2word, plotly, pandas  (use pip)\
<pre>pip install psutil requests kaleido django-rest-passwordreset django-cors-headers docx docxtpl num2word plotly pandas</pre>
Then, install also npm library from -g electron@6.1.4 orca:
<pre>npm install -g electron@6.1.4 orca</pre>
go in flower_frontend and do :
<pre>
npm install
npm run build
</pre>
You can now start the django server going in flower_backend : 
<pre>manage.py runserver</pre>
Don't forget to set the url routing from your web server
