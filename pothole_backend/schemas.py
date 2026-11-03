from pydantic import BaseModel

class Pothole_Detection(BaseModel):
    latitude: float
    longitude: float
    confidence: float
    image_path: str
    def Detection_event(self):
        detection_event={
            "latitude": self.latitude,
            "longitude": self.longitude,
            "confidence": self.confidence,
            "image_path": self.image_path
        }
        return detection_event 
        



















def create_detection(
    conn,
    latitude,
    longitude,
    confidence,
    image_path
):
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO detections
        (
            latitude,
            longitude,
            confidence,
            image_path
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            latitude,
            longitude,
            confidence,
            image_path
        )
    )

    conn.commit()

    return cursor.lastrowid