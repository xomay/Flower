from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from http import HTTPStatus
import io
from django.conf import settings

from flower_app.models.ParamsJE import ParamsJE

def betterMobile(mobile):
    mobile = ' '.join(a+b for a,b in zip(mobile[::2], mobile[1::2]))
    if mobile[0] == '0':
        return '(+33) (0)' + mobile[1:]
    return mobile

def createSignature(membre):
    try:
        params = ParamsJE.objects.get(pk=1)
    except:
        return HttpResponse("Les paramètres de la JE n'ont pas été instanciés !", status=HTTPStatus.SERVICE_UNAVAILABLE)

    image = Image.open(settings.OTHERS_LOCATION + 'signature_base.png')
    image_editable = ImageDraw.Draw(image)

    text_font = ImageFont.truetype(settings.OTHERS_LOCATION + 'arial.ttf', 22)
    text_emote = ImageFont.truetype(settings.OTHERS_LOCATION + 'OpenSansEmoji.ttf', 22)
    text_font_bold = ImageFont.truetype(settings.OTHERS_LOCATION + 'ariblk.ttf', 23)

    hrz_offset = 350
    vrt_offset = 20
    line_offset = 33
    post_bold_offset = 7

    # <prénom nom> • <poste>
    nomPrenom = membre.firstname + ' ' + membre.lastname
    image_editable.text((hrz_offset,vrt_offset), nomPrenom, (50, 48, 68), font=text_font_bold)

    posteName = (membre.poste.name_feminine, membre.poste.name)[membre.gender == 'M.']
    if posteName != '':
        bbox_nom = image_editable.textbbox((0, 0), nomPrenom, font=text_font_bold)
        sizeNomPrenom = bbox_nom[2] - bbox_nom[0]
        image_editable.text((hrz_offset + 10 + sizeNomPrenom,vrt_offset + post_bold_offset), '• ' + posteName, (85, 85, 85), font=text_font)
    # ☎ <Téléphone JE> • 📞 <numéro de téléphone>
    vrt_offset += 3
    mobile_text = ""
    if membre.mobile != "":
        mobile_text = ' • 📞 ' + betterMobile(membre.mobile)
    image_editable.text((hrz_offset,vrt_offset+line_offset), '☎ '+ params.je_phone + mobile_text, (85, 85, 85), font=text_emote)
    # 💼 <nom je> • <slogan>
    jeEmote = '💼 '
    image_editable.text((hrz_offset,vrt_offset+line_offset*2), jeEmote, (85, 85, 85), font=text_emote)
    bbox_emote = image_editable.textbbox((0, 0), jeEmote, font=text_emote)
    sizeJeEmote = bbox_emote[2] - bbox_emote[0]
    jeName = params.je_name
    image_editable.text((hrz_offset+sizeJeEmote,vrt_offset+line_offset*2), jeName, (50, 48, 68), font=text_font_bold)
    bbox_jeName = image_editable.textbbox((0, 0), jeName, font=text_font_bold)
    sizeJeName = (bbox_jeName[2] - bbox_jeName[0]) + sizeJeEmote
    image_editable.text((hrz_offset + 5 + sizeJeName,vrt_offset+line_offset*2+3), '• ' + params.je_slogan, (85, 85, 85), font=text_emote)
    # 🌎 <url> • ✉ <addresse mail>
    vrt_offset += 3
    image_editable.text((hrz_offset,vrt_offset+line_offset*3), '🌎 '+ params.je_url + ' • 📧 ' + membre.email_junior, (85, 85, 85), font=text_emote)

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return HttpResponse(img_byte_arr, content_type="image/png", status=HTTPStatus.OK)
