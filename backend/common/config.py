class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///common/data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'umasenhamuitosegura'
    JWT_ACCESS_TOKEN_EXPIRES = False