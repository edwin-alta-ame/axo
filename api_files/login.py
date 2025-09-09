from configs import *

class ApiLogin(Resource):
	def post(self):
		parser.add_argument('email', type=str)
		parser.add_argument('contrasena', type=str)
		args = parser.parse_args()
		email=args["email"]
		contrasena=args["contrasena"].encode('utf-8')
		contrasena=hashlib.sha256(contrasena).hexdigest()
		rows = junglebranchs.dbpg.selectTable("usuarios","id,email,rol_id","email='" + email + "' AND contrasena='" + contrasena + "'")
		d = {}
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
		else:
			d["_error"] = "DATOS_INCORRECTOS" 
			return ( jsonify(d) )