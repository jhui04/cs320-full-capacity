from django.core.management.base import BaseCommand
from fcapp.main.mongo_models import Device
from fcapp.main.serializers import DeviceSerializer
import json
import time

class Command(BaseCommand):
	help = 'Import JSON file and optionally wipe database'

	def add_arguments(self, parser):
		parser.add_argument('-f', '--file', dest='file', help='JSON file with data', metavar='FILE'),
		parser.add_argument('-w', '--wipe', dest='wipe', action='store_true', default=False, help='Wipe database')
	

	def handle(self, *args, **options):
		wipe_db = options['wipe']
		print('WIPE_DB', wipe_db)

		if wipe_db:
			self.stdout.write('WIPING DATABASE ({} entries)... hit Ctrl-C within 5 seconds.'.format(Device.objects.count()))
			time.sleep(5)
			Device.objects.all().delete()

		if not options['file']:
			self.stdout.write('Specify a path to a JSON file with the -f option.')
			return

		json_text = open(options['file'], 'r').read()
		data = json.loads(json_text)

		for dev in data:
			print('DEV', dev['serialNumberInserv'])
			s = DeviceSerializer(data=dev)
			if s.is_valid():
				s.save()
			else:
				print('ERROR: invalid!', s.errors)
				exit(0)