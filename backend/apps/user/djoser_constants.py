from django.utils.translation import gettext_lazy as _


class Messages(object):
    INVALID_CREDENTIALS_ERROR = _("无法使用提供的凭据登录。")
    INACTIVE_ACCOUNT_ERROR = _("用户帐户已禁用。")
    INVALID_TOKEN_ERROR = _("给定用户的令牌无效。")
    INVALID_UID_ERROR = _("无效的用户id或用户不存在。")
    STALE_TOKEN_ERROR = _("给定用户的陈旧令牌")
    PASSWORD_MISMATCH_ERROR = _("两个密码字段不匹配。")
    USERNAME_MISMATCH_ERROR = _("两个 {0} 字段不匹配。")
    INVALID_PASSWORD_ERROR = _("密码无效。")
    EMAIL_NOT_FOUND = _("具有给定电子邮件的用户不存在。")
    CANNOT_CREATE_USER_ERROR = _("无法创建帐户。")
