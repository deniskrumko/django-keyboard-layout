from django.conf import settings
from django.contrib.admin import site
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache


@login_required(login_url='/admin/login/')
@never_cache
def index(request, extra_context=None):
    """Custom index page for Django CMS.

    Hides some apps from non-developer admin users.

    """
    app_list = site.get_app_list(request)

    # Hide some apps is request's user is not a developer
    if not getattr(request.user, 'is_developer', False):
        only_developers_apps = getattr(settings, 'ONLY_DEVELOPERS_APPS', [])

        for app in tuple(app_list):
            if app['name'].lower() in only_developers_apps:
                app_list.remove(app)

    context = dict(
        site.each_context(request),
        title=site.index_title,
        app_list=app_list,
    )
    context.update(extra_context or {})

    request.current_app = site.name

    return TemplateResponse(request, 'admin/index.html', context)
