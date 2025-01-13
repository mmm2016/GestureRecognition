import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


class VideDraw():
    def __init__(self):
        self.label_text_color = (255, 255, 255)  # white
        self.label_font_size = 1
        self.label_thickness = 2

    def draw_result(self, current_frame, recognition_result_list):
        if recognition_result_list:
            # Draw landmarks and write the text for each hand.
            for hand_index, hand_landmarks in enumerate(
                    recognition_result_list[0].hand_landmarks):
                # Calculate the bounding box of the hand
                x_min = min([landmark.x for landmark in hand_landmarks])
                y_min = min([landmark.y for landmark in hand_landmarks])
                y_max = max([landmark.y for landmark in hand_landmarks])

                # Convert normalized coordinates to pixel values
                frame_height, frame_width = current_frame.shape[:2]
                x_min_px = int(x_min * frame_width)
                y_min_px = int(y_min * frame_height)
                y_max_px = int(y_max * frame_height)

                # Get gesture classification results
                if recognition_result_list[0].gestures:
                    gesture = recognition_result_list[0].gestures[hand_index]
                    category_name = gesture[0].category_name
                    score = round(gesture[0].score, 2)
                    result_text = f'{category_name} ({score})'

                    # Compute text size
                    text_size = \
                        cv2.getTextSize(result_text, cv2.FONT_HERSHEY_DUPLEX, self.label_font_size,
                                        self.label_thickness)[0]
                    text_width, text_height = text_size

                    # Calculate text position (above the hand)
                    text_x = x_min_px
                    text_y = y_min_px - 10  # Adjust this value as needed

                    # Make sure the text is within the frame boundaries
                    if text_y < 0:
                        text_y = y_max_px + text_height

                    # Draw the text
                    cv2.putText(current_frame, result_text, (text_x, text_y),
                                cv2.FONT_HERSHEY_DUPLEX, self.label_font_size,
                                self.label_text_color, self.label_thickness, cv2.LINE_AA)

                # Draw hand landmarks on the frame
                hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                hand_landmarks_proto.landmark.extend([
                    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y,
                                                    z=landmark.z) for landmark in
                    hand_landmarks
                ])
                mp_drawing.draw_landmarks(
                    current_frame,
                    hand_landmarks_proto,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            recognition_result_list.clear()
        return current_frame
