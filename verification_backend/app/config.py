class DefaultConfig(object):
    SECRET_UUID_ID = "45fdbacd-8b08-4fa7-b801-7c1f84d7fe28" 
    SECRET_UUID_VALUE = "ea8e7c0c-0fb8-468c-94af-dda7007bc879"


def init_app(app):
    app.config.from_object("app.config.DefaultConfig")
    # app.config.from_envvar("CONFIG_PATH")
