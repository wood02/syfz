# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from Syfz.setup import django_setup
import json
from datetime import datetime, timedelta
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class SyfzTask:
    """
    Syfz，增加周期性任务
    """

    def __init__(self, name):
        self.name = name
        self.periodic_task = self.get_task()

    def create_schedule(self, every, period):
        print(IntervalSchedule.PERIOD_CHOICES)
        print(IntervalSchedule.MINUTES)

        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=every,
            period=period,
        )
        return schedule

    def get_task(self):
        return PeriodicTask.objects.filter(name=self.name).first()

    def update_or_create(self, every, period, task, **kwargs):
        start_time = kwargs.pop('start_time', None)
        print(start_time)
        defaults = {
            'interval': self.create_schedule(every, period),
            'task': task,  # name of task.
            'args': json.dumps([]),
            'kwargs': json.dumps(kwargs),
            'expires': None,
            'enabled': True,
            'start_time': start_time
            # 'expires': datetime.now() + timedelta(seconds=30),
        }
        periodic_task = PeriodicTask.objects.update_or_create(
            # we created this above.
            name=self.name,  # simply describes this periodic task.
            defaults=defaults
        )
        return periodic_task

    def start(self):
        """
        启动任务
        """
        if self.periodic_task:
            self.periodic_task.enabled = True
            self.periodic_task.save()

    def stop(self):
        """
        停止任务
        """
        if self.periodic_task:
            self.periodic_task.enabled = False
            self.periodic_task.save()


if __name__ == '__main__':
    st = SyfzTask(name="Importing contacts1")
    st.update_or_create(4, "seconds", 'apps.system.tasks.mul', x=3, y=2)
    # st.stop()
