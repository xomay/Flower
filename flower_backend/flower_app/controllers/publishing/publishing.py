from django.http import HttpResponse

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

import locale
locale.setlocale(locale.LC_TIME, "fr_FR.utf8")
from datetime import date, timedelta
import jinja2
from num2words import num2words
import io

def nbrToLetters(number):
    return num2words(number, lang='fr')

def shortDate(isodate):
    return date.fromisoformat(str(isodate)).strftime('%d/%m/%Y')

def addMonths(isodate, numberOfMonths):
    return (date.fromisoformat(str(isodate)) + timedelta(days=numberOfMonths * 30)).isoformat()

parameters = {
    'nom': 'Ouest INSA',
    'adresse': '20 avenue des Buttes de Coësmes, 35708 Rennes, CS 70839 Cedex 7',
    'email': 'contact@ouest-insa.fr',
    'presidentPrenom': 'presidentPrenom',
    'presidentNom': 'presidentNom',
    'tva': 0.2
}

def param(value):
    return "oui" #getattr(GLOBAL_PARAMS_JE, value)

def computeDocx(context, doctypeFilename, name='undef', images=dict()):
    doc = DocxTemplate('doctypes/' + doctypeFilename)
    docBytes = io.BytesIO()
    for key, value in images.items():
        context[key] = InlineImage(doc, value, width=Mm(160))

    #print("ouais ouais ouais > " + param("je_name"))

    today = date.today()
    context['date'] = today.strftime('%d %B %Y')
    context['dateShort'] = today.strftime('%d/%m/%Y')
    
    jinja_env = jinja2.Environment()
    jinja_env.filters['nbrToLetters'] = nbrToLetters
    jinja_env.filters['shortDate'] = shortDate
    jinja_env.filters['addMonths'] = addMonths
    
    jinja_env.globals['param'] = param

    doc.render(context, jinja_env)
    doc.save(docBytes)

    docBytes.seek(0)
    response = HttpResponse(
        docBytes.getvalue(), 
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    response["Content-Disposition"] = 'attachment; filename = "{}.docx"'.format(name)
    response["Content-Encoding"] = "UTF-8"
    return response
