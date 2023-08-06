#!/usr/bin/env python
# -*- coding: utf-8 -*-



def approx_opt_remaining_time(step):
	"""
	Estimate the amount of time left for the API to finish a task that requires maximum-entropy optimization.


	Parameters
	----------
	step: int
		A string that uniquely identifies the content of the file.

	Returns
	-------
	remaining_time : str
		The approximate remaining duration.
	"""
	elapsed_time = 12*step
	total_time = 10 if step < 1 else 60*5 if step <= 25 else 60*10 if step <= 50 else 60*20
	remaining_time = max(total_time-elapsed_time, 0)

	if step == 100:
		remaining_time = 0

	remaining_time = str(remaining_time) + 's   ' if remaining_time < 60 else str(remaining_time//60) + 'min '

	return remaining_time





