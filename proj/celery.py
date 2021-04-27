from celery import Celery
from celery.schedules import crontab


app = Celery('proj',
             broker='amqp://guest:guest@localhost:5672/celery',
             backend='rpc://guest:guest@localhost:5672/celery',
             include=['proj.testingcelery', 'proj.scrapeEtWebsite'])

"""app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'proj.scrapeEtWebsite.etWebScrape',
        # , day_of_week='mon-fri'),
        'schedule': crontab(hour=[9, 10, 11, 12, 13, 14, 15]),
        'args': ('mbl-infrastructures-ltd', '30660', 'MBLINFRA')
    },
}"""

@app.on_after_configure.connect
def add_periodic(**kwargs):
    app.add_periodic_task(10.0, etWebScrape.s(
        'mbl-infrastructures-ltd', '30660', 'MBLINFRA'), name='add every 10')

app.conf.timezone = 'Asia/Kolkata'

if __name__ == "__main__":
    app.start()
