from __future__ import absolute_import
from celery import shared_task
from time import sleep
from random import random
from firewall.models import Numbers

@shared_task
def save_random(x):
    numbers = Numbers(number = x)
    numbers.save()


@shared_task
def rand_sleep():
	time = random() * 10
	sleep(time)
	return time