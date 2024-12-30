import json
from rest_framework.views import APIView
from rest_framework.response import Response
from sources.models import sources
from django.http import JsonResponse
from rest_framework.decorators import api_view
import os
import pandas as pd
from main.connectors import connectors
from .views import decryptDbCredential
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from .views import changeDateFormat

class Sources(APIView):
	@api_view(('GET',))
	def get(self):
		_sources = [user.selected_tables for user in sources.objects.all()]
		print("_sources", _sources)
		# _sources = [
		#	 {
		#		 'source1': ['table1', 'table2']
		#	 },
		#	 {
		#		 'source2': ['table1', 'table2']
		#	 }
		# ]
		return Response({'data': _sources}, status=200)

	@api_view(('POST',))
	def getTables(request):
		source_id = request.data['source_id']
		path = f'assest/parquet_files/source_{source_id}'
		dir_list = os.listdir(path)
		table_list = {}
		for table in dir_list:
			_path = f'{path}/{table}'
			data = pd.read_parquet(_path)
			table_name = table.rsplit('.', 1)[0]
			table_list[table_name] = list(data.columns.values)
		return JsonResponse({'table_list': table_list})
		
	@api_view(('POST',))
	def getData(request):
		source_id = request.data['source_id']
		table_name = request.data['table_name']
		limit = int(request.data['limit'])
		current_page = int(request.data['current_page'])
		path = f'assest/parquet_files/source_{source_id}/{table_name}.parquet'
		data = pd.read_parquet(path)
		data = changeDateFormat(data)
		total_records = len(data.index)
		# data = data.head(50)
		start_row = (limit*current_page)-limit + 1
		data = data.iloc[(start_row - 1):(limit * current_page)]
		table_records = data.to_json(orient='records')
		return JsonResponse({'data': json.loads(table_records),'total_record':total_records})
		
	@api_view(('POST',))
	def showTables(request):
		if request.method == 'POST':
			decrypted_credential = decryptDbCredential(request.data)
			driver_name = decrypted_credential['driver_name']
			server_name = decrypted_credential['server_name']
			database_name = decrypted_credential['database_name']
			port = decrypted_credential['port']
			user_name = decrypted_credential['user_name']
			password = decrypted_credential['password']
			connection = connectors(driver_name = driver_name, server_name = server_name, database_name = 
			database_name, port = port, user_name = user_name, password = password)
		
			tables = connection.get_tables()
		
			return JsonResponse({'tables': tables})
	@api_view(('POST',))
	def showSheets(request):
		source = request.data['source']
		if request.method == 'POST' and request.data['file'] and source == "Excel":
			file = request.FILES['file']
			print("file------>",file)
			file_ext = file.name.rsplit('.', 1)[-1]
			if file_ext in ('xls','xlsx'):
				df = pd.ExcelFile(file)
				sheet_names = df.sheet_names
				return JsonResponse({'sheets':sheet_names})
			else:
				return JsonResponse({'error':"Invalid Format"})
			
		if request.method == 'POST' and request.FILES.get('file') and source == "Csv":
			file = request.FILES['file']
			file_ext = file.name.rsplit('.', 1)[-1]
			if file_ext in ('csv'):
				return JsonResponse({'error':"VALID CSV"})
			else:
				return JsonResponse({'error':"Invalid Format"})
        