from celery import shared_task
import json
from .sender import send_via_api, MqttSender
from .models import Notification, Reminder, RentDemand, instance_get_debtors
from .serializer import NotificationSerializer
from property.models import DebtRecord

sender = MqttSender()

@shared_task
def populate_notificationDb():
    # print('[notification-task] hello world')
    count_reminder = 0
    count_demand = 0

    #get all active debtors 
    active_debtors = DebtRecord.objects.filter(fully_paid=False)

    # index debtors into reminder or rent_demand notifications based on due date
    for debtor in active_debtors:
        if instance_get_debtors(debtor) == 'reminder notice':
            count_reminder +=1
        elif instance_get_debtors(debtor) == 'demand notice':
            count_demand +=1
        else:
            print(f'[notification-task] debtor not (reminder nor demand): {debtor}')
    print(f'[notification-task] {count_reminder} reminder notification created \n{count_demand} demand notifications created')
    
    # send_via_api mails to messenger server
    # only pending notices
    notices = Notification.objects.filter(status_flag = 'pending')
    # exclude sent and delivered notices
    # notices = Notification.objects.exclude(status_flag__in=['sent', 'delivered'])
    
    # ensure not empty notices
    if notices:
        # convert from querysets to data type by serializing
        serialized_notices = NotificationSerializer(notices, many = True)
        serialized_data = serialized_notices.data
        json_data = json.dumps(serialized_data)
        print(f'this is serialized notices:\n{json_data}\ntype: {type(json_data)}')
        # send_via_api(notices)
        sender.send_via_mqtt(json_data)
        
    else:
        print(f'[task-populate_notification] no new notice')

