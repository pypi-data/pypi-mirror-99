#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Estimation of the amount by which the performance of a trained supervised learning model can be increased, either in a model-driven fashion, or a data-driven fashion.
"""
import json
import logging
logging.basicConfig(level=logging.INFO)
import requests
import sys
from time import time, sleep

import numpy as np
import pandas as pd

from kxy.api import APIClient, upload_data, approx_opt_remaining_time

# Cache old job ids to avoid being charged twice for the same job.
DD_IMPROVABILITY_JOB_IDS = {}
MD_IMPROVABILITY_JOB_IDS = {}

def data_driven_improvability(data_df, target_column, new_variables, problem_type):
	"""
	.. data-driven-improvability:
	Estimate the potential performance boost that a set of new explanatory variables can bring about.


	Parameters
	----------
	data_df : pandas.DataFrame
		The pandas DataFrame containing the data.
	target_column : str
		The name of the column containing true labels.
	new_variables : list
		The names of the columns to use as new explanatory variables.
	problem_type : None | 'classification' | 'regression'
		The type of supervised learning problem. When None, it is inferred from whether or not :code:`target_column` is categorical.



	Returns
	-------
	result : pandas.Dataframe
		The result is a pandas.Dataframe with columns (where applicable):

		* :code:`'Accuracy Boost'`: The classification accuracy boost that the new explanatory variables can bring about.
		* :code:`'R-Squared Boost'`: The :math:`R^2` boost that the new explanatory variables can bring about.
		* :code:`'RMSE Reduction'`: The reduction in Root Mean Square Error that the new explanatory variables can bring about.
		* :code:`'Log-Likelihood Per Sample Boost'`: The boost in log-likelihood per sample that the new explanatory variables can bring about.


	.. admonition:: Theoretical Foundation

		Section :ref:`3 - Model Improvability`.
		
	"""
	assert target_column in data_df.columns, 'The label column should be a column of the dataframe.'
	assert problem_type.lower() in ['classification', 'regression']
	assert len(new_variables) > 0, 'New variables should be provided'
	for col in new_variables:
		assert col in data_df.columns, '%s should be a column in the dataframe' % col
	if problem_type.lower() == 'regression':
		assert np.can_cast(data_df[target_column], float), 'The target column should be numeric'

	k = 0
	max_k = 100
	sys.stdout.write('\r')
	sys.stdout.write("[{:{}}] {:d}% ETA: {}".format("="*k+">", max_k, k, approx_opt_remaining_time(k)))
	sys.stdout.flush()

	file_identifier = upload_data(data_df)
	if file_identifier:
		job_id = DD_IMPROVABILITY_JOB_IDS.get((file_identifier, target_column, str(new_variables), problem_type), None)

		if job_id:
			api_response = APIClient.route(
				path='/wk/data-driven-improvability', method='POST', \
				file_identifier=file_identifier, target_column=target_column, \
				problem_type=problem_type, new_variables=json.dumps(new_variables), \
				job_id=job_id, timestamp=int(time()))
		else:
			api_response = APIClient.route(
				path='/wk/data-driven-improvability', method='POST', \
				file_identifier=file_identifier, target_column=target_column, \
				problem_type=problem_type, new_variables=json.dumps(new_variables), \
				timestamp=int(time()))

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
						DD_IMPROVABILITY_JOB_IDS[(file_identifier, target_column, str(new_variables), problem_type)] = job_id
						sleep(12)
						k += 1
						sys.stdout.write("[{:{}}] {:d}% ETA: {}".format("="*k+">", max_k, k, approx_opt_remaining_time(k)))
						sys.stdout.flush()
						api_response = APIClient.route(
							path='/wk/data-driven-improvability', method='POST', \
							file_identifier=file_identifier, target_column=target_column, \
							problem_type=problem_type, new_variables=json.dumps(new_variables), \
							timestamp=int(time()))
					else:
						sys.stdout.write("[{:{}}] {:d}% ETA: {}".format("="*max_k, max_k, max_k, approx_opt_remaining_time(max_k)))
						sys.stdout.write('\n')
						sys.stdout.flush()
						result = {}
						if 'r-squared-boost' in response:
							result['R-Squared Boost'] = [response['r-squared-boost']]

						if 'log-likelihood-boost' in response:
							result['Log-Likelihood Per Sample Boost'] = [response['log-likelihood-boost']]

						if 'rmse-reduction' in response and problem_type.lower() == 'regression':
							result['RMSE Reduction'] = [response['rmse-reduction']]

						if 'accuracy-boost' in response and problem_type.lower() == 'classification':
							result['Accuracy Boost'] = [response['accuracy-boost']]

						result = pd.DataFrame.from_dict(result)

						return result

				except:
					return None

		if api_response.status_code != requests.codes.ok:
			try:
				response = api_response.json()
				if 'message' in response:
					logging.error('\n%s' % response['message'])
			except:
				logging.error('\nData-driven improvability failed. Last HTTP code: %s' % api_response.status_code)

	return None


def model_driven_improvability(data_df, target_column, prediction_column, problem_type):
	"""
	.. model-driven-improvability:
	Estimate the extent to which a trained supervised learner may be improved in a model-driven fashion (i.e. without resorting to additional explanatory variables).


	Parameters
	----------
	data_df : pandas.DataFrame
		The pandas DataFrame containing the data.
	target_column : str
		The name of the column containing true labels.
	prediction_column : str
		The name of the column containing model predictions.
	problem_type : None | 'classification' | 'regression'
		The type of supervised learning problem. When None, it is inferred from whether or not :code:`target_column` is categorical.



	Returns
	-------
	result : pandas.Dataframe
		The result is a pandas.Dataframe with columns (where applicable):

		* :code:`'Lost Accuracy'`: The amount of classification accuracy that was irreversibly lost when training the supervised learner.
		* :code:`'Lost R-Squared'`: The amount of :math:`R^2` that was irreversibly lost when training the supervised learner.
		* :code:`'Lost RMSE'`: The amount of Root Mean Square Error that was irreversibly lost when training the supervised learner.		
		* :code:`'Lost Log-Likelihood Per Sample'`: The amount of true log-likelihood per sample that was irreversibly lost when training the supervised learner.

		* :code:`'Residual R-Squared'`: For regression problems, this is the highest :math:`R^2` that may be achieved when using explanatory variables to predict regression residuals.
		* :code:`'Residual RMSE'`: For regression problems, this is the lowest Root Mean Square Error that may be achieved when using explanatory variables to predict regression residuals.
		* :code:`'Residual Log-Likelihood Per Sample'`: For regression problems, this is the highest log-likelihood per sample that may be achieved when using explanatory variables to predict regression residuals.


	.. admonition:: Theoretical Foundation

		Section :ref:`3 - Model Improvability`.

	"""
	assert target_column in data_df.columns, 'The label column should be a column of the dataframe.'
	assert prediction_column in data_df.columns, 'The prediction column should be a column of the dataframe.'
	assert problem_type.lower() in ['classification', 'regression']
	if problem_type.lower() == 'regression':
		assert np.can_cast(data_df[target_column], float), 'The target column should be numeric'
		assert np.can_cast(data_df[prediction_column], float), 'The prediction column should be numeric'

	k = 0
	max_k = 100
	sys.stdout.write('\r')
	sys.stdout.write("[{:{}}] {:d}% ETA: {}".format("="*k+">", max_k, k, approx_opt_remaining_time(k)))
	sys.stdout.flush()

	file_identifier = upload_data(data_df)

	if file_identifier:
		job_id = MD_IMPROVABILITY_JOB_IDS.get((file_identifier, target_column, prediction_column, problem_type), None)

		if job_id:
			api_response = APIClient.route(
				path='/wk/model-driven-improvability', method='POST', \
				file_identifier=file_identifier, target_column=target_column, \
				problem_type=problem_type, prediction_column=prediction_column, \
				job_id=job_id, timestamp=int(time()))
		else:
			api_response = APIClient.route(
				path='/wk/model-driven-improvability', method='POST', \
				file_identifier=file_identifier, target_column=target_column, \
				problem_type=problem_type, prediction_column=prediction_column, \
				timestamp=int(time()))

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
						MD_IMPROVABILITY_JOB_IDS[(file_identifier, target_column, prediction_column, problem_type)] = job_id
						sleep(12)
						k += 1
						sys.stdout.write("[{:{}}] {:d}% ETA: {}".format("="*k+">", max_k, k, approx_opt_remaining_time(k)))
						sys.stdout.flush()
						api_response = APIClient.route(
							path='/wk/model-driven-improvability', method='POST', \
							file_identifier=file_identifier, target_column=target_column, \
							problem_type=problem_type, prediction_column=prediction_column, \
							job_id=job_id, timestamp=int(time()))
					else:
						sys.stdout.write("[{:{}}] {:d}% ETA: {}".format("="*max_k, max_k, max_k, approx_opt_remaining_time(max_k)))
						sys.stdout.write('\n')
						sys.stdout.flush()
						result = {}

						if 'lost-r-squared' in response:
							result['Lost R-Squared'] = [response['lost-r-squared']]			

						if 'lost-log-likelihood' in response:
							result['Lost Log-Likelihood Per Sample'] = [response['lost-log-likelihood']]

						if 'lost-rmse' in response and problem_type.lower() == 'regression':
							result['Lost RMSE'] = [response['lost-rmse']]

						if 'lost-accuracy' in response and problem_type.lower() == 'classification':
							result['Lost Accuracy'] = [response['lost-accuracy']]


						if problem_type.lower() == 'regression':
							if 'residual-r-squared' in response:
								result['Residual R-Squared'] = [response['residual-r-squared']]			

							if 'residual-log-likelihood' in response:
								result['Residual Log-Likelihood Per Sample'] = [response['residual-log-likelihood']]

							if 'residual-rmse' in response:
								result['Residual RMSE'] = [response['residual-rmse']]

						result = pd.DataFrame.from_dict(result)

						return result

				except:
					return None

		if api_response.status_code != requests.codes.ok:
			try:
				response = api_response.json()
				if 'message' in response:
					logging.error('\n%s' % response['message'])
			except:
				logging.error('\nModel-driven improvability failed. Last HTTP code: %s' % api_response.status_code)

	return None




