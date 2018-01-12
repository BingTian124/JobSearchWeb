import pymongo
from pymongo import MongoClient
import datetime
import dateutil.relativedelta
from datetime import timedelta, date


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield end_date - timedelta(n+1)


class DBhelper(object):
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        
    def insert_one(self,item):
        db = self.client.linkedinentry
        if not self.exists(item,db.repo):
            db.repo.insert_one(item)


    def exists(self,item,collection):
        return collection.find_one({u'_id' : item['_id']}) != None


    def getLatestItems(self):
        db = self.client.linkedinentry
        todayData = db.repo.find({'date': str(datetime.date.today())}).sort([('date',1)]).limit(500)
        old = []
        today = datetime.date.today()
        start_day = today - dateutil.relativedelta.relativedelta(days=10)
        for single_date in daterange(start_day, today):
            jobData = db.repo.find({u'date':  str(single_date)  }).sort([('date',1)]).limit(800)
            count = jobData.count()
            if count == 0:
                continue
            jobPack = {u'date' : str(single_date), 'jobData': jobData}
            old.append(jobPack)
        return todayData,old




