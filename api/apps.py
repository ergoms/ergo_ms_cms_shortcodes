from django.apps import AppConfig


class CmsShortcodesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.cms_shortcodes.api'
    label = 'cms_shortcodes'
    verbose_name = 'Шорткоды CMS'
