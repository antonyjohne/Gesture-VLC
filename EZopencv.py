import numpy as np
import cv2
import mediapipe as mp
import protobuf_to_dict as ptd

#Function to Stack Multiple Scaled Windows in a single frame
def WindowStack (img_array, scale=1, priority='h'):

	rows = len(img_array)
	columns = len(img_array[0])
	initial_stack = []

	for i in range(rows):
		for j in range(columns):

			img_array[i][j] = cv2.resize(img_array[i][j], (0,0), fx=scale, fy=scale)

			if len(img_array[i][j].shape) == 2:
				img_array[i][j] = cv2.cvtColor(img_array[i][j], cv2.COLOR_GRAY2BGR)

		if (priority == 'h'):
			hrow = np.concatenate(img_array[i], axis=1)
			initial_stack.append(hrow)
			a = 0

		elif (priority == 'v'):
			vrow = np.concatenate(img_array[i], axis=0)
			initial_stack.append(vrow)
			a = 1

	final_stack = np.concatenate(initial_stack, axis=a)

	return final_stack

#Empty Functions for HSV
def nothing(x):
	pass

#HSV Trackbar that Filters and Removes image artifacts. Returns HSV Value Dictionary.
def HSVTrackbar(src, scale=0.5, show_mask=False):
	hsv_dict = {"H Min":[0,180], "H Max":[180,180], "S Min":[0,255], "S Max":[255,255], "V Min":[0,255], "V Max":[255,255]}
	hsv_vals = {}
	cv2.namedWindow("HSV Trackbar")
	cv2.resizeWindow("HSV Trackbar", 400,320)

	for key, values in hsv_dict.items():
		cv2.createTrackbar(key, "HSV Trackbar", values[0], values[1], nothing)
		
	while True:

		if isinstance(src, np.ndarray):
			img = src

		else:
			status, img = src.read()
			
		img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		for name in hsv_dict:
			hsv_vals[name] = cv2.getTrackbarPos(name, "HSV Trackbar")

		min_vals = np.array([hsv_vals["H Min"], hsv_vals["S Min"], hsv_vals["V Min"]], np.uint8)
		max_vals = np.array([hsv_vals["H Max"], hsv_vals["S Max"], hsv_vals["V Max"]], np.uint8)

		mask = cv2.inRange(img_hsv, min_vals, max_vals)

		final_img = cv2.bitwise_and(img, img, mask=mask)
		
		if show_mask:
			final_img = WindowStack([[mask, final_img]], scale=scale)

		cv2.imshow("Result", final_img)

		if cv2.waitKey(1) & 0xFF == ord("q"):
			return hsv_vals


#Hand Tracking Class that uses the Mediapipe Module. Returns Tracking Points as Dictionary.
class HandTracking:

	def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.5):
		self.static_image_mode = static_image_mode 
		self.max_num_hands = max_num_hands 
		self.min_detection_confidence = min_detection_confidence
		self.min_tracking_confidence = min_tracking_confidence
		self.mpHands = mp.solutions.hands
		self.Hands = self.mpHands.Hands(self.static_image_mode, self.max_num_hands, self.min_detection_confidence, self.min_tracking_confidence)
		self.mpDraw = mp.solutions.drawing_utils

	def Track(self, src, draw_points=True, draw_connections=True, id_num=None, flip_image=False, hand_type=False):
		if flip_image:
			src = cv2.flip(src, 1)

		self.points_list = []
		img_h, img_w, _ = src.shape
		img_rgb = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
		results = self.Hands.process(img_rgb)
		landmarks = results.multi_hand_landmarks

		if landmarks:
			landmarks_dict = ptd.protobuf_to_dict(landmarks[0])['landmark']

			if (draw_connections == True):
				self.mpDraw.draw_landmarks(src, landmarks[0], self.mpHands.HAND_CONNECTIONS)

				for i, points in enumerate(landmarks_dict):
					self.points_list.append([i, int(landmarks_dict[i]['x']*img_w), int(landmarks_dict[i]['y']*img_h)])

			elif (draw_points == True and draw_connections == False):
				self.mpDraw.draw_landmarks(src, lms)

				for i, points in enumerate(landmarks_dict):
					self.points_list.append([i, int(landmarks_dict[i]['x']*img_w), int(landmarks_dict[i]['y']*img_h)])

			else:
				for i, points in enumerate(landmarks_dict):
					self.points_list.append([i, int(landmarks_dict[i]['x']*img_w), int(landmarks_dict[i]['y']*img_h)])

			if hand_type:
				handedness = results.multi_handedness
				self.points_list.append(handedness[0].classification[0].label)

		return src, self.points_list