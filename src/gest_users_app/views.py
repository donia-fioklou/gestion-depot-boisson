from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import Permission

User = get_user_model()


class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        View to get the permissions assigned to the currently authenticated user.

        - Returns:
            Response: A list of permissions with the following fields:
                - `codename`: The codename of the permission.
                - `name`: The name of the permission.
                - `content_type`: The app label of the content type associated with the permission.
        
        - Responses:
            200:
                description: Successfully retrieved user permissions.
                examples:
                    application/json: [
                        {
                            "codename": "add_user",
                            "name": "Can add user",
                            "content_type": "auth"
                        },
                        {
                            "codename": "change_user",
                            "name": "Can change user",
                            "content_type": "auth"
                        }
                    ]
            401:
                description: Unauthorized: Authentication credentials were not provided.
        """

        user = request.user

        # Récupérer les permissions directement attribuées à l'utilisateur
        user_permissions = user.user_permissions.all()

        # Récupérer les permissions des groupes auxquels l'utilisateur appartient
        group_permissions = Permission.objects.filter(group__user=user)

        # Union des deux ensembles de permissions
        all_permissions = user_permissions | group_permissions

        # Formater les données des permissions pour la réponse
        permission_data = [
            {
                "codename": perm.codename,
                "name": perm.name,
                "content_type": perm.content_type.app_label
            }
            for perm in all_permissions
        ]
        
        return Response(permission_data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    operation_description="This view allows the user to change their password by providing the current password and a new password.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'current_password': openapi.Schema(type=openapi.TYPE_STRING, description='Current password'),
            'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password'),
        }
    ),
    responses={
        200: "Password changed successfully",
        400: "Incorrect current password or new password required",
    }
)
@api_view(['POST'])
def change_password(request):
    user = request.user
    current_password = request.data.get("current_password")
    new_password = request.data.get("new_password")

    if not check_password(current_password, user.password):
        return Response({"error": "Mot de passe actuel incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    
    if new_password:
        user.set_password(new_password)
        user.save()
        return Response({"message": "Mot de passe changé avec succès"}, status=status.HTTP_200_OK)
    return Response({"error": "Nouveau mot de passe requis"}, status=status.HTTP_400_BAD_REQUEST)
