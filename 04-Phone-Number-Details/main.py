import phonenumbers
from phonenumbers import geocoder,carrier,timezone


num=input("Enter your phone number with country code: ")
ch=geocoder.description_for_number(phonenumbers.parse(num),"en")
cr=carrier.name_for_number(phonenumbers.parse(num),"en")
tz=timezone.time_for_number(phonenumbers.parse(num),"en")

print("Country: ",ch)
print("Operator: ",cr)
print("Timezone: ",tz)
