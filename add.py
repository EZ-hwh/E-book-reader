import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

                            
with open("/home/harry/Code/Computer_network/The Wonderful Year.txt", "r",encoding='utf-8') as f:
    title = 'The$Wonderful$Year'
    s = f.read()
#print(s)
c.execute("insert into novel(title,words) \
                    values('%s','%s')"%(title,s))
conn.commit()
conn.close()