# 👁️ Computer Vision - Key Concepts

## 🎯 **Real-World Analogy: The Digital Eye with Brain**

> **Think of computer vision as giving machines the ability to see and understand images like humans do, but with superhuman precision and speed. It's like having a detective who can instantly analyze thousands of photos and spot patterns invisible to the human eye.**

## 🔥 **Core Concepts**

### 1. **Image Processing Fundamentals** 📸

```python
import cv2
import numpy as np
from PIL import Image

class ImageProcessor:
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp']
    
    def load_image(self, image_path):
        """Load and validate image"""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        return image
    
    def preprocess_image(self, image, target_size=(224, 224)):
        """Standard preprocessing for ML models"""
        # Resize
        resized = cv2.resize(image, target_size)
        
        # Normalize pixel values to [0, 1]
        normalized = resized.astype(np.float32) / 255.0
        
        # Convert BGR to RGB (OpenCV uses BGR by default)
        rgb_image = cv2.cvtColor(normalized, cv2.COLOR_BGR2RGB)
        
        return rgb_image
    
    def enhance_image(self, image):
        """Basic image enhancement"""
        # Convert to LAB color space for better enhancement
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        
        # Convert back to BGR
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return enhanced

# Usage
processor = ImageProcessor()
image = processor.load_image("sample.jpg")
processed = processor.preprocess_image(image)
enhanced = processor.enhance_image(image)
```

### 2. **Object Detection** 🎯

```python
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image

class ObjectDetector:
    def __init__(self):
        self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
        self.model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    
    def detect_objects(self, image_path, confidence_threshold=0.9):
        """Detect objects in image"""
        image = Image.open(image_path)
        
        # Process image
        inputs = self.processor(images=image, return_tensors="pt")
        
        # Run inference
        outputs = self.model(**inputs)
        
        # Convert outputs to COCO API format
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.processor.post_process_object_detection(
            outputs, target_sizes=target_sizes, threshold=confidence_threshold
        )[0]
        
        # Extract detections
        detections = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            detections.append({
                "label": self.model.config.id2label[label.item()],
                "confidence": score.item(),
                "bbox": box.tolist(),  # [x_min, y_min, x_max, y_max]
            })
        
        return detections
    
    def batch_detect(self, image_paths):
        """Process multiple images"""
        all_detections = {}
        for path in image_paths:
            try:
                detections = self.detect_objects(path)
                all_detections[path] = detections
            except Exception as e:
                all_detections[path] = {"error": str(e)}
        
        return all_detections

# Usage
detector = ObjectDetector()
detections = detector.detect_objects("street_scene.jpg")

for detection in detections:
    print(f"Found {detection['label']} with {detection['confidence']:.2f} confidence")
```

### 3. **Image Classification** 🏷️

```python
from transformers import ViTImageProcessor, ViTForImageClassification
import torch

class ImageClassifier:
    def __init__(self, model_name="google/vit-base-patch16-224"):
        self.processor = ViTImageProcessor.from_pretrained(model_name)
        self.model = ViTForImageClassification.from_pretrained(model_name)
    
    def classify_image(self, image_path, top_k=5):
        """Classify image and return top predictions"""
        image = Image.open(image_path)
        
        # Process image
        inputs = self.processor(images=image, return_tensors="pt")
        
        # Run inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits[0], dim=-1)
        
        # Get top-k predictions
        top_predictions = torch.topk(predictions, top_k)
        
        results = []
        for i in range(top_k):
            idx = top_predictions.indices[i].item()
            confidence = top_predictions.values[i].item()
            label = self.model.config.id2label[idx]
            
            results.append({
                "label": label,
                "confidence": confidence
            })
        
        return results
    
    def classify_batch(self, image_paths):
        """Classify multiple images efficiently"""
        images = [Image.open(path) for path in image_paths]
        
        # Process batch
        inputs = self.processor(images=images, return_tensors="pt")
        
        # Run batch inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Process results
        batch_results = []
        for i, path in enumerate(image_paths):
            top_pred = torch.topk(predictions[i], 1)
            idx = top_pred.indices[0].item()
            confidence = top_pred.values[0].item()
            label = self.model.config.id2label[idx]
            
            batch_results.append({
                "image_path": path,
                "label": label,
                "confidence": confidence
            })
        
        return batch_results

# Usage
classifier = ImageClassifier()
results = classifier.classify_image("dog.jpg", top_k=3)

for result in results:
    print(f"{result['label']}: {result['confidence']:.3f}")
```

### 4. **Face Detection & Recognition** 👤

