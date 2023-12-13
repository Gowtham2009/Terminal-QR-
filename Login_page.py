import smtplib #importing SMTP(Simple mail transfer protocol) library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import qrcode                                 
#===========================================================
import mysql.connector  #importing mysql library
mydb = mysql.connector.connect( #
  host="Mention your Host",
  user="root",
  password="Your Password",
  database="Your Database"
)

mycursor = mydb.cursor()

count = 0
#=============================================================================================================
def generate_qr_code(data, file_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)
    return file_path

def Mail_send(Stu_Name,Stu_Aad,Stu_Pass_info,Stu_Pass_valid,Stu_Mail):
    # Function to generate a QR code and return the file path
    # Email configuration
    r_mail =str(Stu_Mail)
    sender_email = 'Enter your mail ID'
    sender_password = 'Your password'
    receiver_email = r_mail
    subject = 'Gmail ID QR Code'

    # Gmail ID to be encoded in the QR code
    Id = f'{Stu_Name}-{Stu_Aad}-{Stu_Pass_info}-{Stu_Pass_valid}'

    # Generate QR code for the Gmail ID
    qr_code_file_path = 'Id_qrcode.png'
    generate_qr_code(Id, qr_code_file_path)

    # Create the MIME object
    message = MIMEMultipart()
    message['Your Mail'] = sender_email
    message[r_mail] = receiver_email
    message['Test QR >> plaese ignore the mail'] = subject

    # Attach the email content as text
    email_content = f'Hello, this is your Registered Bus Pass ID QR code: {Id}\n This mail is for Test purpose \n Thanking you,\n [Your Name]'
    message.attach(MIMEText(email_content, 'plain'))

    # Attach the QR code image
    with open(qr_code_file_path, 'rb') as qr_file:
        img_data = MIMEImage(qr_file.read(), name='Id_qrcode.png')
        message.attach(img_data)

    # Connect to the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Log in to the email account
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Disconnect from the SMTP server
    server.quit()

    print('Email with Gmail ID QR code sent successfully!')
#===================================================================================================================================================================================================================================================
#printing Details
def Print_pass(Username):
    Unam = str(Username)
    print(f"==================================> Hello {Unam} <=========================================")
    print("We are printing your data, just a while Please!!...........")
    Que = (f"SELECT Student_Name,Student_Phone_Number,Student_Aadhar_Number,Student_Age,Student_Education,Student_Pass_info,Student_Pass_Validity,Student_Roll_Num,Student_Mail_id FROM students_info WHERE Student_Mail_id = '{Unam}' ")
    mycursor.execute(Que)
    result = mycursor.fetchone()
    print(result)

#====================================================================================================================================================================================================================================================
#Apply Pass
def Apply_Pass(Username):
    print("=======================> Welcome to the RTC Bus Pass Apllication <=========================")
    insert=("INSERT INTO students_info(Student_Name,Student_Phone_Number,Student_Aadhar_Number,Student_Age,Student_Education,Student_Pass_info,Student_Pass_Validity,Student_Roll_Num,Student_Mail_id)values(%s,%s,%s,%s,%s,%s,%s,%s,%s) ")
    Stu_Name = input("==> Enter your Name: ")
    Stu_Phone = int(input("==> Enter your Phone No: "))
    Stu_Aad = int(input("Enter your Aadhar Number: "))
    Stu_Age = int(input("Enter your Age: "))
    Stu_Edu = input("Enter your Education (Example: B.Tech, Degree, Intermediate, School,etc..): ")
    Stu_Pass_info = input("Enter your pass Info (Metro or General): ")
    Stu_Pass_valid = input("Enter your Pass Validity (Ex: 3M, 6M, 9M, 12M, M -> Months): ")
    Stu_Roll = input("Enter your Registered Number from your (School,College.etc..): ")
    print("As your maild is your Username it will be continue as your Mail ID for your Apllication!! ")
    Stu_Mail = str(Username)
    print("Processing your Application.......")
    val = (Stu_Name,Stu_Phone,Stu_Aad,Stu_Age,Stu_Edu,Stu_Pass_info,Stu_Pass_valid,Stu_Roll,Stu_Mail)
    mycursor.execute(insert,val)
    mydb.commit()
    print("Succesfully Your Apllication Submited..")
    print("======================> Your Details Added into our Database!! <=======================")
    print("You will get a QR to your registered Mail ID........")
    Mail_send(Stu_Name,Stu_Aad,Stu_Pass_info,Stu_Pass_valid,Stu_Mail)

#===========================================================================================================================================================
#Main Page
def Main_Page(Username):
    print("=========================================================================================================================")
    print("=========================================================================================================================")
    print(f"                           Hello!! {Username} Welcome to the Main page of RTC.....")
    print("=========================================================================================================================")
    print("=========================================================================================================================")
    Take_input = int(input("Enter the number '1' for Apply Bus pass or '2' for to print your applied Bus Pass: "))
    if Take_input == 1:
        Apply_Pass(Username)
    elif Take_input == 2:
        Print_pass(Username)
    else:
        print('You have entered wrong number!!!!!')
        print("Your now Redirecting to login page............")
        login()
