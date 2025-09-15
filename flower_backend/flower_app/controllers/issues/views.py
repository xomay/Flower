from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
import os
import requests
import json

from rest_framework import serializers

GITLAB_TOKEN = os.getenv("API_TOKEN")
PROJECT_ID = os.getenv("PROJECT_ID")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")

from flower_app.controllers.permissions import HasGroupPermission

class IssueSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    labels = serializers.CharField(required=False, allow_blank=True)

class IssueCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'POST': ['ROLE_CA']
    }

    serializer_class = IssueSerializer
    def create(self, request, *args, **kwargs):
        if self.request.method == "POST":
            data = request.data
            title = data.get("title")
            description = data.get("description")
            labels_data = data.get("labels", "")
            labels = ""
            for l in labels_data : labels = labels + l + ","
            print(labels)

            url = f"https://gitlab.insa-rennes.fr/api/v4/projects/{PROJECT_ID}/issues"
            headers = {
                "PRIVATE-TOKEN": GITLAB_TOKEN,
                "Content-Type": "application/json",
            }
            payload = {
                "title": title,
                "description": description,
                "labels": labels[:-1],
            }

            slack_url = f"https://slack.com/api/chat.postMessage"
            slack_headers = {
                "Authorization": "Bearer "+SLACK_TOKEN,
                "Content-Type": "application/json",
            }
            slack_payload = {
                "channel": "si",
                "text": "Nouveau ticket reçu !\nTitre : "+title+"\nDescription : "+description+"\nLabels : "+labels,
            }

            r = requests.post(url, headers=headers, json=payload)

            slack = requests.post(slack_url, headers=slack_headers, json=slack_payload)

            return JsonResponse(r.json(), status=r.status_code)
        return JsonResponse({"error": "Invalid method"}, status=405)
