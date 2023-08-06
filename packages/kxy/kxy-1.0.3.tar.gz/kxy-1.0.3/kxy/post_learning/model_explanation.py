#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Estimation of the top-:math:`k` most valuable variables in a supervised learning problem for every possible :math:`k`, and 
the corresponding achievable performances.
"""
import logging
logging.basicConfig(level=logging.INFO)
import requests
import sys
from time import time, sleep

import numpy as np
import pandas as pd

from kxy.api import APIClient, upload_data, approx_opt_remaining_time

# Cache old job ids to avoid being charged twice for the same job.
EXPLANATION_JOB_IDS = {}

def model_explanation(data_df, prediction_column, problem_type):
	"""
	.. _model-explanation:
	Analyzes the variables that a model relies on the most in a brute-force fashion.
	
	The first variable is the variable the model relies on the most. The second variable is the variable that complements the first variable the most in explaining model decisions etc.

	Running performances should be understood as the performance achievable when trying to guess model predictions using variables with selection order smaller or equal to that of the row.

	When :code:`problem_type=None`, the nature of the supervised learning problem (i.e. regression or classification) is inferred from whether or not :code:`prediction_column` is categorical.


	Parameters
	----------
	data_df : pandas.DataFrame
		The pandas DataFrame containing the data.
	prediction_column : str
		The name of the column containing true labels.
	problem_type : None | 'classification' | 'regression'
		The type of supervised learning problem. When None, it is inferred from the column type and the number of distinct values.



	Returns
	-------
	result : pandas.DataFrame
		The result is a pandas.Dataframe with columns (where applicable):

		* :code:`'Selection Order'`: The order in which the associated variable was selected, starting at 1 for the most important variable.
		* :code:`'Variable'`: The column name corresponding to the input variable.
		* :code:`'Running Achievable R-Squared'`: The highest :math:`R^2` that can be achieved by a classification model using all variables selected so far, including this one.
		* :code:`'Running Achievable Accuracy'`: The highest classification accuracy that can be achieved by a classification model using all variables selected so far, including this one.
		* :code:`'Running Achievable RMSE'`: The highest classification accuracy that can be achieved by a classification model using all variables selected so far, including this one.


	.. admonition:: Theoretical Foundation

		Section :ref:`a) Model Explanation`.

	"""
	assert prediction_column in data_df.columns, 'The label column should be a column of the dataframe.'
	assert problem_type.lower() in ['classification', 'regression']
	if problem_type.lower() == 'regression':
		assert np.can_cast(data_df[prediction_column], float), 'The prediction column should be numeric'

	k = 0
	max_k = 100
	sys.stdout.write('\r')
	sys.stdout.write("[{:{}}] {:d}% ETA: {}".format("="*k+">", max_k, k, approx_opt_remaining_time(k)))
	sys.stdout.flush()

	file_identifier = upload_data(data_df)
	if file_identifier:
		job_id = EXPLANATION_JOB_IDS.get((file_identifier, prediction_column, problem_type), None)
		if job_id:
			api_response = APIClient.route(
				path='/wk/variable-selection', method='POST', \
				file_identifier=file_identifier, target_column=prediction_column, \
				problem_type=problem_type, timestamp=int(time()), job_id=job_id)
		else:
			api_response = APIClient.route(
				path='/wk/variable-selection', method='POST', \
				file_identifier=file_identifier, target_column=prediction_column, \
				problem_type=problem_type, timestamp=int(time()))

		while api_response.status_code == requests.codes.ok and k <= max_k:
			if k%5 != 0:
				sleep(12)
				k += 1
				sys.stdout.write('\r')
				sys.stdout.write("[{:{}}] {:d}% ETA: {}".format("="*k+">", max_k, k, approx_opt_remaining_time(k)))
				sys.stdout.flush()
			else:
				try:
					sys.stdout.write('\r')
					response = api_response.json()
					if 'job_id' in response:
						job_id = response['job_id']
						EXPLANATION_JOB_IDS[(file_identifier, prediction_column, problem_type)] = job_id
						sleep(12)
						k += 1
						sys.stdout.write("[{:{}}] {:d}% ETA: {}".format("="*k+">", max_k, k, approx_opt_remaining_time(k)))
						sys.stdout.flush()
						# Note: it is important to pass the job_id to avoid being charged twice for the work.
						api_response = APIClient.route(
							path='/wk/variable-selection', method='POST', \
							file_identifier=file_identifier, target_column=prediction_column, \
							problem_type=problem_type, timestamp=int(time()), job_id=job_id)
					else:
						sys.stdout.write("[{:{}}] {:d}% ETA: {}".format("="*max_k, max_k, max_k, approx_opt_remaining_time(max_k)))
						sys.stdout.write('\n')
						sys.stdout.flush()
						result = {}

						if 'selection_order' in response:
							result['Selection Order'] = response['selection_order']				

						if 'variable' in response:
							result['Variable'] = response['variable']	

						if 'r-squared' in response:
							result['Running Achievable R-Squared'] = response['r-squared']

						if 'log-likelihood' in response:
							result['Running Achievable Log-Likelihood Per Sample'] = response['log-likelihood']

						if 'rmse' in response and problem_type.lower() == 'regression':
							result['Running Achievable RMSE'] = response['rmse']

						if 'accuracy' in response and problem_type.lower() == 'classification':
							result['Running Achievable Accuracy'] = response['accuracy']

						result = pd.DataFrame.from_dict(result)

						if 'selection_order' in response:
							result.set_index('Selection Order', inplace=True)

						return result


				except:
					logging.exception('Model explanation failed. Last HTTP code: %s, Content: %s' % (api_response.status_code, api_response.content))
					return None

		if api_response.status_code != requests.codes.ok:
			try:
				response = api_response.json()
				if 'message' in response:
					logging.error('\n%s' % response['message'])
			except:
				logging.error('\nModel explanation failed. Last HTTP code: %s, Content: %s' % (api_response.status_code, api_response.content))

	return None


