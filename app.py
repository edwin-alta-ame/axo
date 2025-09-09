from configs import *

app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello():
	return "API-REST"

from api_files.signup import *
api.add_resource(ApiSignUp, '/api/signup')


from api_files.login import *
api.add_resource(ApiLogin, '/api/login')

from api_files.getuser import *
api.add_resource(ApiGetUser, '/api/getuser')

class pruebaToken(Resource):
	@junglebranchs.token.auth
	def get(self,token_data):
		return "Hola"
api.add_resource(pruebaToken, '/api/tokenprueba')