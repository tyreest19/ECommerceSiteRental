class Config(object):
    """
    Common configurations
    """
    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sql9210979:jCRXP47R66@sql9.freemysqlhosting.net/sql9210979'
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'tyreeostevenson@gmail.com'
    MAIL_PASSWORD = 'xsbmuourppfhnkfc'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # Put any configurations here that are common across all environments

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
