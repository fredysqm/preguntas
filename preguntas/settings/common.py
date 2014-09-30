import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

ROOT_URLCONF = 'preguntas.urls'
WSGI_APPLICATION = 'preguntas.wsgi.application'

LANGUAGE_CODE = 'es-PE'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGIN_URL = '/admin/'

PIPELINE_COMPILERS = (
    'pipeline.compilers.coffee.CoffeeScriptCompiler',
    'pipeline.compilers.less.LessCompiler',
    'pipeline.compilers.stylus.StylusCompiler',
)

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE_CSSMIN_BINARY = 'cssmin'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'

PIPELINE_CSS = {
    'all': {
        'source_filenames': (
            'less/bootstrap.less',
            'stylus/base.styl',
        ),
        'output_filename': 'css/all.css',
    },
}

PIPELINE_JS = {
    'all': {
        'source_filenames': (
            'js/jquery.js',
            'js/bootstrap.js',
        ),
        'output_filename': 'js/all.js',
    },
}