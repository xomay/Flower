from django.http import HttpResponse
from http import HTTPStatus
import plotly.express as px
from plotly.io import to_image
import pandas as pd
import textwrap
from datetime import datetime

import locale
locale.setlocale(locale.LC_TIME, "fr_FR.utf8")

def computeGanttFromEtudeRaw(etude):
    data = []
    for phase in etude.phases.order_by('index').iterator():
        data.append(dict(Phase="<br>".join(textwrap.wrap(phase.title, width=(datetime.fromisoformat(phase.finishDate).date()-phase.beginDate).days)), Début=phase.beginDate, Fin=phase.finishDate))
    if len(data) > 0 :
        df = pd.DataFrame(data)
        fig = px.timeline(df, x_start="Début", x_end="Fin", y="Phase", color="Phase", text="Phase")
        fig.update_yaxes(showticklabels=False)
        fig.update_xaxes(tickformat='%d/%m/%y')
        fig.update_layout(showlegend=False)
        fig.update_traces(textposition='inside', insidetextanchor='middle', textfont=dict(color='white', size=15))
        return True, fig
    return False, None

def computeGanttFromEtude(etude, image_format="jpg"):
    success,fig = computeGanttFromEtudeRaw(etude)
    if success :
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
        return HttpResponse("Il n'y a pas de phases dans cette étude !", status=HTTPStatus.NO_CONTENT)

def computeJPGGanttFromEtude(etude, image_format="jpg"):
    return computeGanttFromEtude(etude, image_format)
