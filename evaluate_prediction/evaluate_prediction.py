# evaluate_prediction(2, 4, 2, 4) # 10, awesome prediction
# evaluate_prediction(5, 4, 2, 1) # 5, fair prediction
# evaluate_prediction(3, 8, 9, 1) # 0, poor prediction


def evaluate_prediction(predicted_t1, predicted_t2, actual_t1, actual_t2):
	if predicted_t1 == actual_t1 and predicted_t2 == actual_t2:
		return 10

	predicted_t1_win = predicted_t1 >= predicted_t2
	actual_t1_win = actual_t1 >= actual_t2
	if predicted_t1_win == actual_t1_win:
		return 5

	return 0


assert evaluate_prediction(2, 4, 2, 4) == 10
assert evaluate_prediction(5, 4, 2, 1) == 5
assert evaluate_prediction(3, 8, 9, 1) == 0
assert evaluate_prediction(3, 0, 2, 3) == 0
