from django.http import HttpResponse

import plotly.express as px
from plotly.io import to_html, to_image
import pandas as pd
import io
import base64
from datetime import date, timedelta

import locale
locale.setlocale(locale.LC_TIME, "fr_FR.utf8")

def computeJPGGanttFromEtude(etude):
    data = []
    # TODO: Trier en fonction des indices
    for groupe in etude.groupe_set.iterator():
        print('Groupe : {}'.format(groupe))
        for phase in groupe.phase_set.iterator():
            data.append(dict(Phase=phase.title + " ", Début=phase.beginDate, Fin=phase.finishDate))

    if len(data)>0 :
        df = pd.DataFrame(data)
        fig = px.timeline(df, x_start="Début", x_end="Fin", y="Phase")
        fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
        fig.update_xaxes(tickformat='%d/%m/%y')
        fig_img = to_image(fig, format="jpg")
        return fig_img
    else:
        return HttpResponse()

def computeGanttFromEtude(etude, image_format="jpg"):

    data = []
    # TODO: Trier en fonction des indices
    for groupe in etude.groupe_set.iterator():
        print('Groupe : {}'.format(groupe))
        for phase in groupe.phase_set.iterator():
            data.append(dict(Phase=phase.title + " ", Début=phase.beginDate, Fin=phase.finishDate))

    if len(data)>0 :
        df = pd.DataFrame(data)
        fig = px.timeline(df, x_start="Début", x_end="Fin", y="Phase")
        fig.update_yaxes(autorange="reversed", ticks="outside") # otherwise tasks are listed from the bottom up
        fig.update_xaxes(tickformat='%d/%m/%y')

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
        return HttpResponse()
