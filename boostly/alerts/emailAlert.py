import csv, smtplib, ssl

message = """Subject: Your grade

Hi {name}, your grade is {grade}"""
from_address = "my@gmail.com"
password = input("Type your password and press enter: ")

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(from_address, password)
    with open("contacts_file.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for name, email, grade in reader:
            server.sendmail(
                from_address,
                email,
                message.format(name=name,grade=grade),
            )





import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime


def sendEmail(alert):
    
    # Extracting alert data

    alertID = alert.alertID
    calID = alert.calID
    freeOwner = alert.freeOwner
    freeStatus = alert.freeStatus
    freeStart = alert.freeStartTime
    freeEnd = event['freeEnd']
    parentSentTimestamp = event['sendingTimestamp']

    freeDateStart = datetime.strptime(freeStart, '%Y-%m-%d %H:%M:%S' )
    freeStartTime = freeDateStart.strftime('%H:%M%p')
    freeStartDay = freeDateStart.strftime('%A')
    freeStartDate = freeDateStart.strftime('%d %b %Y')
    print("The freeStatus before condition is: " + freeStatus)
    
    if freeStatus=="confirmed":
        freeStatus = "moved"
        
    print("The freeStatus after condition is: " + freeStatus)
    fromName = "Boostly Notifications"
    fromAddress = "no-reply@whitecathearing.com"
    
    waitAlertFormURL += alertID     # Adding the specific alertID to the URL
    
    # # This address must be verified with Amazon SES.
    SENDER = fromName+ "<" + fromAddress + ">"
  
    # # If your account is still in the sandbox, this address must be verified.
    RECIPIENT = freeOwner
    
    # # the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"
    
    # # The subject line for the email.
    SUBJECT = "Do you want to notify your waitlist? An appointment slot has opened up!"
    
    
    # # The email body for recipients with non-HTML email clients.
    BODY_TEXT = "Let's see if this works!" + "An appointment has been " + freeStatus + ". Choose what you'd like to do : button1: NotifyWaitlist button2: BlockOffSlot"
                
    # # The HTML body of the email.
    BODY_HTML = """<html>
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
                    style="padding-bottom:20px;max-width:550px;min-width:220px">
                    <tbody>
                        <tr>
                            <td width="8" style="width:8px"></td>
                            <td>
                                <div style="border-style:solid;border-width:thin;border-color:#dadce0;border-radius:8px;padding:40px 20px"
                                    align="center" class="m_-1106791331338812591mdv2rw"><img
                                        src="https://ci5.googleusercontent.com/proxy/T_zJ7UbaC9x27OP4-ZCPfDipqYLSGum30AlaxEycVclfvxO8Cze0sZ0kCrXlx6a-MgvW2tswbIyiNVfczjDuGh9okorzC5SUJDfwkHr6-3j1KUu94HuAw5uxM_jaElQef3Sub84=s0-d-e1-ft#https://www.gstatic.com/images/branding/googlelogo/2x/googlelogo_color_74x24dp.png"
                                        width="74" height="24" aria-hidden="true" style="margin-bottom:16px" alt="Google" class="CToWUd" data-bit="iit">
                                    <div
                                        style="font-family:'Google Sans',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;border-bottom:thin solid #dadce0;color:rgba(0,0,0,0.87);line-height:32px;padding-bottom:24px;text-align:center;word-break:break-word">
                                        <div style="font-size:18px">An appointment at </div>
                                        <div style="font-size:24px">{fst} on {fsd}, {fsdt}</div> 
                                        <div style="font-size:18px">has been {fs} for </div>
                                        <div style="font-size:18px">{fo}</div>
    
                                    </div>
                                    <div
                                        style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:rgba(0,0,0,0.87);line-height:20px;padding-top:20px;text-align:center">
                                        <br>Choose what you'd like to do:<div
                                            style="padding-top:16px;text-align:center"><a
                                                href= {wurl}
                                                style="font-family:'Google Sans',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;line-height:16px;color:#ffffff;font-weight:400;text-decoration:none;font-size:14px;display:inline-block;padding:10px 24px;margin:5px;background-color:#A68986;border-radius:5px;min-width:100px"
                                                target="_blank">Notify Your Waitlist</a><br><a
                                                href="https://www.amazon.com"
                                                style="font-family:'Google Sans',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;line-height:16px;color:#A68986;border:1px solid #A68986;font-weight:400;text-decoration:none;font-size:14px;display:inline-block;padding:10px 24px;margin:5px;background-color:#ffffff;border-radius:5px;min-width:100px"
                                                target="_blank">Block Off This Slot</a></div>
                                    </div>
                                    
                                    <div style="padding-top:20px;font-size:12px;line-height:16px;color:#5f6368;letter-spacing:0.3px;text-align:left">
                                        <b>Note:</b><br>
                                        <b>"Notify Your Waitlist"</b> will allow you to send an email to your Boostly-Timely waitlist<br>
                                        <b>"Block Off This Slot"</b> will auto-magically create an event on your Timely calendar. This will make sure that no one else will be able to make another booking during this timeslot.<br><br>
                                    </div>
                                </div>
                                <div style="text-align:left">
                                    <div
                                        style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;color:rgba(0,0,0,0.54);font-size:11px;line-height:18px;padding-top:12px;text-align:center">
                                        <div>PS: If you ignore this notification the slot will remain open on your Timely booking link. Anyone will be able to make a booking for this timeslot as per usual.</div>
                                        <div style="direction:ltr">© 2023 Boostly Magic</div>
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
    </html>""".format(fst=freeStartTime, fsd=freeStartDay, fsdt=freeStartDate, fs=freeStatus, fo=freeOwner, wurl=waitAlertFormURL)
    
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
        print("Something went wrong while trying to send out the email" + e.response['Error']['Message'])
    else:
        print("Email sent to " + RECIPIENT + "! Message ID:" + response['MessageId']),
        print()
    
    childResponse = {
        'alertURL' : waitAlertFormURL,
        'freeCalID' : calID,
        'freeOwner' : freeOwner,
        'freeStatus' : freeStatus,
        'freeStart' : freeStart,
        'freeEnd' : freeEnd,
        'parentSentTimestamp' : parentSentTimestamp
    }
    print("Sending back childResponse: " + str(childResponse))
  
    return {
        'statusCode': 200,
        'childResponse' : str(childResponse),

    }