import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class GestureRecognizer:
    def __init__(self, model_path, num_hands=1, min_hand_detection_confidence=0.5,
                 min_hand_presence_confidence=0.5, min_tracking_confidence=0.5):
        """Initialize the GestureRecognizer with model and configurations."""
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_hands=num_hands,
            min_hand_detection_confidence=min_hand_detection_confidence,
            min_hand_presence_confidence=min_hand_presence_confidence,
            min_tracking_confidence=min_tracking_confidence,
            result_callback=self.save_result  # Linking the result callback
        )
        self.recognizer = vision.GestureRecognizer.create_from_options(options)
        self.recognition_result_list = []

    def save_result(self, result: vision.GestureRecognizerResult, unused_output_image: mp.Image, timestamp_ms: int):
        """Save recognition results to the list."""

        self.recognition_result_list.append(result)

    def recognize_gesture(self, image: mp.Image, timestamp_ms: int):
        """Run gesture recognition asynchronously."""
        self.recognizer.recognize_async(image, timestamp_ms)

    def get_recognition_results(self):
        """Return the latest recognition result."""
        return self.recognition_result_list
