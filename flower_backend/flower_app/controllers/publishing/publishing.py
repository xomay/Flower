import os
import subprocess
import tempfile
from decimal import Decimal, ROUND_HALF_UP

from dateutil.relativedelta import relativedelta
from django.http import HttpResponse, FileResponse
from django.conf import settings

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import time
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

def rd(number, digits=2):
    try:
        # Essaye un arrondi précis avec Decimal
        return str(Decimal(str(number)).quantize(Decimal('1.' + '0' * digits), rounding=ROUND_HALF_UP))
    except:
        # En cas d'erreur, arrondi classique sans planter
        return str(round(float(number), digits))

def addMonths(isodate, numberOfMonths):
    if isinstance(isodate, date):
        d = isodate
    elif isodate:
        d = date.fromisoformat(str(isodate))
    else:
        d = date.today()
    return (d + timedelta(days=numberOfMonths * 30)).isoformat()


def addWeeks(isodate, numberOfWeeks):
    if isinstance(isodate, date):
        d = isodate
    elif isodate:
        d = date.fromisoformat(str(isodate))
    else:
        d = date.today()
    return (d + timedelta(weeks=numberOfWeeks)).isoformat()

def toPercent(number):
    return str(number*100)

def isNotEmpty(string):
    return len(string.replace(' ', '')) > 0

def phasesReal(phases):
    return [p for p in phases if p.index >= 0]

def phasesTransverse(phases):
    return [p for p in phases if p.index < 0]

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
        context[key] = InlineImage(doc, value, width=Mm(180))
    
    today = date.today()
    context['date'] = today.strftime('%d %B %Y')
    context['dateShort'] = today.strftime('%d/%m/%Y')
    context['today'] = today.isoformat()
    
    jinja_env = jinja2.Environment()
    jinja_env.filters['nbrToLetters'] = nbrToLetters
    jinja_env.filters['shortDate'] = shortDate
    jinja_env.filters['addMonths'] = addMonths
    jinja_env.filters['addWeeks'] = addWeeks
    jinja_env.filters['phasesReal'] = phasesReal
    jinja_env.filters['phasesTransverse'] = phasesTransverse
    jinja_env.filters['abs'] = abs

    jinja_env.globals['param'] = param
    jinja_env.globals['shortDate'] = shortDate
    jinja_env.globals['toPercent'] = toPercent
    jinja_env.globals['rd'] = rd
    jinja_env.globals['isNotEmpty'] = isNotEmpty

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

def docx_to_pdf(input_path, output_dir="/tmp"):
    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        input_path
    ], check=True)
    base = os.path.basename(input_path)
    name_without_ext = os.path.splitext(base)[0]
    return os.path.join(output_dir, f"{name_without_ext}.pdf")

def computePdf(context, doctypeFilename, name='undef', images=dict()):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
        doc = DocxTemplate(settings.DOCTYPES_LOCATION + doctypeFilename)
        docBytes = io.BytesIO()
        for key, value in images.items():
            context[key] = InlineImage(doc, value, width=Mm(180))

        today = date.today()
        context['date'] = today.strftime('%d %B %Y')
        context['dateShort'] = today.strftime('%d/%m/%Y')
        context['today'] = today.isoformat()

        jinja_env = jinja2.Environment()
        jinja_env.filters['nbrToLetters'] = nbrToLetters
        jinja_env.filters['shortDate'] = shortDate
        jinja_env.filters['addMonths'] = addMonths
        jinja_env.filters['addWeeks'] = addWeeks

        jinja_env.globals['param'] = param
        jinja_env.globals['shortDate'] = shortDate
        jinja_env.globals['toPercent'] = toPercent
        jinja_env.globals['rd'] = rd
        jinja_env.globals['isNotEmpty'] = isNotEmpty

        doc.render(context, jinja_env)
        doc.save(docBytes)
        tmp_docx.write(docBytes.getvalue())
        tmp_docx.flush()

    # 2. Convertir en PDF
    pdf_path = docx_to_pdf(tmp_docx.name)

    # 3. Retourner le PDF
    pdf_file = open(pdf_path, 'rb')
    response = FileResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = "{}.pdf"'.format(name)
    return response
