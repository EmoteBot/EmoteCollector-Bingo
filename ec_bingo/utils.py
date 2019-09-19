# SPDX-License-Identifer: BlueOak-1.0.0

def scale_resolution(old_res, new_res):
	"""Resize a resolution, preserving aspect ratio. Returned w,h will be <= new_res"""
	# https://stackoverflow.com/a/6565988

	old_width, old_height = old_res
	new_width, new_height = new_res

	old_ratio = old_width / old_height
	new_ratio = new_width / new_height
	if new_ratio > old_ratio:
		return (old_width * new_height//old_height, new_height)
	return new_width, old_height * new_width//old_width
