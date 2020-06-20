import sqlite3
import pickle

conn=sqlite3.connect('REPORTS.db')

print('ddatabase created successfully')

'''cursor=conn.execute(\'''create table REPORTS
                    (SR int primary key not null,
                    Name text not null,
                    Crime_Tag text not null,
                    Date text not null,
                    Address text not null,
                    Contact text not null,
                    Description text not null,
                    Crime_Spot text not null);\''')

print('table created')


conn.execute(\'''insert into REPORTS (SR,Name,Crime_Tag,Date,Address,Contact,Description,Crime_Spot)\
values(1,'Hariram','Molestation','2020/1/10','near pratag nagar','abc@gmail.com','I was passing from my street last day\
 and I saw there were three boys who were trying to molest a girl. That girl was probably returning back to home.\
 I tried to stop them but they had weapons. I hope you will look into this matter and take an action as soon as \
possible.','near megha street')\''')'''

conn.commit()                  
cursor = conn.execute('select * from REPORTS;')
for row in cursor:
    for e in row:
        print(e)

conn.close()






'''import pickle

with open('reports.bin','wb') as file:
    pickle.dump(2,file)'''
