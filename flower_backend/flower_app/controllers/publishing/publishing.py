from django.http import HttpResponse
from django.conf import settings

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

import threading
import locale, io, sys
locale.setlocale(locale.LC_TIME, "fr_FR.utf8")
from datetime import date, timedelta
import jinja2
from num2words import num2words
from ...models.ParamsJE import ParamsJE

def nbrToLetters(number):
    return num2words(number, lang='fr')

def shortDate(isodate):
    return date.fromisoformat(str(isodate)).strftime('%d/%m/%Y')

def rd(number):
    return str(round(number, 2))

def addMonths(isodate, numberOfMonths):
    return (date.fromisoformat(str(isodate)) + timedelta(days=numberOfMonths * 30)).isoformat()

def toPercent(number):
    return str(number*100)

def generateGantt(etude):
    
    th = threading.Thread(target=deleteImage, args=('users.csv'))
    return InlineImage(tpl,'test_files/python_logo.png',width=Mm(20))

def param(value):
    try:
        return getattr(ParamsJE.objects.get(pk=1), value)
    except:
        print("ERROR : parameter ["+value+"] doesn't exist.", file=sys.stderr)
        return "(!! ERROR : bad field name: '"+value+"' !!)"

def computeDocx(context, doctypeFilename, name='undef', images=dict()):
    doc = DocxTemplate(settings.DOCTYPES_LOCATION + doctypeFilename)
    docBytes = io.BytesIO()
    for key, value in images.items():
        context[key] = InlineImage(doc, value, width=Mm(160))
    
    today = date.today()
    context['date'] = today.strftime('%d %B %Y')
    context['dateShort'] = today.strftime('%d/%m/%Y')
    
    jinja_env = jinja2.Environment()
    jinja_env.filters['nbrToLetters'] = nbrToLetters
    jinja_env.filters['shortDate'] = shortDate
    jinja_env.filters['addMonths'] = addMonths
    
    jinja_env.globals['param'] = param
    jinja_env.globals['shortDate'] = shortDate
    jinja_env.globals['toPercent'] = toPercent
    jinja_env.globals['rd'] = rd

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
