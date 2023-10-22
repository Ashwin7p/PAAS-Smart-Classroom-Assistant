import face_recognition
import pickle
import numpy as np

class FaceEncodingsLoader:
    def __init__(self, encoding_file):
        self.encodings = self.load_encodings(encoding_file)

    def load_encodings(self, filename):
        try:
            with open(filename, "rb") as file:
                encodings = pickle.load(file)
            return encodings
        except Exception as e:
            raise ValueError(f"Failed to load encodings from {filename}: {str(e)}")

    def get_encodings(self):
        return self.encodings

    def find_best_match(self, known_encodings, unknown_image_path,names, threshold=0.6):
        """
        Compares an unknown face image to a list of known face encodings and returns the best match.
        
        :param known_encodings: List of known face encodings (numpy arrays).
        :param unknown_image_path: Path to the unknown image for comparison.
        :param threshold: Similarity threshold for considering a match (default is 0.6).
        :return: Name or identifier of the best match, or None if no match is found.
        """
        # Load the unknown image
        print(unknown_image_path)
        unknown_image = face_recognition.load_image_file(unknown_image_path)

        # Encode the faces in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        unknown_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        # unknown_encodings = face_recognition.face_encodings(unknown_image)

        if not unknown_encodings:
            return None  # No faces found in the unknown image.

        # Compare the unknown face encodings to the list of known encodings
        matches = face_recognition.compare_faces(known_encodings, unknown_encodings[0], tolerance=threshold)

        face_distances = face_recognition.face_distance(known_encodings, unknown_encodings[0])
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = names[best_match_index]
            return name
        else:
            return "unknown face"
        





if __name__ == "__main__":
    encoding_file = "encoding"  # Replace with the path to your encoding file
    encodings_loader = FaceEncodingsLoader(encoding_file)
    
    # Get the loaded encodings
    loaded_encodings = encodings_loader.get_encodings()
    img_path = "exp/0001.jpg"
    results  = encodings_loader.find_best_match(loaded_encodings["encoding"],img_path,loaded_encodings["name"])
    print(results)

    
    # find_best_match(loaded_encodings["encoding"],img_path)
    # # Print the loaded encodings
    # for name, encoding in loaded_encodings.items():
    #     print(f"Name: {name}")
    #     print(f"Face Encoding: {encoding}")

