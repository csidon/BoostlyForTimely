from boostly import db
db.drop_all()
print("All tables dropped")
db.create_all()
print("New tables added")
from boostly.models import AvailTimes, Client, ClientCompany, ClientPref, Company, Event, PrefTimes, TempWaitAlert, User
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

# To add test data
# coy1 = Company(companyName="Lena Massage")
# db.session.add(coy1)
# db.session.commit()
# user1 = User(userFirstName="Testy", userLastName="Tester", userEmail="test@test.com", userPassword="$2b$12$6Lxi6jt8RtxNlggq9ugHlusxuDmbydw084Gl5IfQfcSVjERO6vtLu", companyid=1)
# db.session.add(user1)
# db.session.commit()
