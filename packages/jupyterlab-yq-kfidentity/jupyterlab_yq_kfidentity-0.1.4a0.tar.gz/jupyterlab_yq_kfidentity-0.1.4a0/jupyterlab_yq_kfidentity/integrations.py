import requests
import xmltodict
import json

from jupyter_server.base.handlers import APIHandler
from tornado.log import app_log
from jupyter_server.utils import url_path_join



def get_jwt():
    filename = 'jwt.txt'
    try:
        with open(filename, 'r') as jwt:
            return jwt.read()
    except:
        app_log.error('Failed to read a JWT.')
        return None
        

class YqKfIdentity(APIHandler):
    def get(self):
        #data = self.get_json_body()
        headers = self.request.headers
        if "userid-token" in headers:
            filename = 'jwt.txt'
            with open(filename, 'w') as out:
                out.write(headers["userid-token"])
        else:
            app_log.warn('There is no JWT token in the headers')
            self.set_status(500)
        self.finish(f"JWT Found: {headers['userid-token']}")


class YqMinioIntegration(APIHandler):
    def get(self):
        jwt = get_jwt()
        if jwt is not None:
            params = (
                ('Action', 'AssumeRoleWithWebIdentity'),
                ('DurationSeconds', '3600'),
                ('Version', '2011-06-15'),
                ('WebIdentityToken', jwt),
            )

            response = requests.post('http://yq-storage-viewer.yq:9000/', params=params)
            if response.status_code == 200:
                sts_cred = json.dumps(xmltodict.parse(response.body))
                app_log.info(sts_cred)
                self.finish(f"Minio credentials: {sts_cred}")
            else:
                app_log.error('Failed to create STS credentials in Minio.')
    

def setup_handlers(web_app):
    """
    Setups all of the YQ ID integrations.
    Every handler is defined here to be integrated with JWT.
    """
    host_pattern = ".*"

    # add the baseurl to our paths
    base_url = web_app.settings["base_url"]
    handlers = [
        (url_path_join(base_url, "yqid", "sync"), YqKfIdentity),
        (url_path_join(base_url, "yqid", "minio"), YqMinioIntegration),
    ]

    
    web_app.add_handlers(host_pattern, handlers)