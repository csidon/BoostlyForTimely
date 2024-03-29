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
from boostly.utils import cleanup
drop_everything()
print("All tables dropped")
db.create_all()
print("New tables added")
from boostly.models import AvailTimes, Client, ClientPref, Company, Event, TempWaitAlert, User, MsgTmpl
av1=AvailTimes(time_unit='Monday')
av2=AvailTimes(time_unit='Tuesday')
av3=AvailTimes(time_unit='Wednesday')
av4=AvailTimes(time_unit='Thursday')
av5=AvailTimes(time_unit='Friday')
av6=AvailTimes(time_unit='Saturday')
av7=AvailTimes(time_unit='Sunday')
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
							part3=" minute ", part4=" appointment slot is now available on ", \
							part5=" starting at ", part6=".", part7="Look forward to seeing you,", 
							part8="Please note that this is a first-come-first-serve notification. Be quick, or someone else might book it first!")

defaultSmsMsg = MsgTmpl(subj1="Waitlist Notification for ", subj2="'s clients",\
							part1="Hi ", part2="I'm contacting everyone on my Waitlist as a ",\
							part3=" minute ", part4=" appointment slot is now available on ", \
							part5=" starting at ", part6=". If you would like to book in please do so via this link: ", \
							part7="Look forward to seeing you,")

db.session.add(defaultEmailMsg)
db.session.add(defaultSmsMsg)
db.session.commit()
print("Default messages have been entered into MsgTmpl table")


# #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
# # Uncomment section to add test data
# #------------------------------------------------------
print(">>>>>> Adding lambda test event  >>>>>")
lambda_event = Event(cal_event_uid="6diiipdhiflt44smpeq9afkkc4" , event_owner="fakerachellette@gmail.com" , status="confirmed" , event_start="2023-05-16 20:15:00" , event_end="2023-05-16 22:15:00" , event_updated="2023-06-25 20:15:00")
db.session.add(lambda_event)
db.session.commit()
print(">>>>>> Lambda event 6diiipdhiflt44smpeq9afkkc4 added ")
print(">>>>>> Adding test data >>>>>")
coy1 = Company(company_name="Rachelle Massage Therapist")
db.session.add(coy1)
lenaCoy = Company(company_name="Lena Walton - Massage Therapist")
db.session.add(lenaCoy)
coy3 = Company(company_name="Evan Tuina")
db.session.add(coy3)
db.session.commit()
print("<<Lena Massage>> and <<Evan Tuina>> has been added to Company table ")
user1 = User(user_first_name="Rachelle", user_last_name="Skywalker", user_email="fakerachellette@gmail.com", user_password="$2b$12$6Lxi6jt8RtxNlggq9ugHlusxuDmbydw084Gl5IfQfcSVjERO6vtLu", timely_booking_url="https://bookings.gettimely.com/rachelleeastwoodmassagetherapist/book", companyid=1)
db.session.add(user1)
user2 = User(user_first_name="Chipper", user_last_name="Mika", user_email="chris.chonghuihui@gmail.com", user_password="$2b$12$6Lxi6jt8RtxNlggq9ugHlusxuDmbydw084Gl5IfQfcSVjERO6vtLu", timely_booking_url="https://bookings.gettimely.com/rachelleeastwoodmassagetherapist/book", companyid=1)
db.session.add(user2)
user3 = User(user_first_name="Evan", user_last_name="Master", user_email="evan@user.com", user_password="$2b$12$6Lxi6jt8RtxNlggq9ugHlusxuDmbydw084Gl5IfQfcSVjERO6vtLu", timely_booking_url="https://bookings.gettimely.com/rachelleeastwoodmassagetherapist/book", companyid=1)
db.session.add(user3)
userLena = User(user_first_name="Lena", user_last_name="Walton", user_email="LenaWalton.MassageTherapist@gmail.com", user_password="$2b$12$6Lxi6jt8RtxNlggq9ugHlusxuDmbydw084Gl5IfQfcSVjERO6vtLu", timely_booking_url="https://bookings.gettimely.com/rachelleeastwoodmassagetherapist/book", companyid=2)
db.session.add(userLena)
userHest = User(user_first_name="Hester", user_last_name="TheTester", user_email="hester.hamilton@gmail.com", user_password="$2b$12$6Lxi6jt8RtxNlggq9ugHlusxuDmbydw084Gl5IfQfcSVjERO6vtLu", timely_booking_url="https://bookings.gettimely.com/rachelleeastwoodmassagetherapist/book", companyid=2)
db.session.add(userHest)
db.session.commit()
print("<<ChipperMika>> and <<Evan Tuina>> has been added to User table ")

