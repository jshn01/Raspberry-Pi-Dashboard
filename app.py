from flask import Flask, jsonify, render_template
import psutil
import os
# Variables 



app = Flask(__name__)

def get_cpu_temp():
    try:
        temp = os.popen("vcgencmd measure_temp").readline()
        return f"{float(temp.replace("temp=", "").replace("'C\n",""))} °C"
    except:
        return None

@app.route("/api")
def api():
    ram = psutil.virtual_memory()

    ramPercentage = psutil.virtual_memory().percent

    data = {
        "cpu_usage": f"{psutil.cpu_percent(interval=0.1)} % ",
        "cpu_temp": get_cpu_temp(),
        "cpu_freq": psutil.cpu_freq().current,
        "ram_used": round(ram.used / 1024 / 1024, 2),
        "ram_total": round(ram.total / 1024 / 1024, 2),
        "ram_str": f"{round(ram.used / 1024 / 1024, 2)} / {round(ram.total / 1024 / 1024, 2)} MB",
        "ram_percentage": f"{ramPercentage} %"
    }
    return jsonify(data)

@app.route("/shutdown", methods=["POST"])
def shutdown():
    os.system("sudo shutdown -h now")
    return jsonify({"status": "ok"})

@app.route("/reboot", methods=["POST"])
def reboot():
    os.system("sudo shutdown -r now")
    return jsonify({"status": "ok"})

@app.route("/OpenRetroPi", methods=["POST"])
def openRetroPi():
    os.system("sudo DISPLAY=:0 emulationstation &")
    return jsonify({"status": "ok"})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
