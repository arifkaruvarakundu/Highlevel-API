from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .config import *
import requests
from .serializer import *
import random
from django.views.decorators.csrf import csrf_exempt

class InitiateAuthView(APIView):

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        options = {
            'responseType': 'code',
            'redirectUri': 'http://127.0.0.1/',
            'clientId': HIGHLEVEL_CLIENT_ID,
            'scopes': [
                'contacts.readonly',
                'contacts.write',
                'locations/customFields.readonly'
            ]
        }

        auth_url = (
            f"{base_url}/oauth/chooselocation?"
            f"response_type={options['responseType']}&"
            f"redirect_uri={options['redirectUri']}&"
            f"client_id={options['clientId']}&"
            f"scope={' '.join(options['scopes'])}"
        )

        print("authentication_URL:", auth_url)

        return HttpResponseRedirect(auth_url)


class UpdateCustomFieldView(APIView):
    authentication_classes = []  # Add your authentication classes here if needed
    permission_classes = []  # Add your permission classes here if needed

    def get(self, request):


        access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoQ2xhc3MiOiJMb2NhdGlvbiIsImF1dGhDbGFzc0lkIjoiazFGMzh6M0EwZWZSTUhlVmtrM3YiLCJzb3VyY2UiOiJJTlRFR1JBVElPTiIsInNvdXJjZUlkIjoiNjVjMGE5YTQyNzdiMjk2MTMyMmM1NDVhLWxzOHE5MzRkIiwiY2hhbm5lbCI6Ik9BVVRIIiwicHJpbWFyeUF1dGhDbGFzc0lkIjoiazFGMzh6M0EwZWZSTUhlVmtrM3YiLCJvYXV0aE1ldGEiOnsic2NvcGVzIjpbImNvbnRhY3RzLnJlYWRvbmx5IiwiY29udGFjdHMud3JpdGUiLCJsb2NhdGlvbnMvY3VzdG9tRmllbGRzLnJlYWRvbmx5Il0sImNsaWVudCI6IjY1YzBhOWE0Mjc3YjI5NjEzMjJjNTQ1YSIsImNsaWVudEtleSI6IjY1YzBhOWE0Mjc3YjI5NjEzMjJjNTQ1YS1sczhxOTM0ZCJ9LCJpYXQiOjE3MDc4MDYyMjAuMjY0LCJleHAiOjE3MDc4OTI2MjAuMjY0fQ.UT9qOsACNHhTsCwBBpArADXTVmxJE8X4lDSEDHuoh3c'

        # Step 1: Find random contact ID
        contacts_url = f"{HIGHLEVEL_API_BASE_URL}/contacts/?locationId=k1F38z3A0efRMHeVkk3v"
        headers = {"Authorization": f"Bearer {access_token}", "Version": "2021-07-28", "Accept": "application/json"}
        contacts_response = requests.get(contacts_url, headers=headers)
        contacts_data = contacts_response.json().get("contacts")
        random_contact = random.choice(contacts_data)
        random_contact_id = random_contact.get("id")
        print("Selected Random Contact ID:", random_contact_id)
        
        # Step 2: Find custom field ID
        custom_field_id = None
        custom_field_name = "DFS Booking Zoom Link"

        custom_fields_url = f"{HIGHLEVEL_API_BASE_URL}/locations/k1F38z3A0efRMHeVkk3v/customFields"
        headers = {"Authorization": f"Bearer {access_token}", "Version": "2021-07-28", "Accept": "application/json"}
        custom_fields_response = requests.get(custom_fields_url,headers=headers)
        custom_fields_data = custom_fields_response.json().get("customFields")
        
        # Iterate through custom fields to find the matching custom field
        for custom_field in custom_fields_data:
            if custom_field.get("name") == custom_field_name:
                custom_field_id = custom_field.get("id")
                print("custom_field_id",)
                break
        
        # Step 3: Update custom field
        if custom_field_id:
            update_url = f"{HIGHLEVEL_API_BASE_URL}/contacts/{random_contact_id}"

        update_data = {
            "customFields": [
            {"id": custom_field_id, "value": "TEST"}
            ]
        }

        update_response = requests.put(update_url, json=update_data, headers=headers)

        if update_response.status_code == 200:
            serializer = UpdateCustomFieldSerializer({"status": "success"})
            return Response(serializer.data)
        else:
            serializer = UpdateCustomFieldSerializer({"status": "error"})
            return Response(serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
