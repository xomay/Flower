from django.http import HttpResponse
from http import HTTPStatus
import plotly.express as px
from plotly.io import to_html, to_image
import pandas as pd
import io
import base64
from datetime import date, timedelta

import locale
locale.setlocale(locale.LC_TIME, "fr_FR.utf8")

def computeGanttFromEtude(etude, image_format="jpg"):
    data = []
    for groupe in etude.groupe_set.order_by('index').iterator():
        for phase in groupe.phase_set.order_by('index').iterator():
            data.append(dict(Phase=phase.title + " ", Début=phase.beginDate, Fin=phase.finishDate, Groupe=str(groupe)))

    if len(data) > 0 :
        df = pd.DataFrame(data)
        fig = px.timeline(df, x_start="Début", x_end="Fin", y="Phase", color="Groupe")
        fig.update_yaxes(autorange="reversed", ticks="outside") # otherwise tasks are listed from the bottom up
        fig.update_xaxes(tickformat='%d/%m/%y')
        fig.update_layout(showlegend=False)

        if image_format == "svg":
            fig_img = to_image(fig, format="svg")
            response = HttpResponse(fig_img, content_type="image/svg+xml")
            return response
        else:
            fig_img = to_image(fig, format="jpg")
            response = HttpResponse(fig_img, content_type="image/jpeg")
            response["Content-Encoding"] = "UTF-8"
            return response
    else:
        return HttpResponse("Il n'y a pas de groupes dans cette étude !", status=HTTPStatus.NOT_FOUND)

def computeJPGGanttFromEtude(etude):
    return computeGanttFromEtude(etude)
