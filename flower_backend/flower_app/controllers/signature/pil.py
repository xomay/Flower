from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from http import HTTPStatus
import io
from django.conf import settings

from flower_app.models.ParamsJE import ParamsJE

def createSignature(membre):
    try:
        params = ParamsJE.objects.get(pk=1)
    except:
        return HttpResponse("Les paramètres de la JE n'ont pas été instanciés !", status=HTTPStatus.SERVICE_UNAVAILABLE)

    image = Image.open(settings.SIGNATURE_LOCATION + 'signature_basee.png')
    image_editable = ImageDraw.Draw(image)

    text_font = ImageFont.truetype("arial.ttf", 22)
    text_font_bold = ImageFont.truetype("ariblk.ttf", 23)

    hrz_offset = 350
    vrt_offset = 20
    line_offset = 32
    post_bold_offset = 7

    # <prénom nom> • <poste>
    nomPrenom = membre.firstname + ' ' + membre.lastname
    image_editable.text((hrz_offset,vrt_offset), nomPrenom, (50, 48, 68), font=text_font_bold)

    posteName = (membre.poste.name_feminine, membre.poste.name)[membre.gender == 'M.']
    if posteName != '':
        sizeNomPrenom = image_editable.textsize(nomPrenom, font=text_font_bold)[0]
        image_editable.text((hrz_offset + 10 + sizeNomPrenom,vrt_offset + post_bold_offset), '• ' + posteName, (85, 85, 85), font=text_font)
    # ☎ <Téléphone JE> • 📞 <numéro de téléphone>
    image_editable.text((hrz_offset,vrt_offset+line_offset), '☎ '+ params.je_phone + ' • 📞 ' + membre.mobile, (85, 85, 85), font=text_font)
    # 💼 <nom je> • <slogan>
    jeName = '💼 '+ params.je_name
    image_editable.text((hrz_offset,vrt_offset+line_offset*2), jeName, (85, 85, 85), font=text_font_bold)
    sizeJeName = image_editable.textsize(jeName, font=text_font_bold)[0]
    image_editable.text((hrz_offset + 5 + sizeJeName,vrt_offset+line_offset*2+post_bold_offset), '• ' + params.je_slogan, (85, 85, 85), font=text_font)
    # 🌎 <url> • ✉ <addresse mail>
    image_editable.text((hrz_offset,vrt_offset+line_offset*3), '🌎 '+ params.je_url + ' • ✉ ' + membre.email_junior, (50, 48, 68), font=text_font)

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return HttpResponse(img_byte_arr, content_type="image/png", status=HTTPStatus.OK)

"""
# <prénom nom> • <poste>
    nomPrenom = membre.firstname + ' ' + membre.lastname
    sizeNomPrenom = image_editable.textsize(nomPrenom, font=text_font_bold)[0]
    image_editable.text((155,11), nomPrenom, (50, 48, 68), font=text_font)
    posteName = (membre.poste.name_feminine, membre.poste.name)[membre.gender == 'M.']
    if posteName != '':
        image_editable.text((148 + sizeNomPrenom,11), '• ' + posteName, (85, 85, 85), font=text_font)
    # ☎ <Téléphone JE> • 📞 <numéro de téléphone>
    # 💼 <nom je> • <slogan>
    image_editable.text((313,29), membre.mobile, (50, 48, 68), font=text_font_text)
    # 🌎 <url> • <addresse mail>
    image_editable.text((300,63), membre.email_junior, (50, 48, 68), font=text_font_text)
"""