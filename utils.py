from ultralytics import YOLO
import cv2

model = YOLO('model.pt')

def process_image(image_path):
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
            cv2.putText(img, f'{class_name} {conf:.0%}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    output_path = 'static/output.jpg'
    cv2.imwrite(output_path, img)
    return output_path, summary