#==================================================================================================================================================================================================
#Login or SignUp Functions
# Cpass Function
def Cpass(NP):
    C = input("Please confirm your Password: ")
    return C
 
# Wrong password function
def wrongpassword(Uname):
    global count # we can access the count(variable) anywhere in the code
    count += 1 #count getting increement
    if count == 3: #if count become 3 then it will enter into the if condition!!
        print("======> As Number of attempts reached for password entry, please Update your new password!! <====")
        New_password = input("Create your new password: ") # creation of new password
        Confirm_Password = input("Please confirm your Password: ") #creation of confirm password
        while New_password != Confirm_Password: # the while loop runs until the both new and confirm passwords will be equal
            Confirm_Password = Cpass(New_password) 
        mycursor.execute("UPDATE user_login_data SET User_password = %s WHERE User_name = %s", (Confirm_Password, Uname)) # we are using 'UPDATE' query as we want update the new password in the place of old password!!
        mydb.commit() #the commit() method is used to save the changes made through a series of SQL commands as a transaction. When you perform operations like insert, update, or delete on a database, those changes are not immediately applied to the database
        print("=====> Successfully we have updated your Password..... <=====")
        print("Now, Please Login with your Credentials....")
        print("========> Redirecting to Login Page..... <========")#Redirecting to login page
        login() #It will go to login function..
        

    else:
        print("====> You Entered Wrong Password please retry <====")
        mycursor.execute("SELECT User_name,User_password from user_login_data")# we are using SELECT querey as we need only two columns so we are selecting them!!
        user_data = mycursor.fetchall() #we are fetching the required columns from the database and now the user_data(variable) contains the required data
        Password= input(f"=====> Please Enter your password: ")
        passwords = [result[1] for result in user_data] # we are using list comprehension 
        if Password in passwords:
            print("==>  Authentication Successfull  <==")
            print("=======> Redirectiong to main Page!! <=======")#Redirecting to Main Page.......
            Main_Page(Uname)
        else:
            wrongpassword(Uname)

def is_valid_gmail(email):
    return "@" in email and (email.endswith("@gmail.com") or email.endswith("@gitam.in"))#checking whether the user entered correct gmail or not

#SignUp Page

def SignUp():
    print("====> Please Enter your details <====")
    insert = "INSERT INTO user_login_data(User_name, User_Password) VALUES (%s, %s)"

    New_username = input("Enter your new Username(Gmail ID) : ")
    if not is_valid_gmail(New_username):# if user entered gmail in wrong format then again he need to start from first
        print("Enter a valid Gmail ID.")
        print("====================> please SignUp Again <========================")#Redirecting to SignUp page
        SignUp()
    # creating New password
    New_password = input("Create your new password: ") # 
    Confirm_Pass = input("Please confirm your Password: ")

    while New_password != Confirm_Pass:# the while loop runs until the both new and confirm passwords will be equal
        Confirm_Pass = Cpass(New_password)

    val = (New_username, Confirm_Pass) 
    mycursor.execute(insert, val)#using cursor and inserting the values to database
    mydb.commit()

    #global Useranme  # Assuming this is a global variable used elsewhere
    #Useranme = New_username  # Update the global variable after successful signup

    print("Successfully Updated Your Details.........")
    print("==================================> Thank You For Signing Up <=================================")
    print("..................................Redirecting to Login Page.................")#Redirecting to login page
    login()



#Login Page
def login():
    global Username
    print("==> Please Login With your Credentials <== ")
    Username = input("   Enter your Username(gmail): ")
    mycursor.execute("SELECT User_name,User_password from user_login_data")
    user_data = mycursor.fetchall()
    usernames = [result[0] for result in user_data]#list comprehension
    #print(user_data)
    #print(usernames)
    if Username in usernames:
        Password= input(f"Hello!! {Username:<5} please Enter your password: ")
        passwords = [result[1] for result in user_data]
        if Password in passwords:
            print("==>  Authentication Successfull  <==")
            print("=======> Redirectiong to main Page!! <=======")#Redirecting to Main page.......
            Main_Page(Username)
        else:
            wrongpassword(Username)
    else:
        print("====> Your Username not found <=====")
        print("====> Redirecting to SignUp page........")#Redirecting to SignUp page
        SignUp()

#==============================================================================================================================================================

#Main
if __name__=="__main__" :
    print("===============================================")
    print("       Welcome to Login Page of RTC.....   ")
    Login = int(input("   Press 1 for Login or 2 for SignUp: "))# Typecasting the input into Integer as we know it will take the inpust as string
    if Login == 1:#1 for login
        login()
    elif Login == 2:#2 for SignUp
        SignUp()
    else:
        print("OOps!! you have entered other than given number '1' or '2'")
        print("Not a problem you are redirected to Login page.........")
        login()

        
