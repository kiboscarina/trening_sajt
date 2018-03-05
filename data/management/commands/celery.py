import subprocess
import sys
from time import sleep

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Used for starting, stopping or restarting celery process'

    def add_arguments(self, parser):
        parser.add_argument(
            '--start',
            action='store_true',
            dest='start',
            help='start celery process',
        )
        parser.add_argument(
            '--stop',
            action='store_true',
            dest='stop',
            help='stop celery process',
        )
        parser.add_argument(
            '--restart',
            action='store_true',
            dest='restart',
            help='restart celery process',#                 newrelic_config = os.path.join(settings.BASE_DIR, 'newrelic.ini')
#                 os.environ['NEW_RELIC_CONFIG_FILE'] = '{}'.format(newrelic_config)
#                 current_env = os.environ.get('DJANGO_ENV')
#                 if current_env: os.environ['NEW_RELIC_ENVIRONMENT'] = current_env
        )

    def getInfo(self):
        processes = subprocess.check_output(['ps', 'ax']).decode("utf-8") 
        celery_lines = []
        for line in processes.split('\n'):
            if 'celery ' in line:
                if '--stop' not in line and '--start' not in line and '--restart' not in line: 
                    celery_lines.append(line)
        celery_processes = []
        if len(celery_lines) > 0:
            for line in celery_lines:
                running, pid = True, int(line.strip().split(' ')[0])
                celery_processes.append((running, pid, line))
        else:
            celery_processes = None
        return celery_processes

    def start(self):
        print ('starting celery ... ', end='')
        sys.stdout.flush()
        for i in range(5):
            processes = self.getInfo()
            if not processes:
                commands = [
                    ['celery', 'beat', '-A', 'vezbacki', '-l', 'info', '--detach', '--pidfile=../../celery/beat.pid', '--logfile=../../celery/beat.log'],
                    ['celery', '-A', 'vezbacki', 'multi', 'restart', '1', '-c', '1', '--detach', '--pidfile=../../celery/workers/%N.pid', '--logfile=../../celery/%N.log', '--verbose']
                ]
                for command in commands:
                    print('executing: {}'.format(command))
                    p = subprocess.Popen(command)
                    while(True):
                        exitCode = p.poll()
                        if exitCode != None:
                            break
                        sleep(0.1)
                    cmd_string = ' '.join(command)
                    print('successfully started {}'.format(cmd_string) if not exitCode else 'failed to start {}, exit code {}'.format(cmd_string, exitCode))
                return
            else:
                print ('\nretry #{} ... '.format(i+1)),
                sys.stdout.flush()
                sleep(5)
        if processes: 
            print('celery processes already running')
    
    def stop(self):
        print ('stopping celery ... ', end='')
        sys.stdout.flush()
        processes = self.getInfo()
        print(processes)
        shutdown_workers = ['celery', 'control', 'shutdown']
        if processes:
            shutdown_beat = ['kill']
            for p in processes:
                if 'worker' in p[2]:
                    p = subprocess.Popen(shutdown_workers)
                elif 'beat' in p[2]:
                    shutdown_beat.append(str(p[1]))
                    p = subprocess.Popen(shutdown_beat)
                else:
                    continue
                
                while(True):
                    exitCode = p.poll()
                    if exitCode != None:
                        break
                    sleep(0.1)
            print('successfully stopped' if not exitCode else 'failed to stop, exit code {}'.format(exitCode))
        else:
            print('no celery processes running')
    
    def restart(self):
        self.stop()
        self.start()
    
    def handle(self, *args, **options):
        values_true = 0
        for item in ['start', 'stop', 'restart']:
            if options[item]: values_true += 1
        
        if values_true != 1:
            exit(-1)

        if options['start']: self.start()
        elif options['stop']: self.stop()
        elif options['restart']: self.restart()