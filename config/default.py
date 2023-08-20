import os
import sys

# Server config
SERVER_NAME = 'icourse.npuer.life'
DEBUG = False
# DEBUG = True
# SERVER_NAME = 'localhost'

for arg in sys.argv:
  if arg == '-d':
    DEBUG = True

SECRET_KEY = 'course-secret-key'
EMAIL_CONFIRM_SECRET_KEY = 'course-email-confirm-secret-key'
PASSWORD_RESET_SECRET_KEY = 'course-password-reset-secret-key'

# available languages
LANGUAGES = {
  'en': 'English',
  'zh': '中文'
}

# SQL config
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://icourse:guadaxuanke@localhost/icourse?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask mail
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEBUG = DEBUG
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = 'course-review-support@npuer.life'
MAIL_MAX_EMAILS = None
# MAIL_SUPPRESS_SEND =
MAIL_ASCII_ATTACHMENTS = False

# Upload config
UPLOAD_FOLDER = '/var/course-uploads/'
# Alowed extentsions for a filetype
# for example 'image': set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = {
  'image': set(['png', 'jpg', 'jpeg', 'gif', 'webp', 'avif']),
  'file': set(
    '7z|avi|csv|doc|docx|flv|gif|gz|gzip|jpeg|jpg|mov|mp3|mp4|mpc|mpeg|mpg|ods|odt|pdf|png|ppt|pptx|ps|pxd|rar|rtf|tar|tgz|txt|vsd|wav|wma|wmv|xls|xlsx|xml|zip'.split(
      '|')),
}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

IMAGE_PATH = 'uploads/images'

# Debugbar Settings
# Enable the profiler on all requests
DEBUG_TB_PROFILER_ENABLED = True
# Enable the template editor
DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

# URL to return to after signing on
RETURN_URL = "https://icourse.npuer.life/signincallback/"
# URL to Discourse
DISCOURSE_URL = "https://npuer.life"
# replace with your own secret
CALL_DISCOURSE_SSO_SECRET = 'FtwFnoJpYNHemwR3CimF'
assert len(CALL_DISCOURSE_SSO_SECRET) > 20
CALL_DISCOURSE_SSO_SECRET = bytes(CALL_DISCOURSE_SSO_SECRET, 'utf-8')
