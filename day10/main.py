import collections
import functools
import io
import itertools
import more_itertools
import operator
import os
import re
import sys

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		machines = re.findall(r"\[(.+)\] (.*) \{(.*)\}", file.read())
	num_presses = 0
	for lights, buttons_str, joltages in machines:
		target = [True if light == "#" else False for light in lights]
		buttons = [list(map(int, re.findall(r"\d+", button_str))) for button_str in re.findall(r"\([^\)]+\)", buttons_str)]
		for curr_num_presses in range(1, len(buttons) + 1):
			for curr_buttons in map(list, itertools.combinations(buttons, curr_num_presses)):
				curr_lights = [False] * len(target)
				for button in curr_buttons:
					for connection in button:
						curr_lights[connection] ^= True
				if curr_lights == target:
					num_presses += curr_num_presses
					break
			else:
				continue
			break
	print("Part 1: {}".format(num_presses))

def foo(target, available_buttons, incrementing_buttons, button_increments, button_max_presses, button_counts, i=0):
	# print(target, available_buttons, button_counts, i)
	# if all(jolt == 0 for jolt in target):
	# 	return button_counts
	i = 0
	for j in range(1, len(target)):
		if (target[j] and target[j] < target[i]) or not target[i]:
			i = j
	# print(i, target, available_buttons, button_counts)
	if not target[i]:
		# print(i, target, button_counts)
		return button_counts
	# if i == len(target):
	# 	return None
	best_result = None
	selected_buttons = [button for button in available_buttons if button in incrementing_buttons[i]]
	remaining_buttons = [button for button in available_buttons if button not in incrementing_buttons[i]]
	for buttons in itertools.combinations_with_replacement(selected_buttons, target[i]):
	# for buttons in itertools.combinations_with_replacement(incrementing_buttons[i] & available_buttons, target[i]):
	# print(list(itertools.chain(*([button] * button_max_presses[button] for button in incrementing_buttons[i] & available_buttons))))
	# for buttons in itertools.combinations(itertools.chain(*([button] * button_max_presses[button] for button in incrementing_buttons[i] & available_buttons)), target[i]):
		new_target = list(target)
		new_counts = list(button_counts)
		for button, count in collections.Counter(buttons).items():
			# print(button, count)
			new_counts[button] = count
			for j in range(len(target)):
				new_target[j] -= count * button_increments[button][j]
		valid = True
		for j in range(len(target)):
			if new_target[j] < 0:
				valid = False
				break
		if not valid:
			continue
		# result = foo(new_target, available_buttons - incrementing_buttons[i], incrementing_buttons, button_increments, button_max_presses, new_counts, i + 1)
		result = foo(new_target, remaining_buttons, incrementing_buttons, button_increments, button_max_presses, new_counts, i + 1)
		if result:
			if not best_result or sum(result) < sum(best_result):
				best_result = result
			if sum(best_result) == max(target):
				break
	return best_result

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		machines = re.findall(r"\[(.+)\] (.*) \{(.*)\}", file.read())
	num_presses = 0
	for lights, buttons_str, joltages in machines:
		target = [int(joltage) for joltage in re.findall(r"\d+", joltages)]
		target_sum = sum(target)
		buttons = [list(map(int, re.findall(r"\d+", button_str))) for button_str in re.findall(r"\([^\)]+\)", buttons_str)]
		buttons.sort(key=len, reverse=True)
		button_increments = []
		button_sums = []
		incrementing_buttons = [set() for _ in target]
		for i, button in enumerate(buttons):
			button_increment = [0] * len(target)
			for connection in button:
				button_increment[connection] = 1
				incrementing_buttons[connection].add(i)
			button_increments.append(button_increment)
			button_sums.append(sum(button_increment))
		# print(target, button_increments, incrementing_buttons)
		button_max_presses = [min(connection_target for connection_target, connection_increment in zip(target, button_increment) if connection_increment) for button_increment in button_increments]
		# print(button_max_presses)
		available_buttons = list(range(len(buttons)))
		# for curr_num_presses in range(max(target), target_sum + 1):
		button_counts = foo(target, available_buttons, incrementing_buttons, button_increments, button_max_presses, [0] * len(buttons))
		print(button_counts)
		if not button_counts:
			print("FAILED!!!")
			break
		num_presses += sum(button_counts)
			

			# num_presses_left = curr_num_presses
			# for i in range(len(button_counts)):
			# 	button_counts[i] = min(button_max_presses[i], num_presses_left)
			# 	num_presses_left -= button_max_presses[i]
			# 	if num_presses_left <= 0:
			# 		break

		# for curr_num_presses in range(max(target), target_sum + 1):
		# 	# print(curr_num_presses)
		# 	button_counts = [0] * len(buttons)
		# 	num_presses_left = curr_num_presses
		# 	for i in range(len(button_counts)):
		# 		button_counts[i] = min(button_max_presses[i], num_presses_left)
		# 		num_presses_left -= button_max_presses[i]
		# 		if num_presses_left <= 0:
		# 			break
		# 	found = False
		# 	while not found:
		# 		if sum(count * button_sum for count, button_sum in zip(button_counts, button_sums)) == target_sum:
		# 			curr_joltages = [sum(connector_increments) for connector_increments in zip(*[[count * increment for increment in increments] for count, increments in zip(button_counts, button_increments)])]
		# 			# print(button_counts, curr_joltages)
		# 			if curr_joltages == target:
		# 				num_presses += curr_num_presses
		# 				found = True
		# 		if button_counts[-1] == curr_num_presses:
		# 			break
		# 		valid_count = False
		# 		while not valid_count:
		# 			end_count = button_counts[-1]
		# 			if end_count == curr_num_presses:
		# 				break
		# 			for i in range(2, len(buttons) + 1):
		# 				if button_counts[-i]:
		# 					button_counts[-i] -= 1
		# 					button_counts[-i + 1] += 1 + end_count
		# 					button_counts[-1] -= end_count
		# 					break
		# 			valid_count = button_counts[-i + 1] <= button_max_presses[-i + 1]
		# 		else:
		# 			continue
		# 		break
		# 	if found:
		# 		break

		# 	for curr_button_increments in map(list, itertools.combinations_with_replacement(button_increments, curr_num_presses)):
		# 		increments, sums = zip(*curr_button_increments)
		# 		if(sum(sums) != target_sum):
		# 			continue
		# 		curr_joltages = [sum(connection_joltages) for connection_joltages in zip(*increments)]
		# 		# print(curr_joltages)
		# 		if curr_joltages == target:
		# 			num_presses += curr_num_presses
		# 			print(num_presses)
		# 			break
		# 	else:
		# 		continue
		# 	break
	print("Part 2: {}".format(num_presses))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
