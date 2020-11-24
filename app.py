from flask import Flask, render_template, abort
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


@app.route("/preview/<string:code>")
def preview(code):
    palette = generatePalette(f"#{code}")
    if not palette:
        abort(404)
    contrast = palette["contrast"]
    del palette["contrast"]
    return render_template(
        "home.html",
        title="Material palette preview",
        code=code,
        palette=palette,
        contrast=contrast,
    )


api.add_resource(Hex, "/<string:code>")

if __name__ == "__main__":
    app.run()
