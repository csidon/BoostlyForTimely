import boto3
from botocore.exceptions import ClientError
from boostly import db
from boostly.utils import cleanup
from boostly.models import TempWaitAlert, MsgTmpl, Client, SentWaitAlert
from datetime import datetime


# To send in: company_name =  current_user.coyowner.company_name
def sendEmail(alertid, company_name, client_id, currentuser):
    print("currentuser is " + str(currentuser) + " with datatype " + str(type(currentuser)))
    alertid = int(alertid)
    client_id=int(client_id)
    msg = MsgTmpl.query.get(1)      # Hardcoding to a single message template for the MVP
    alert = TempWaitAlert.query.get_or_404(alertid)
    recipient = Client.query.get_or_404(client_id)

    
    # Extracting alert data
    alertSubject1 =  msg.subj1
    alertSubject2 =  msg.subj2
    alertBody1 = msg.part1                                                   # Hi + [clientName]
    alertBody2 = msg.part2                                                   # I’m contacting everyone on my waitlist as a
    slotLength = str(alert.slot_length)                                            #slotLength
    alertBody3 = msg.part3                                                   # min 
    bizType = ""                                                             #massage  
    slotDay = alert.slot_start_date_time.strftime("%A")                         # appointment is now available on
    slotDate = str(alert.slot_start_date_time.strftime("%d/%m/%y"))
    alertBody4 = msg.part4                                                   # starting at 
    slotStartTime = alert.slot_start_date_time.strftime("%I:%M %p")                # 
    alertBody5 = msg.part5                                                   # \nIf you would like to book in please do so on this link
    alertBody6 = msg.part6                                                   # Look forward to seeing you
    alertBody7 = msg.part7
    alertBody8 = msg.part8

    bookingURL = currentuser.timely_booking_url
    fullSubject = alertSubject1 + company_name + alertSubject2
    bodySalute = alertBody1 + recipient.first_name
    fullTextBody = bodySalute + alertBody2 + slotLength + alertBody3 + bizType + alertBody4 + slotDay + slotDate +\
                    alertBody5 + slotStartTime + alertBody6 + bookingURL + alertBody7 + alertBody8
    staffname = currentuser.user_first_name
    

    print("The fullTextBody is " + fullTextBody)
    sentTimestamp = datetime.now()


    fromName = "Boostly Notifications"
    fromAddress = "no-reply@whitecathearing.com"
    
    # # This address must be verified with Amazon SES.
    SENDER = fromName+ "<" + fromAddress + ">"
  
    # # If your account is still in the sandbox, this address must be verified.
    RECIPIENT = recipient.email
    
    # # the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"
    
    # # The subject line for the email.
    SUBJECT = fullSubject
    
    
    # # The email body for recipients with non-HTML email clients.
    BODY_TEXT = fullTextBody

    # # The HTML body of the email.
    BODY_HTML = """
    <html>
    <head></head>
    <body>
        <tr height="32" style="height:32px">
            <td></td>
        </tr>
        <tr align="center">
            <td>
                <div>
                    <div></div>
                </div>
                <table border="0" cellspacing="0" cellpadding="0"
                    style="padding-bottom:20px;min-width:80%;width:80%">
                    <tbody>
                        <tr>
                            <td width="8" style="width:8px"></td>
                            <td>
                                <div style="border-style:solid;border-width:thin;border-color:#dadce0;border-radius:8px;padding:40px 40px"
                                    align="center" class="m_-1106791331338812591mdv2rw"><img src="https://boostly-site-images.s3.amazonaws.com/logo-03.png"
                                        width="148" height="48" aria-hidden="true" style="margin-bottom:5px" alt="Boostly" class="CToWUd" data-bit="iit">
                                    <div
                                        style="font-family:'Google Sans',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;border-bottom:thin solid #dadce0;color:rgba(0,0,0,0.87);line-height:32px;padding-bottom:24px;text-align:center;word-break:break-word">
                                        <div style="font-size:18px">{salut} </div>
                                    </div>
                                    <div
                                        style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:rgba(0,0,0,0.87);line-height:10px;padding-top:20px;text-align:center">
                                        <p>{alertBody2} 
                                        <div style="font-size:18px;padding:15px"><strong>{slotLength} {alertBody3}</strong></div> 
                                        <br> {bizType} {alertBody4}
                                        <div style="font-size:18px;padding:15px; padding-top: 25px"><strong>{slotDay}, {slotDate}</strong></div>
                                        <div style="font-size:18px;padding:15px">{alertBody5} <strong> {slotStartTime}</strong> {alertBody6}</div>
                                        </p>
                                    </div>
                                    <div
                                        style="padding-top:16px;text-align:center"><a
                                            href= {wurl}
                                            style="font-family:'Google Sans',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;line-height:16px;color:#ffffff;font-weight:400;text-decoration:none;font-size:14px;display:inline-block;padding:10px 24px;margin:5px;background-color:#A68986;border-radius:5px;min-width:100px"
                                            target="_blank">Grab the slot!</a>
                                    </div>
                                    <div
                                        style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:rgba(0,0,0,0.87);line-height:30px;padding-top:20px;text-align:center">
                                        <p>{alertBody7}
                                            <br>{staffname}
                                        </p>
                                    </div>
 
                                    
                                    <div style="padding-top:20px;font-size:14px;line-height:16px;color:#5f6368;letter-spacing:0.3px;text-align:center">
                                        <b>Note:</b><br>
                                        {alertBody8}<br>
                                    </div>
                                </div>
                            </td>
                            <td width="8" style="width:8px"></td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <tr height="32" style="height:32px">
            <td></td>
        </tr>
    </body>
    </html>
    """.format(salut=bodySalute, alertBody2=alertBody2, slotLength=slotLength, alertBody3=alertBody3, bizType=bizType, alertBody4=alertBody4,\
                slotDay=slotDay, slotDate=slotDate, alertBody5=alertBody5, slotStartTime=slotStartTime,\
                alertBody6=alertBody6, wurl=bookingURL, alertBody7=alertBody7, staffname=staffname, alertBody8=alertBody8)
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    # Create SES client (edited)
    ses = boto3.client('ses', region_name=AWS_REGION)
    try:
        #Provide the contents of the email.
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong. 
    except ClientError as e:
        print("Something went wrong while trying to send out the email" + str(e))
        sentAlertRecord = SentWaitAlert(slot_start_date_time=alert.slot_start_date_time, 
                                        slot_length=alert.slot_length,
                                        user_id=alert.user_id,
                                        msg_tmpl=alert.msg_tmpl,
                                        client_id=client_id,
                                        send_alert_id=alert.id,
                                        last_updated=datetime.now(),
                                        status="failed")
        db.session.add(sentAlertRecord)
        db.session.commit()
        db.session.refresh(sentAlertRecord)
        print("The successful sentAlertRecord id is: " + str(sentAlertRecord.id))

    else:
        print("Email sent to " + RECIPIENT + "! Message ID:" + response['MessageId']),
        # Now I want to create a new record in the database for each client that we're sending to
        sentAlertRecord = SentWaitAlert(slot_start_date_time=alert.slot_start_date_time, 
                                        slot_length=alert.slot_length,
                                        user_id=alert.user_id,
                                        msg_tmpl=alert.msg_tmpl,
                                        client_id=client_id,
                                        send_alert_id=alert.id,
                                        last_updated=datetime.now(),
                                        status="sent")
        db.session.add(sentAlertRecord)
        db.session.commit()
        db.session.refresh(sentAlertRecord)
        print("The failed sentAlertRecord id is: " + str(sentAlertRecord.id))
    finally:
        cleanup(db.session)

    childResponse = {
        'salut' : bodySalute,
        'slotLength' : slotLength,
        'slotDay' : slotDay,
        'slotDate' : slotDate,
        'slotStartTime' : slotStartTime,
        'wurl' : bookingURL,
        'sentTimestamp' : sentTimestamp
    }
    print("Sending back childResponse: " + str(childResponse))
  
    return {
        'statusCode': 200,
        'childResponse' : str(childResponse),

    }