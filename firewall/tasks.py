from __future__ import absolute_import
from celery import shared_task
from time import sleep
from random import random

@shared_task
def square_random(x):
    return x


@shared_task
def rand_sleep():
	time = random() * 10
	sleep(time)
	return time