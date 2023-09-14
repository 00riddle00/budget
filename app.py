from flask import Flask, request, render_template
import budget


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    budget_app = budget.Budget()
    app.run(debug=True, port=8000)

