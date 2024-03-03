from studease.models import RollNumber

def datagiver():
    for i in range(1,2):
        data = {'rollnumber': 'uday', 'id': 'ec1'}
        new_instance = RollNumber(**data)
        new_instance.save()

datagiver()