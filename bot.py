#!/usr/bin/python
import time, os, sys
from routing import worker
import analysis
import datetime


def restartBot():
        python = sys.executable
        os.execl(python, python, * sys.argv)


if __name__=='__main__':
        try:
                worker.start()

        except Exception as e:
                print('Slack Service error, main exception: %s' % e)
                worker.stop()
                restartBot()
        worker.stop()
