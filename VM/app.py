from flask import Flask, render_template
import base64
from io import BytesIO
from matplotlib.figure import Figure
from get_ultrasonic_data import get_distance_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/distance")
def skraldespand():
    distance_data = get_distance()
    return render_template("distance.html", distance=distance_data)

def get_distance():
    datetimes, distances = get_distance_data(20)
    
    # Generate figure without pyplot
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis="x", which="both", rotation=30)
    ax.set_facecolor("#fff")

    ax.plot(datetimes, distances, linestyle="dashed", c="orange", linewidth="1.7", marker="D", mec="green", ms=7)
    ax.set_xlabel("Tidspunkt")
    ax.set_ylabel("Distance")
    fig.patch.set_facecolor("#fff")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="green")
    ax.spines["left"].set_color("orange")
    ax.spines["right"].set_color("orange")
    ax.spines["top"].set_color("black")
    ax.spines["bottom"].set_color("black")

    # Save to a temporary buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return data 

app.run(debug=True, host="0.0.0.0")
