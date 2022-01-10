
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
# from flask_session.__init__ import Session
from datetime import datetime
# from decouple import config
from github import Github, InputGitAuthor
import os
import csv
import subprocess
# import time
import requests

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

todos = []

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))

def get_userdata(ip_address):
    try:
        response = requests.get("http://ip-api.com/json/{}".format(ip_address))
        js = response.json()
        country = js['country']
        region = js['regionName']
        latitud = js['lat']
        longitud = js['lon']
        return country, region, latitud, longitud
    except Exception as e:
        return "Unknown", "Unknown","Unknown","Unknown"

@app.route("/")
def index():

    if "todos" not in session:
        session["todos"] = []

    fecha = datetime.now()    
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_address = request.environ['REMOTE_ADDR']
    else:
        ip_address = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    country, region, latitud, longitud = get_userdata(ip_address)

    if country == "Peru" or country == "Chile":
        """Show presentacion principal"""
        print ("token index")
        token = os.getenv('GITHUB_TOKEN')
        file_path = "count.txt"
        g = Github(token)
        repo = g.get_repo("cespivilla/cambioestado")
        file = repo.get_contents(file_path, ref="main")  # Get file from branch
        data = file.decoded_content.decode("utf-8")  # Get raw string data
        count = int(data) + 1
        data = str(count)  # Modify/Create file

        def push(path, message, content, branch, update=False):
            author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
            source = repo.get_branch("main")
            contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
            repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
        # Add, commit and push branch
        push(file_path, "Updating counter.", data, "main", update=True)

        mensaje = '{}, {}, {}, {}, {}, {}\n'.format(fecha, ip_address, country, region, latitud, longitud)

        file_path = "visitas.txt"
        file = repo.get_contents(file_path, ref="main")  # Get file from branch
        data = file.decoded_content.decode("utf-8")  # Get raw string data
        data += mensaje  # Modify/Create file

        def push(path, message, content, branch, update=False):
            author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
            source = repo.get_branch("main")
            contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
            repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
        # Add, commit and push branch
        push(file_path, "Updating visits global", data, "main", update=True)  

    return render_template("index.html")

@app.route("/cameco", methods=["GET", "POST"])
def cameco():
    session["todos"] = []

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Validate submission
        seccion = request.form.get("seccion")
        if not seccion or float(seccion) < 50.0 or float(seccion) > 5000.0:
                return render_template("error.html", message="No se ha indicado la sección o está fuera de rango")
        session["todos"].append(seccion)        

        diam = request.form.get("diam")
        if not diam or float(diam) < 8.0 or float(diam) > 50.0:
                return render_template("error.html", message="No se ha indicado el diámetro o está fuera de rango")
        session["todos"].append(diam)  

        masa = request.form.get("masa")
        if not masa or float(masa) < 0.1 or float(masa) > 4.0:
                return render_template("error.html", message="No se ha indicado la masa longitudinal o está fuera de rango")
        session["todos"].append(masa)  

        young = request.form.get("young")
        if not young or float(young) < 5000.0 or float(young) > 21000.0:
                return render_template("error.html", message="No se ha indicado el módulo de elasticidad o está fuera de rango")
        session["todos"].append(young)  

        # t1 = time.time()

        dilat= request.form.get("dilat")
        session["todos"].append(dilat)  
        tempini = request.form.get("tempini")
        session["todos"].append(tempini)  
        esfini = request.form.get("esfini")
        session["todos"].append(esfini)  
        tempfin = request.form.get("tempfin")
        session["todos"].append(tempfin)  
        pv = request.form.get("pv")
        session["todos"].append(pv)  
        eh = request.form.get("eh")
        session["todos"].append(eh)  
        dha = request.form.get("dha")
        session["todos"].append(dha)  
        denshie = request.form.get("denshie")
        session["todos"].append(denshie)  

        # Opens a file for writing, creates the file if it does not exist
        file = open("cameco.csv", "w")
        writer = csv.writer(file)
        # writer.writerow((seccion, diam, masa, rotura, young, dilat, tempini, esfini, tempfin, pv, eh, dha, denshie))
        writer.writerow(session["todos"])
        print ("session[todos] ", session["todos"])
        file.close()

        # t2 = time.time()

        subprocess.call("cameco.exe")

        # t3 = time.time()

        file = open("cameco.out", "r")
        mylist = list(file)
  
        # t4 = time.time()

        # print ("t2-t1, t3-t2, t4-t3  ", t2-t1, t3-t2, t4-t3)

        return render_template("camecout.html", result=mylist)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("cameco.html")

