from configs import *
import junglebranchs.token

class ApiGetUser(Resource):
	@junglebranchs.token.auth
	def get(self, token_data):
		parser.add_argument('value', type=str)
		args = parser.parse_args()
		value = args["value"]
		rows = junglebranchs.dbpg.selectTable("usuarios","id, email","nombre='" + value + "' OR email='" + value + "'")
		if(len(rows)>0):
			return rows[0]
		else:
			return jsonify(ERROR = "NOT_FOUND")