```python
import face_recognition
import cv2
import numpy as np

class FaceProcessor:
    def __init__(self):
        self.known_faces = {}
        self.face_encodings = {}
    
    def detect_faces(self, image_path):
        """Detect all faces in image"""
        image = face_recognition.load_image_file(image_path)
        
        # Find face locations
        face_locations = face_recognition.face_locations(image)
        
        # Get face encodings
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        faces = []
        for i, (encoding, location) in enumerate(zip(face_encodings, face_locations)):
            faces.append({
                "face_id": i,
                "location": location,  # (top, right, bottom, left)
                "encoding": encoding
            })
        
        return faces
    
    def add_known_face(self, name, image_path):
        """Add a known face for recognition"""
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        
        if encodings:
            self.known_faces[name] = encodings[0]
            return True
        return False
    
    def recognize_faces(self, image_path, tolerance=0.6):
        """Recognize faces in image"""
        faces = self.detect_faces(image_path)
        
        recognized_faces = []
        for face in faces:
            face_encoding = face["encoding"]
            
            # Compare with known faces
            matches = face_recognition.compare_faces(
                list(self.known_faces.values()),
                face_encoding,
                tolerance=tolerance
            )
            
            name = "Unknown"
            confidence = 0.0
            
            if True in matches:
                # Find best match
                face_distances = face_recognition.face_distance(
                    list(self.known_faces.values()),
                    face_encoding
                )
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = list(self.known_faces.keys())[best_match_index]
                    confidence = 1 - face_distances[best_match_index]
            
            recognized_faces.append({
                "name": name,
                "confidence": confidence,
                "location": face["location"]
            })
        
        return recognized_faces

# Usage
face_processor = FaceProcessor()

# Add known faces
face_processor.add_known_face("Alice", "alice.jpg")
face_processor.add_known_face("Bob", "bob.jpg")

# Recognize faces in new image
results = face_processor.recognize_faces("group_photo.jpg")

for result in results:
    print(f"Found {result['name']} with {result['confidence']:.2f} confidence")
```

## 🚀 **Advanced Applications**

### **Document Analysis** 📄

```python
import easyocr
import cv2
import numpy as np

class DocumentAnalyzer:
    def __init__(self):
        self.ocr_reader = easyocr.Reader(['en'])
    
    def extract_text(self, image_path):
        """Extract text from document image"""
        results = self.ocr_reader.readtext(image_path)
        
        extracted_text = []
        for (bbox, text, confidence) in results:
            if confidence > 0.5:  # Filter low-confidence detections
                extracted_text.append({
                    "text": text,
                    "confidence": confidence,
                    "bbox": bbox
                })
        
        return extracted_text
    
    def detect_document_structure(self, image_path):
        """Detect document structure (headers, paragraphs, etc.)"""
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect horizontal lines (potential separators)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        horizontal_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, horizontal_kernel)
        
        # Detect vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        vertical_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, vertical_kernel)
        
        # Find contours for text blocks
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        text_blocks = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 50 and h > 20:  # Filter small noise
                text_blocks.append({
                    "bbox": (x, y, w, h),
                    "area": w * h
                })
        
        return {
            "text_blocks": text_blocks,
            "has_tables": len(horizontal_lines) > 0 and len(vertical_lines) > 0
        }

# Usage
doc_analyzer = DocumentAnalyzer()
text_results = doc_analyzer.extract_text("invoice.jpg")
structure = doc_analyzer.detect_document_structure("invoice.jpg")

print(f"Extracted {len(text_results)} text elements")
print(f"Document has tables: {structure['has_tables']}")
```

### **Video Analysis** 🎬

```python
import cv2
from collections import deque

class VideoAnalyzer:
    def __init__(self):
        self.frame_buffer = deque(maxlen=30)  # Keep last 30 frames
    
    def analyze_video(self, video_path, sample_rate=30):
        """Analyze video and extract key information"""
        cap = cv2.VideoCapture(video_path)
        
        frame_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        analysis_results = {
            "duration": total_frames / fps,
            "fps": fps,
            "total_frames": total_frames,
            "key_frames": [],
            "motion_analysis": []
        }
        
        prev_frame = None
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Sample frames at specified rate
            if frame_count % sample_rate == 0:
                # Motion detection
                if prev_frame is not None:
                    motion_score = self.calculate_motion(prev_frame, frame)
                    analysis_results["motion_analysis"].append({
                        "frame": frame_count,
                        "timestamp": frame_count / fps,
                        "motion_score": motion_score
                    })
                
                # Store key frame info
                analysis_results["key_frames"].append({
                    "frame_number": frame_count,
                    "timestamp": frame_count / fps
                })
                
                prev_frame = frame.copy()
            
            frame_count += 1
        
        cap.release()
        return analysis_results
    
    def calculate_motion(self, frame1, frame2):
        """Calculate motion between two frames"""
        # Convert to grayscale
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Calculate absolute difference
        diff = cv2.absdiff(gray1, gray2)
        
        # Calculate motion score as percentage of changed pixels
        motion_score = np.sum(diff > 30) / (diff.shape[0] * diff.shape[1])
        return motion_score
    
    def extract_frames(self, video_path, output_dir, interval_seconds=1):
        """Extract frames at regular intervals"""
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval_seconds)
        
        frame_count = 0
        saved_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                output_path = f"{output_dir}/frame_{saved_count:06d}.jpg"
                cv2.imwrite(output_path, frame)
                saved_count += 1
            
            frame_count += 1
        
        cap.release()
        return saved_count

# Usage
video_analyzer = VideoAnalyzer()
results = video_analyzer.analyze_video("sample_video.mp4", sample_rate=30)

print(f"Video duration: {results['duration']:.2f} seconds")
print(f"Average motion score: {np.mean([m['motion_score'] for m in results['motion_analysis']]):.3f}")
```