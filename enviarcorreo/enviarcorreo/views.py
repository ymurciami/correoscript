from django.shortcuts import render
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from .models import Archivo
from .forms import DocumentForm

def home(request):
    form = DocumentForm(request.POST)
    return render(request,'index.html',{'form':form})

def enviarCorreo(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Archivo(name = request.FILES['docfile'])
            newdoc.save()
    else:
        form = DocumentForm() # A empty, unbound form
    ultimo = Archivo.objects.latest('id')
    desglo = str(ultimo.name)
    desglozado = desglo.split('/')
    fromaddr = request.POST["emailemisor"]
    toaddr = request.POST["email"]
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = request.POST["asunto"]
    body = request.POST["mensaje"]
    msg.attach(MIMEText(body, 'plain'))
    filename = desglozado[2]
    attachment = open(str(ultimo.name), "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.starttls()
    server.login(fromaddr, request.POST["clave"])
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    return render(request,'mensajes.html')
    
    
