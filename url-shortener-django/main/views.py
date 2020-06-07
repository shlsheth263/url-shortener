from django.shortcuts import render,redirect
from .models import short_urls
from .forms import UrlForm
import mysql.connector
from .shortener import get_random_string
import datetime
import dateutil.parser
from django.views.generic import TemplateView 
from django.http import Http404  


def Home(request, token):
    conn = mysql.connector.connect(
            host="us-cdbr-east-05.cleardb.net",
            user="b1e337b88487dd",
            passwd="60cfc22a",
            database='heroku_daa746ade202a92'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM url WHERE shorturl=(%s);', (str(token),))
    print(" custom : " + token)
    for row in cursor.fetchall():
        return_this= row[0]
        d=row[2]
        expiry = dateutil.parser.parse(d)
    print("url : "+str(return_this))
    now= datetime.datetime.now()
    print("now = "+ str(now))
    print("expiry : "+ str(expiry))
    if now <= expiry :
        print("In IF")
        print(return_this)
        return redirect(return_this,code=302)
    else :
        print("In ELSE")
        raise Http404  
        return render(request,'404.html')  


def Make(request):
    form = UrlForm(request.POST)
    short_url=''
    if request.method == 'POST':
        if form.is_valid():
            conn = mysql.connector.connect(
                    host="us-cdbr-east-05.cleardb.net",
                    user="b1e337b88487dd",
                    passwd="60cfc22a",
                    database='heroku_daa746ade202a92'
            )
            cursor = conn.cursor()
            NewUrl= form.save(commit=False)
            short_url= get_random_string()
            NewUrl.short_url=short_url
            long_url=form.data['long_url']
            expiry=form.data['expiry']
            print(long_url)
            print(short_url)
            print(expiry)
            try:
                cursor.execute("insert into url (longurl,shorturl,expiry) values (%s,%s,%s);",(long_url,short_url,expiry)) 
            except:
                print(Exception.with_traceback)
                return '''Invalid/Already existing custom url <script>alert("Invalid/Already existing custom url");
                var meta = document.createElement('meta');
            meta.httpEquiv = "REFRESH";
            meta.content = "0;URL=/";
            document.getElementsByTagName('head')[0].appendChild(meta);

                </script>'''
            conn.commit()
            conn.close()
            NewUrl.save()
        else:
            form=UrlForm()
            short_url="Invalid URL"

    return render(request,'home.html',{'form': form,'short_url':short_url})