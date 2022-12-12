from flask import Flask, request
app = Flask(__name__)
#curl -X POST -d 'direction=in&truck=t1&containers=['c-1', 'c2', 'c3']&weight=200&unit=kg&force=something&produce=apples' http://localhost:5000/weight
#curl -X POST -d 'container=123&blabla=abc' http://localhost:5000/weight
@app.route("/weight", methods=["POST"])
def weightpost():
    if request.method == "POST":
        dirction = request.form.get("direction")
        truck = request.form.get("truck")
        containers = request.form.get("containers")
        weight = request.form.get("weight")
        unit = request.form.get("unit")
        force = request.form.get("force")
        produce = request.form.get("produce")

        data = {
        'direction': dirction, 
        'truck': truck, 
        'containers': containers, 
        'weight': weight, 
        'unit': unit, 
        'force': force, 
        'produce': produce}

        return data

@app.route("/weight", methods=["GET"])
def weightget():
    return "dict(data)"

@app.route("/health")
def health():
    return "OK\n"


if __name__ == "__main__":
    app.run()