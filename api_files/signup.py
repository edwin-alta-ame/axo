from configs import *
import junglebranchs.token

class ApiSignUp(Resource):
	@junglebranchs.token.auth
	def post(self, token_data):
		parser.add_argument('nombre', type=str)
		parser.add_argument('email', type=str)
		parser.add_argument('rol_id', type=str)
		parser.add_argument('contrasena', type=str)
		args = parser.parse_args()

		nombre = args["nombre"]
		email = args["email"]
		rol_id = args["rol_id"]
		contrasena=args["contrasena"].encode('utf-8')
		contrasena=hashlib.sha256(contrasena).hexdigest()
		d = {}

		rows = junglebranchs.dbpg.selectTable("usuarios","id, email","email='" + email + "'")
		if(len(rows)>0):
			d["_error"] = "USUARIO_EMAIL_EXISTE"
			return jsonify(d)
		data = {"nombre": nombre,"email": email,"rol_id": rol_id,"contrasena": contrasena}
		salida = junglebranchs.dbpg.insertTable("usuarios",data)
		rows = junglebranchs.dbpg.selectTable("usuarios","id,email,rol_id","email='" + email + "'")
		if(len(rows)>0):
			result = rows[0]
			d["_status"] = "ok"
			d["_id"] = result["id"]
			d["_email"] = result["email"]
			d["_rol_id"] = result["rol_id"]
			d["_ip"] = request.remote_addr
			d["_exp"] = ( int( time.time() ) + 86400 )
			token = jwt.encode(d, token_key, algorithm='HS256')
			return ( jsonify( TOKEN = token ) )