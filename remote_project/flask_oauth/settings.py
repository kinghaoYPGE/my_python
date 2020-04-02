class MongoConfig(object):
    """
    MongoDB连接参数
    """
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_DBNAME = 'github_cafe'
    MONGO_URI = 'mongodb://{0}:{1}/{2}'.format(MONGO_HOST, MONGO_PORT, MONGO_DBNAME)


class GitHubConfig(object):
    """
    github授权参数
    """
    client_id = '2735358e7e966bdb0f3d'
    client_secret = '0d7f99e734a47337ccd55d90b05e52f5ea2132d6'
    authorization_base_url = 'https://github.com/login/oauth/authorize'
    token_url = 'https://github.com/login/oauth/access_token'
    user_url = 'https://api.github.com/user'
