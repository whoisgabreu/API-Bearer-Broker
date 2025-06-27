# from flask import Flask, request, jsonify
# from modules.login_broker import ProjetoBroker

# app = Flask(__name__)

# # LITERALMENTE "gabrielbucetinha123"
# API_KEY = "ccf9d74a30dc58035c50d1d0cb19dd20"

# def require_api_key(func):
#     def wrapper(*args, **kwargs):
#         key = request.headers.get("X-API-KEY")
#         if key != API_KEY:
#             return jsonify(
#                 {"error": "Unauthorized"}
#             ), 401
#         return func(*args, **kwargs)
#     wrapper.__name__ = func.__name__
#     return wrapper


# @app.route("/broker/extrair_bearer", methods=["GET"])
# # @require_api_key
# def extrair_bearer():

#     try:
        
#         bearer = ProjetoBroker().extrair_bearer()

#         return jsonify({
#             "broker_bearer": bearer
#         })
    
#     except Exception as e:

#         return jsonify(
#             {
#                 "erro": f"{e}"
#             }
#         ), 400
    

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)


from flask import Flask, request, jsonify
from modules.login_broker import ProjetoBroker
from threading import Lock

app = Flask(__name__)

API_KEY = "ccf9d74a30dc58035c50d1d0cb19dd20"
selenium_lock = Lock()  # lock global

def require_api_key(func):
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-KEY")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@app.route("/broker/extrair_bearer", methods=["GET"])
@require_api_key
def extrair_bearer():
    with selenium_lock:
        try:
            bearer = ProjetoBroker().extrair_bearer()
            return jsonify({"broker_bearer": bearer})
        except Exception as e:
            return jsonify({"erro": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
