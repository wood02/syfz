# -*- coding: utf-8 -*-
DJOSER = {
    'SEND_ACTIVATION_EMAIL': False,
    'SET_PASSWORD_RETYPE': True,  # 重置密码确认
    'PASSWORD_RESET_CONFIRM_URL': '#/password-reset/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'USER_CREATE_PASSWORD_RETYPE': True,  # 新建用户确认密码
    'LOGOUT_ON_PASSWORD_CHANGE': True,
    'SERIALIZERS': {

        'set_password_retype_no_curr': 'djoser.serializers.PasswordRetypeSerializer',
        'set_password_retype': 'djoser.serializers.SetPasswordRetypeSerializer',
        'user_create': 'apps.user.serializer.user_ser.UserCreateSerializer',
        'user_create_password_retype': 'apps.user.serializer.user_ser.UserCreatePasswordRetypeSerializer',
        'user': 'apps.user.serializer.user_ser.UserSerializer',
        'current_user': 'apps.user.serializer.user_ser.UserSerializer',
        'list': 'apps.user.serializer.user_ser.UserSerializer',

        'messages': 'apps.user.djoser_constants.CustomMessages',
    },
    'PERMISSIONS': {
        'set_password': ['rest_framework.permissions.IsAdminUser'],
        'set_me_password': ['djoser.permissions.CurrentUserOrAdmin'],
        'user_create': ['rest_framework.permissions.IsAdminUser'],
        'user_delete': ['rest_framework.permissions.IsAdminUser'],
        'user': ['djoser.permissions.CurrentUserOrAdmin'],
        'user_list': ['rest_framework.permissions.IsAdminUser'],

    }
}
