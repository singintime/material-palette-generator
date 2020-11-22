import os
from flask import Flask
from flask_restful import Resource, Api
from lib.palette import generatePalette

app = Flask(__name__)
api = Api(app)

settings = app.config.get("RESTFUL_JSON", {})
settings.setdefault("indent", 2)
settings.setdefault("sort_keys", True)
app.config["RESTFUL_JSON"] = settings


class Hex(Resource):
    def get(self, code):
        palette = generatePalette(f"#{code}")
        if not palette:
            return {"error": {"message": "Color not found"}}, 404
        return palette, 200


api.add_resource(Hex, "/<string:code>")

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
