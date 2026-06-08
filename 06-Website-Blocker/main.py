import datetime

end_time = datetime.datetime(2026,6,9)

while True:
    if datetime.datetime.now()<=end_time:
        print("block website")
        time.sleep(300)
    else:
        break
print("allowed to access websites")