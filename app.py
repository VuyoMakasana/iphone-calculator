from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session storage


@app.route("/", methods=["GET", "POST"])
def calculator():
    if "expression" not in session:
        session["expression"] = ""

    if request.method == "POST":
        if "num" in request.form:
            # Append number or decimal point
            session["expression"] += request.form["num"]

        elif "operation" in request.form:
            op = request.form["operation"]

            if op == "clear":
                session["expression"] = ""

            elif op == "sign":
                if session["expression"]:
                    if session["expression"].startswith("-"):
                        session["expression"] = session["expression"][1:]
                    else:
                        session["expression"] = "-" + session["expression"]

            elif op == "percent":
                try:
                    session["expression"] = str(eval(session["expression"]) / 100)
                except (ZeroDivisionError, SyntaxError, NameError, TypeError, ValueError):
                    session["expression"] = "Error"

            elif op == "equals":
                try:
                    session["expression"] = str(eval(session["expression"]))
                except (ZeroDivisionError, SyntaxError, NameError, TypeError, ValueError):
                    session["expression"] = "Error"

            else:  # +, -, ×, ÷
                if op == "add":
                    session["expression"] += "+"
                elif op == "subtract":
                    session["expression"] += "-"
                elif op == "multiply":
                    session["expression"] += "*"
                elif op == "divide":
                    session["expression"] += "/"

        session.modified = True
        return redirect(url_for("calculator"))

    return render_template("index.html", result=session["expression"])


if __name__ == "__main__":
    app.run(debug=True)