@app.route("/unispan", methods=["GET", "POST"])
def unispan():
    session["todos"] = []
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Validate submission
        sec = request.form.get("sec")
        if not sec or float(sec) < 50.0 or float(sec) > 5000.0:
                return render_template("error.html", message="No se ha indicado la sección o está fuera de rango")
        session["todos"].append(sec)        

        fi = request.form.get("fi")
        if not fi or float(fi) < 8.0 or float(fi) > 50.0:
                return render_template("error.html", message="No se ha indicado el diámetro o está fuera de rango")
        session["todos"].append(fi)  

        mass = request.form.get("mass")
        if not mass or float(mass) < 0.1 or float(mass) > 4.0:
                return render_template("error.html", message="No se ha indicado la masa longitudinal o está fuera de rango")
        session["todos"].append(mass)  

        # t1 = time.time()

        mod = request.form.get("mod")
        session["todos"].append(mod)  
        alfa= request.form.get("alfa")
        session["todos"].append(alfa)  
        temp0 = request.form.get("temp0")
        session["todos"].append(temp0)  
        param0 = request.form.get("param0")
        session["todos"].append(param0)  
        tempf = request.form.get("tempf")
        session["todos"].append(tempf)  
        wp = request.form.get("wp")
        session["todos"].append(wp)  
        ice = request.form.get("ice")
        session["todos"].append(ice)  
        pehie = request.form.get("pehie")
        session["todos"].append(pehie) 
        pg1 = request.form.get("pg1")
        session["todos"].append(pg1)
        cot1 = request.form.get("cot1")
        session["todos"].append(cot1) 
        pg2 = request.form.get("pg2")
        session["todos"].append(pg2) 
        cot2 = request.form.get("cot2")
        session["todos"].append(cot2) 
        lcad = request.form.get("lcad")
        session["todos"].append(lcad) 
        pcad = request.form.get("pcad")
        session["todos"].append(pcad) 
        nsub = request.form.get("nsub")
        session["todos"].append(nsub)  


        file = open("unispan.csv", "w")
        writer = csv.writer(file)
        # writer.writerow((sec, fi, mass, mod, alfa, temp0, param0, tempf, wp, ice, pehie, pg1, cot1, pg2, cot2, lcad, pcad, nsub))
        writer.writerow(session["todos"])
        file.close()

        # t2 = time.time()

        subprocess.call("unispan.exe")

        # t3 = time.time()

        file = open("unispan.out", "r")
        unilist = list(file)
  
        # t4 = time.time()

        # print ("t2-t1, t3-t2, t4-t3  ", t2-t1, t3-t2, t4-t3)

        return render_template("unispanout.html", result2=unilist)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("unispan.html")


@app.route("/changespan", methods=["GET", "POST"])
def changespan():
    session["todos"] = []
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Validate submission
        param = request.form.get("param")
        if not param or float(param) < 500.0 or float(param) > 2000.0:
                return render_template("error.html", message="No se ha indicado el parámetro o está fuera de rango")
        session["todos"].append(param)  
        print("tipo session: ", type(session["todos"]))

        delta = request.form.get("delta")
        if not delta or float(delta) < -1.0 or float(delta) > 2.0:
                return render_template("error.html", message="No se ha indicado el desplazamiento o está fuera de rango")
        session["todos"].append(delta)  

        token = os.getenv('GITHUB_TOKEN')
        file_path = "changespan.dat"
        g = Github(token)
        repo = g.get_repo("cespivilla/cambioestado")
        data = session["todos"]
        def push(path, message, content, branch, update=False):
            author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
            source = repo.get_branch("main")
            contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
            repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
        # Add, commit and push branch
        push(file_path, "Updating changespan.dat", data, "main", update=True)
        
        subprocess.call("/changespan.exe")

        file = open("/changespan.out", "r")
        unilist = list(file)
  
        return render_template("changespanout.html", result3=unilist)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changespan.html")




@app.route("/rotura")
def rotura():
        return render_template("rotura.html")

@app.route("/oscila")
def oscila():
        return render_template("oscila.html")

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    """datos de contacto"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        name = request.form.get("name")
        # Ensure username was submitted
        if not request.form.get("name"):
                return render_template("error.html", message="No se ha indicado nombre")

        apellidos = request.form.get("apellidos")
        # Ensure surnames were submitted
        if not request.form.get("apellidos"):
                return render_template("error.html", message="No se ha indicado los apellidos")

        correo = request.form.get("correo")
        # Ensure email was submitted
        if not request.form.get("correo"):
                return render_template("error.html", message="No se ha indicado correo electrónico")

        telefono = request.form.get("telefono")
        comentario = request.form.get("comentario")
        print ("name", name, type(name))
        print ("apellidos", apellidos, type(apellidos))
        print ("comentario", comentario, type(comentario))
        fecha = datetime.now()
        
        mensaje = '\n{}\n{}\n{}\n{}\n{}\n{}\n**'.format(name, apellidos, telefono, correo, comentario, fecha)
        print (" mensaje  ", mensaje)
        token = os.getenv('GITHUB_TOKEN')
        file_path = "contactos.txt"
        g = Github(token)
        repo = g.get_repo("cespivilla/cambioestado")
        file = repo.get_contents(file_path, ref="main")  # Get file from branch
        data = file.decoded_content.decode("utf-8")  # Get raw string data
        data += mensaje  # Modify/Create file

        def push(path, message, content, branch, update=False):
            author = InputGitAuthor("cespivilla","cespivilla@gmail.com")
            source = repo.get_branch("main")
            contents = repo.get_contents(path, ref=branch)  # Retrieve old file to get its SHA and path
            repo.update_file(contents.path, message, content, contents.sha, branch=branch, author=author) 
        # Add, commit and push branch
        push(file_path, "Updating contacts.", data, "main", update=True)    
        
        # Remain in actual page so user can verifiy the sending of data
        return ("", 204)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("contacto.html")
