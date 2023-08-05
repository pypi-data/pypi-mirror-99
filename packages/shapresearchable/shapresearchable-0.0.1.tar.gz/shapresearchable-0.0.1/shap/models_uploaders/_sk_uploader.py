import pathlib
import shutil
import pickle
import yaml
import os
import pandas as pd 
import requests


class skExplainerUploader():
	"""docstring for """
	def __init__(self, token_id):

		self.token_id = token_id

	def test_sk_upload(self):
		x_dir = pathlib.Path('x_temp')
		shutil.rmtree(x_dir, ignore_errors=True)
		x_dir.mkdir()

	def upload_sk_model(self, model, project_id, model_id):

		url = 'http://127.0.0.1:8000/explain/upload_data_set/'

		model_dir = pathlib.Path(model_id)
		shutil.rmtree(model_dir, ignore_errors=True)
		model_dir.mkdir()

		personal_info = {'token': self.token_id, 'project_id' : project_id, 'model_id' : model_id}

		with open(model_dir / 'model.pkl', 'wb') as pkl_file:
			pickle.dump(model, pkl_file)

			file_final_name = model_id + '/model.pkl'
			files = {'file': ('model.pkl', open(file_final_name, 'rb')), }

			response = requests.post(url, files=files, data=personal_info)
			print(response.status_code, response.text)
			#Then we do the uploading

	def upload_sk_dataset(self, filename, project_id, model_id, target_name):

		url = 'http://127.0.0.1:8000/explain/upload_data_set/'

		dataFrame = []

		# print(os.path.splitext(filename)[-1])
		
		if os.path.splitext(filename)[-1] == '.csv':

			dataFrame = pd.read_csv(filename)

		elif os.path.splitext(filename)[-1] == '.xlsx':

			dataFrame = pd.read_excel(filename)

		else:
			ex = Exception('Please us .xlsx or .csv files')
			raise ex;

		target_colum = dataFrame[target_name]
		x_colums = dataFrame.drop(target_name, axis=1)

		x_dir = pathlib.Path('x_temp')
		shutil.rmtree(x_dir, ignore_errors=True)
		x_dir.mkdir()

		personal_info = {'token': self.token_id, 'project_id' : project_id, 'model_id' : model_id}



		with open(x_dir / 'x_csv.csv', 'wb') as x_file:
			x_colums.to_csv(x_file)

			file_final_name = 'x_temp/x_csv.csv'
			files = {'file': ('x_ask.csv', open(file_final_name, 'rb')), }

			response = requests.post(url, files=files, data=personal_info)
			print(response.status_code, response.text)


			#Do the uplaod network things

		with open(x_dir / 'y_csv.csv', 'wb') as y_file:
			target_colum.to_csv(y_file)

			file_final_name = 'x_temp/y_csv.csv'
			files = {'file': ('y_ask.csv', open(file_final_name, 'rb')), }

			response = requests.post(url, files=files, data=personal_info)
			print(response.status_code, response.text)



		


