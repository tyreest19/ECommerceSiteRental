class Config(object):
    """
    Common configurations
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sql9210979:jCRXP47R66@sql9.freemysqlhosting.net/sql9210979'
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
