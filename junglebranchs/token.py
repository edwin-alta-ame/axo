from configs import *
import junglebranchs.dbpg

def ValidateToken(_token,_ip,_time):
	try:
		claro = jwt.decode(_token, token_key, algorithms=["HS256"])
		if( claro["_exp"] > int(time.time()) ):
			return claro
		else:
			d = {}
			d["tipo"] = "tiempo"
			d["_status"] = "INVALID_TOKEN"
			return d
	except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.InvalidSignatureError):
		d = {}
		d["_status"] = "INVALID_TOKEN"
		d["tipo"] = "ExpiredSignatureError,InvalidTokenError,InvalidSignatureError"
		return d

def auth(f):
	@functools.wraps(f)
	def wrapper(*args, **kwargs):
		if "ApiKeyAuth" in request.headers:
			errores = []
			token_validation = ValidateToken(request.headers["ApiKeyAuth"],request.remote_addr,time.time())
			if( token_validation["_status"] == "ok" ):
				rows = junglebranchs.dbpg.selectTable("permisos","*","nombre_permiso='" + str(f.__qualname__) + "'")
				if(len(rows)>0):
					result = rows[0]
					rows = junglebranchs.dbpg.selectTable("roles_permisos","*","rol_id='" + str(token_validation["_rol_id"]) + "' AND permiso_id='" + str(result["id"]) + "'")
					if(len(rows)>0):
						return f(*args, token_data=token_validation, **kwargs)
					else:
						return jsonify(ERROR = "NOT_PERMISSION")
				else:
					return jsonify(ERROR = "NOT_PERMISSION")
			else:
				return jsonify(ERROR = "INVALID_TOKEN")
		else:
			return jsonify(ERROR = "INVALID_TOKEN")
	return wrapper