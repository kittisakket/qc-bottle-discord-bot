from ultralytics import YOLO
import cv2
import os
import requests
import gc



model_path = "model.pt"
model_url = "https://drive.google.com/uc?export=download&id=1YopjpBNiPrvNtDq4tWLWyOjnEj7UJD1r"  # <== เปลี่ยนตรงนี้สำหรับการแนบ url ของ model

if not os.path.exists(model_path):
    print("Downloading model.pt...")
    r = requests.get(model_url)
    with open(model_path, 'wb') as f:
        f.write(r.content)
    print("Downloaded model.pt ✅")

model = YOLO(model_path)


def process_image(image_path):
    try:
        img = cv2.imread(image_path)
        results = model(img)

        summary = {}
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            labels = result.boxes.cls.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()

            for box, label, conf in zip(boxes, labels, confidences):
                x1, y1, x2, y2 = map(int, box)
                class_name = model.names[int(label)]
                summary[class_name] = summary.get(class_name, 0) + 1

                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, f'{class_name} {{conf:.0%}}'.format(conf=conf),
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        output_path = 'static/output.jpg'
        cv2.imwrite(output_path, img)

        # Clear memory
        del img, results, boxes, labels, confidences
        gc.collect()

        return output_path, summary

    except Exception as e:
        print(f"❌ Error during image processing: {e}")
        return None, {"error": str(e)}

