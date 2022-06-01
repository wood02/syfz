# session配置

SESSION_COOKIE_AGE = 60 * 60 * 12  # 12小时过期

SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 是否关闭浏览器使得Session过期（默认）
SESSION_COOKIE_HTTPONLY = True