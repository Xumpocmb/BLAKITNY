from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from .serializers import (
    RegisterSerializer, LoginSerializer, UserProfileSerializer, ChangePasswordSerializer, 
    ChangeEmailSerializer, UpdateAvatarSerializer, ArchiveUserSerializer
)
from .logic import (
    change_password, change_email, archive_user, 
    restore_user, update_avatar, get_user_profile
)

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'User registered successfully',
            'tokens': tokens,
            'user_id': user.id,
            'email': user.email
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        tokens = get_tokens_for_user(user)

        return Response({
            'message': 'Login successful',
            'tokens': tokens,
            'user_id': user.id,
            'email': user.email
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_view(request):
    serializer = TokenRefreshSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user
    return Response({
        'user_id': user.id,
        'email': user.email
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    Возвращает профиль текущего пользователя.
    
    Args:
        request: HTTP-запрос
        
    Returns:
        Response: JSON-ответ с данными профиля пользователя
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Изменяет пароль текущего пользователя.
    
    Args:
        request: HTTP-запрос с новым паролем
        
    Returns:
        Response: JSON-ответ с результатом операции
    """
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        confirm_new_password = serializer.validated_data['confirm_new_password']
        
        success = change_password(request.user, old_password, new_password, confirm_new_password)
        if success:
            return Response({'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Не удалось изменить пароль'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_email_view(request):
    """
    Изменяет email текущего пользователя.
    
    Args:
        request: HTTP-запрос с новым email
        
    Returns:
        Response: JSON-ответ с результатом операции
    """
    serializer = ChangeEmailSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        new_email = serializer.validated_data['new_email']
        
        success = change_email(request.user, new_email)
        if success:
            return Response({'message': 'Email успешно изменен'}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Не удалось изменить email'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_avatar(request):
    """
    Обновляет аватар текущего пользователя.
    
    Args:
        request: HTTP-запрос с файлом аватара
        
    Returns:
        Response: JSON-ответ с результатом операции
    """
    if 'avatar' not in request.FILES:
        return Response(
            {'error': 'Файл аватара не предоставлен'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    avatar_file = request.FILES['avatar']
    success = update_avatar(request.user, avatar_file)
    
    if success:
        return Response({'message': 'Аватар успешно обновлен'}, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Не удалось обновить аватар'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def archive_account(request):
    """
    Архивирует аккаунт текущего пользователя.
    
    Args:
        request: HTTP-запрос
        
    Returns:
        Response: JSON-ответ с результатом операции
    """
    success = archive_user(request.user)
    
    if success:
        return Response({'message': 'Аккаунт успешно архивирован'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(
            {'error': 'Не удалось архивировать аккаунт'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restore_account(request):
    """
    Восстанавливает аккаунт текущего пользователя из архива.
    
    Args:
        request: HTTP-запрос
        
    Returns:
        Response: JSON-ответ с результатом операции
    """
    success = restore_user(request.user)
    
    if success:
        return Response({'message': 'Аккаунт успешно восстановлен'}, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Не удалось восстановить аккаунт'}, 
            status=status.HTTP_400_BAD_REQUEST
        )