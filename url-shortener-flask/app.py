from flask import Flask,render_template,request,redirect,url_for
import requests
import datetime
import dateutil.parser
import random
import string
import mysql.connector


port = 5100
app = Flask(__name__)

def randomString(stringLength):
    letters = string.ascii_letters
    print(len(letters))
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_random_string():
    conn = mysql.connector.connect(
        host="us-cdbr-east-05.cleardb.net",
        user="b1e337b88487dd",
        passwd="60cfc22a",
        database='heroku_daa746ade202a92'
    )
    cursor = conn.cursor()
    # sql = "INSERT INTO url (longurl, shorturl, expiry) VALUES (%s, %s,%s)"
    # val = ('www.google.com','www.spit.com','2020-06-05 18:34:00')
    # cursor.execute(sql, val)
    cursor.execute("SELECT shorturl FROM url")
    print("url list")
    urls_list=[]
    for i in cursor:
        urls_list.append(i[0])
    print(urls_list)
    while True :
        #generating random string of length 5 itself has 380204032 combinationspossible as target set contains 52 chars.
        n = random.randint(1,5) 
        short_link = randomString(n)
        if short_link in urls_list :
            print("repetition found-----generating new string")
            continue
        else:
            print("unique string generated")
            break
    conn.commit()
    conn.close()
    return short_link

        

@app.route('/',methods=['GET'])
def start():
    return render_template('index.html')


@app.route('/s',methods=['GET','POST'])
def short():
    if request.method=='POST':
        longurl = request.form['longurl']
        custom = get_random_string()
        expiry = request.form['expiry']
        expiry = str(expiry)
        expiry = expiry.replace("T"," ")
        expiry = dateutil.parser.parse(expiry)

        if not longurl and custom and expiry:
            return 'Error <script>alert("Invalid Credentials");</script>'
        if longurl.startswith("http://" or "https://"):
            pass
        else:
            longurl = str("http://"+str(longurl))

        try:
            r = requests.get(longurl)
            if r.status_code == 200:
                pass
            else:
                return 'Invalid URL <script>alert("Invalid URL");</script>'
        except:
            return '''Invalid URL <script>alert("Invalid URL");
            var meta = document.createElement('meta');
		meta.httpEquiv = "REFRESH";
		meta.content = "0;URL=/";
		document.getElementsByTagName('head')[0].appendChild(meta);

            </script>'''

        print(longurl)
        print(custom)
        conn = mysql.connector.connect(
            host="us-cdbr-east-05.cleardb.net",
            user="b1e337b88487dd",
            passwd="60cfc22a",
            database='heroku_daa746ade202a92'
        )
        cursor = conn.cursor()

        try:
            cursor.execute("insert into url (longurl,shorturl,expiry) values (%s,%s,%s);",(longurl,custom,expiry)) 
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
        url = "http://127.0.0.1:"+str(port)+"/s/"+custom

        return 'Live at <a target="_blank" href="'+url+'">'+url+'</a>'
    return ""

@app.route('/s/<custom>',methods=['GET','POST'])
def final(custom):

    conn = mysql.connector.connect(
        host="us-cdbr-east-05.cleardb.net",
        user="b1e337b88487dd",
        passwd="60cfc22a",
        database='heroku_daa746ade202a92'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM url WHERE shorturl=(%s);', (str(custom),))
    print(" custom : " + custom)
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
        #to do redirect to 404 error
        return render_template(url_for("static", filename="404.html"))


if __name__ == '__main__':
    app.run(port=port)
