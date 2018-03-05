# from models import  SampleCount
# from celery.decorators import task
# 
# 
# 
# @task()
# def delay():
#         try:
#             sc = SampleCount.object.get(pk=1)
#         except:
#             sc = SampleCount()
#         sc.num = sc.num + 1
#         sc.save()    