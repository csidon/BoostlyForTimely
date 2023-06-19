def drop_everything():
    """(On a live db) drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """
    from sqlalchemy.engine.reflection import Inspector
    from sqlalchemy.schema import DropConstraint, DropTable, MetaData, Table

    con = db.engine.connect()
    trans = con.begin()
    inspector = Inspector.from_engine(db.engine)

    # We need to re-create a minimal metadata with only the required things to
    # successfully emit drop constraints and tables commands for postgres (based
    # on the actual schema of the running instance)
    meta = MetaData()
    tables = []
    all_fkeys = []

    for table_name in inspector.get_table_names():
        fkeys = []

        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey["name"]:
                continue

            fkeys.append(db.ForeignKeyConstraint((), (), name=fkey["name"]))

        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)

    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))

    for table in tables:
        con.execute(DropTable(table))

    trans.commit()




from boostly import db
drop_everything()
print("All tables dropped")
db.create_all()
print("New tables added")
from boostly.models import AvailTimes, Client, ClientCompany, ClientPref, Company, Event, PrefTimes, TempWaitAlert, User, MsgTmpl
av1=AvailTimes(timeUnit='Monday')
av2=AvailTimes(timeUnit='Tuesday')
av3=AvailTimes(timeUnit='Wednesday')
av4=AvailTimes(timeUnit='Thursday')
av5=AvailTimes(timeUnit='Friday')
av6=AvailTimes(timeUnit='Saturday')
av7=AvailTimes(timeUnit='Sunday')
db.session.add(av1)
db.session.add(av2)
db.session.add(av3)
db.session.add(av4)
db.session.add(av5)
db.session.add(av6)
db.session.add(av7)
db.session.commit()
print("AvailTimes table data entered")


defaultEmailMsg = MsgTmpl(subj1="Waitlist Notification for ", subj2="'s clients",\
							part1="Hi ", part2="I'm contacting everyone on my Waitlist as a ",\
							part3=" minute ", part4=" appointment is now available on ", \
							part5=" starting at ", part6=".", part7="Look forward to seeing you,", 
							part8="Please note that this is a first-come-first-serve notification. Be quick, or someone else might book it first!")

defaultSmsMsg = MsgTmpl(subj1="Waitlist Notification for ", subj2="'s clients",\
							part1="Hi ", part2="I'm contacting everyone on my Waitlist as a ",\
							part3=" minute ", part4=" appointment is now available on ", \
							part5=" starting at ", part6=". If you would like to book in please do so via this link: ", \
							part7="Look forward to seeing you,")

db.session.add(defaultEmailMsg)
db.session.add(defaultSmsMsg)
db.session.commit()
print("Default messages have been entered into MsgTmpl table")


# #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
# # Uncomment section to add test data
# #------------------------------------------------------
print(">>>>>> Adding test data >>>>>")
coy1 = Company(companyName="Lena Massage")
db.session.add(coy1)
coy2 = Company(companyName="Evan Tuina")
db.session.add(coy2)
db.session.commit()
print("<<Lena Massage>> and <<Evan Tuina>> has been added to Company table ")
user1 = User(userFirstName="Testy", userLastName="Tester", userEmail="test@test.com", userPassword="$2b$12$6Lxi6jt8RtxNlggq9ugHlusxuDmbydw084Gl5IfQfcSVjERO6vtLu", companyid=1)
db.session.add(user1)
user2 = User(userFirstName="Evan", userLastName="Master", userEmail="evan@user.com", userPassword="$2b$12$6Lxi6jt8RtxNlggq9ugHlusxuDmbydw084Gl5IfQfcSVjERO6vtLu", companyid=1)
db.session.add(user2)
db.session.commit()
print("<<Testy Tester>> and <<Evan Tuina>> has been added to User table ")

print(">>> Adding Client data >>>")
client1 = Client(firstName="Baby", lastName="Yoda", email="yoda@client.com", mobile=220220222)
client2 = Client(firstName="Richie", lastName="Rich", email="richie@rich.com")
client3 = Client(firstName="Poke", lastName="Man", email="poke@man.com")
client4 = Client(firstName="Pikkka", lastName="Achoo", email="achoo@client.com")
client5 = Client(firstName="Pickles", lastName="TheDog", email="pick@client.com")
client6 = Client(firstName="Emailable", lastName="Tester", email="fakerachellette@gmail.com")
db.session.add(client1)
db.session.add(client2)
db.session.add(client3)
db.session.add(client4)
db.session.add(client5)
db.session.add(client6)
db.session.commit()
client1.companies.append(coy1)
client2.companies.append(coy1)
client3.companies.append(coy1)
client4.companies.append(coy1)
client5.companies.append(coy1)
client6.companies.append(coy1)
db.session.commit()
db.session.refresh(client1)                                           
clientID1 = client1.id        # can i successfully get the id?	
db.session.refresh(client2)
clientID2 = client2.id
db.session.refresh(client3)
clientID3 = client3.id
db.session.refresh(client4)
clientID4 = client4.id
db.session.refresh(client5)
clientID5 = client5.id
db.session.refresh(client6)
clientID6 = client6.id
cp1 = ClientPref(minDuration=25, clientid=clientID1)
cp2 = ClientPref(minDuration=125, clientid=clientID2)
cp3 = ClientPref(minDuration=180, clientid=clientID3)
cp4 = ClientPref(minDuration=15, clientid=clientID4)
cp5 = ClientPref(minDuration=26, clientid=clientID5)
cp6 = ClientPref(minDuration=20, clientid=clientID6)
db.session.add(cp1)
db.session.add(cp2)
db.session.add(cp3)
db.session.add(cp4)
db.session.add(cp5)
db.session.add(cp6)
db.session.commit()
print(">>> Client data added with client preferences added")

print(">>> Adding avtime Client preferences >>>")

cp1.avtimes.clear()
cp1.avtimes.append(av1)
cp1.avtimes.append(av3)
cp2.avtimes.clear()
cp2.avtimes.append(av4)
cp2.avtimes.append(av5)
cp2.avtimes.append(av7)
cp3.avtimes.clear()
cp3.avtimes.append(av1)
cp3.avtimes.append(av2)
cp3.avtimes.append(av3)
cp4.avtimes.clear()
cp4.avtimes.append(av2)
cp4.avtimes.append(av3)
cp4.avtimes.append(av4)
cp5.avtimes.clear()
cp5.avtimes.append(av3)
cp5.avtimes.append(av5)
cp5.avtimes.append(av7)
cp6.avtimes.clear()
cp6.avtimes.append(av1)
cp6.avtimes.append(av2)
cp6.avtimes.append(av3)
cp6.avtimes.append(av4)
cp6.avtimes.append(av5)
cp6.avtimes.append(av6)
cp6.avtimes.append(av7)
db.session.commit()
print(">>> Client avtimes preferences added!!")
    


rawAlert1=TempWaitAlert(slotStartDateTime="2023-05-16 20:15:00", slotLength=45)
rawAlert2 = TempWaitAlert(slotStartDateTime="2023-06-01 11:30:00", slotLength=120)
db.session.add(rawAlert1)
db.session.add(rawAlert2)
db.session.commit()
print("Two random raw alert data pieces have been added to TempWaitAlert table ")

