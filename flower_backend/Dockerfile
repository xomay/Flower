FROM python
WORKDIR /app

RUN pip install psutil requests kaleido djangorestframework django-rest-passwordreset django-cors-headers docx docxtpl num2words plotly pandas mysqlclient

RUN apt-get update && apt-get -y install locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i fr_FR -c -f UTF-8 -A /usr/share/locale/locale.alias fr_FR.UTF-8
ENV LANG fr_FR.UTF-8

COPY . .
