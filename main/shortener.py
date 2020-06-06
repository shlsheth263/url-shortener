import random
import string
import mysql.connector

def get_random_string():
    letters=string.ascii_letters
    conn = mysql.connector.connect(
    host="us-cdbr-east-05.cleardb.net",
    user="b1e337b88487dd",
    passwd="60cfc22a",
    database='heroku_daa746ade202a92'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT shorturl FROM url")
    print("url list")
    urls_list=[]
    for i in cursor:
        urls_list.append(i[0])
    print(urls_list)
    while True :
        #generating random string of length 5 itself has 380204032 combinationspossible as target set contains 52 chars.
        stringLength = random.randint(1,5) 
        letters = string.ascii_letters
        short_link= ''.join(random.choice(letters) for i in range(stringLength))

        if short_link in urls_list :
            print("repetition found-----generating new string")
            continue
        else:
            print("unique string generated")
            print("unqie : "+ short_link)
            break
    conn.commit()
    conn.close()
    return short_link