print(">>> Adding Client data >>>")
client1 = Client(first_name="Baby", last_name="Yoda", email="yoda@client.com", mobile=220220222, status="active")
client2 = Client(first_name="Richie", last_name="Rich(eha)", email="heartaudionz@gmail.com", mobile=220220222, status="active")
client3 = Client(first_name="Poke", last_name="Man(ecc)", email="chris.chonghuihui+poke@gmail.com", mobile=220220222, status="active")
client4 = Client(first_name="Pikkka", last_name="Achoo", email="achoo@client.com", mobile=220220222, status="active")
client5 = Client(first_name="Pickles", last_name="TheDog", email="pick@client.com", mobile=220220222, status="active")
client6 = Client(first_name="Rachel", last_name="Latte(e)", email="heartaudionz@gmail.com", mobile=220220222, status="active")
client7 = Client(first_name="Lucas", last_name="Moonwalker(e)", email="fakerachellette+lukas@gmail.com", mobile=220220222, status="active")
client8 = Client(first_name="Richie", last_name="Rich", email="richie@rich.com", mobile=220220222, status="active")
client9 = Client(first_name="Poke", last_name="Man(e)", email="chris.chonghuihui+poke@gmail.com", mobile=220220222, status="active")
db.session.add(client1)
db.session.add(client2)
db.session.add(client3)
db.session.add(client4)
db.session.add(client5)
db.session.add(client6)
db.session.add(client7)
db.session.add(client8)
db.session.add(client9)
db.session.commit()
print(">>> Appending 6 clients to company 1 and 3 clients to company userLena>>>")
client1.companies.append(coy1)
client2.companies.append(coy1)
client3.companies.append(coy1)
client4.companies.append(coy1)
client5.companies.append(coy1)
client6.companies.append(lenaCoy)
client7.companies.append(coy1)
client8.companies.append(lenaCoy)
client9.companies.append(lenaCoy)
db.session.commit()
print(">>> Refreshing clients to get their clientID>>>")
db.session.refresh(client1)                                           
client_id_1 = client1.id        	
db.session.refresh(client2)
client_id_2 = client2.id
db.session.refresh(client3)
client_id_3 = client3.id
db.session.refresh(client4)
client_id_4 = client4.id
db.session.refresh(client5)
client_id_5 = client5.id
db.session.refresh(client6)
client_id_6 = client6.id
db.session.refresh(client7)
client_id_7 = client7.id
db.session.refresh(client8)
client_id_8 = client8.id
db.session.refresh(client9)
client_id_9 = client9.id
cp1 = ClientPref(min_duration=25, client_id=client_id_1)
cp2 = ClientPref(min_duration=125, client_id=client_id_2)
cp3 = ClientPref(min_duration=180, client_id=client_id_3)
cp4 = ClientPref(min_duration=15, client_id=client_id_4)
cp5 = ClientPref(min_duration=26, client_id=client_id_5)
cp6 = ClientPref(min_duration=30, client_id=client_id_6)
cp7 = ClientPref(min_duration=45, client_id=client_id_7)
cp8 = ClientPref(min_duration=30, client_id=client_id_8)
cp9 = ClientPref(min_duration=60, client_id=client_id_9)
db.session.add(cp1)
db.session.add(cp2)
db.session.add(cp3)
db.session.add(cp4)
db.session.add(cp5)
db.session.add(cp6)
db.session.add(cp7)
db.session.add(cp8)
db.session.add(cp9)
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
cp7.avtimes.clear()
cp7.avtimes.append(av1)
cp7.avtimes.append(av2)
cp7.avtimes.append(av3)
cp7.avtimes.append(av4)
cp7.avtimes.append(av5)
cp8.avtimes.clear()
cp8.avtimes.append(av6)
cp8.avtimes.append(av7)
cp9.avtimes.clear()
cp9.avtimes.append(av1)
cp9.avtimes.append(av3)
cp9.avtimes.append(av5)
cp9.avtimes.append(av6)
cp9.avtimes.append(av7)
db.session.commit()
print(">>> Client avtimes preferences added!!")
    

print(">>> Adding some 'raw' alerts to TempWaitAlert table >>>")
rawAlert1=TempWaitAlert(slot_start_date_time="2023-05-16 20:15:00", slot_length=45)
rawAlert2 = TempWaitAlert(slot_start_date_time="2023-06-01 11:30:00", slot_length=120)
db.session.add(rawAlert1)
db.session.add(rawAlert2)
db.session.commit()

print("Two random raw alert data pieces added. Remember that raw alerts are not attached to users! The check is on their email address")
cleanup(db.session)
print("db session closed")

print(" Adding Slots synced to Gmail Boostly Alerts... ")
alert3 = TempWaitAlert(id=3, slot_start_date_time="2023-07-12 13:00:00", slot_length=30)
alert4 = TempWaitAlert(id=4, slot_start_date_time="2023-07-06 11:30:00", slot_length=60)
alert5 = TempWaitAlert(id=5, slot_start_date_time="2023-07-08 13:45:00", slot_length=90)
db.session.add(alert3)
db.session.add(alert4)
db.session.add(alert5)
db.session.commit()