"""
Gesture VLC program allows you to control a media player using hand gestures.

The program uses the Mediapipe Module to track a single hand, and executes the functions through keyboard presses using PyAutoGUI

For the program to work, ensure that the Media Player is running in the foreground.
Press the 'Esc' key with the Hand Tracking Window open in the foreground to Quit the Program.

Gestures:
You must first Activate Gesture Recognition using Open Hand before making Gestures.

1. Open Hand: Gesture Recognition Active
2. Closed Fist: Pause/Play
3. 1 Finger Open (Swipe Horizontally): Skip Forward/Backward
4. 2 Finger Open (Swipe Vertically): Volume Increase/Decrease
5. 3 Finger Open: Mute
6. Rock Sign: Close Program

"""

#Import Libraries
import cv2
import pyautogui as pag
import EZopencv as ez


#Intialize Instances
cap = cv2.VideoCapture(0)
HandTrack = ez.HandTracking()
init = False


#Main Loop
while True:
	status, img = cap.read()
	img_h, img_w, _ = img.shape

	img, points = HandTrack.Track(img, flip_image=True, hand_type=True)

	if points and points[21] == "Right":
		index_tip, index_upper, index_bottom = points[8], points[7], points[5]
		middle_tip, middle_upper, middle_bottom = points[12], points[11], points[9]
		ring_tip, ring_upper, ring_bottom = points[16], points[15], points[13]
		pinky_tip, pinky_upper, pinky_bottom = points[20], points[19], points[17]
		wrist = points[0]

		if init == True:

			if (index_tip[2] > index_upper[2]) and (middle_tip[2] > middle_upper[2]) and (ring_tip[2] > ring_upper[2]) and (pinky_tip[2] > pinky_upper[2]):
				print("Play/Pause")
				pag.press('space')
				init = False

			elif (index_tip[2] < index_upper[2]) and (middle_tip[2] < middle_upper[2]) and (ring_tip[2] < ring_upper[2]) and (pinky_tip[2] > pinky_upper[2]):
				print("Mute")
				pag.press('m')
				init = False
			
			elif (index_tip[2] < index_upper[2]) and (middle_tip[2] > middle_upper[2]) and (ring_tip[2] > ring_upper[2]) and (pinky_tip[2] < pinky_upper[2]):
				print("Close Program")
				break

			elif (index_tip[2] < index_upper[2]) and (middle_tip[2] < middle_upper[2]) and (ring_tip[2] > ring_upper[2]) and (pinky_tip[2] > pinky_upper[2]):
				if (index_tip[2] > 0) and (middle_tip[2] > 0) and (index_tip[2]*1.05 < previous_index_tip[2]) and (middle_tip[2]*1.05 < previous_index_tip[2]):
					print("Volume Up")
					pag.press('up')
					previous_index_tip = index_tip

				elif (wrist[2] < img_h) and (index_tip[2] > previous_index_tip[2]*1.05) and (middle_tip[2] > previous_index_tip[2]*1.05):
					print("Volume Down")
					pag.press('down')
					previous_index_tip = index_tip

			elif (index_tip[2] < index_upper[2]) and (middle_tip[2] > middle_upper[2]) and (ring_tip[2] > ring_upper[2]) and (pinky_tip[2] > pinky_upper[2]):
				if (index_tip[1] > 0) and (index_tip[1] > previous_index_tip[1]*1.1):
					print("Skip Forward")
					pag.hotkey('shift', 'right')
					previous_index_tip = index_tip

				elif (pinky_upper[1] < img_w) and (index_tip[1]*1.1 < previous_index_tip[1]):
					print("Skip Backward")
					pag.hotkey('shift', 'left')
					previous_index_tip = index_tip


		elif (index_tip[2] < index_upper[2]) and (middle_tip[2] < middle_upper[2]) and (ring_tip[2] < ring_upper[2]) and (pinky_tip[2] < pinky_upper[2]):
			print("Gesture Recognition Activated")
			init = True
			previous_index_tip, previous_middle_tip = index_tip, middle_tip

	else:
		init=False

	cv2.imshow("Hand Tracking", img)

	if cv2.waitKey(1) & 0xFF == 27:
		break