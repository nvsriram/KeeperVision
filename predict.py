import cv2
from ultralytics import YOLO


class KeeperVisionModel:
    GP_MODEL_PATH = "./models/yolov8m_custom.pt"
    GK_MODEL_PATH = "./models/yolov8m.pt"
    FB_POS = 0.8
    FB_THRESHOLD = 0.2
    LR_THRESHOLD = 0.35

    def __init__(self):
        self.gp_model = YOLO(self.GP_MODEL_PATH)
        self.gk_model = YOLO(self.GK_MODEL_PATH)

    def get_idx(self, lr, fb):
        # F :1
        # B :2
        # L :3
        # LF:4
        # LB:5
        # R :6
        # RF:7
        # RB:8
        return lr * 3 + fb

    def get_bounding_box(self, results):
        if len(results) != 1:
            print("len", len(results))
            print(results)
        boxes = results[0].boxes
        sorted_boxes = sorted(boxes, key=lambda x: x.conf[0].item(), reverse=True)
        print("sorted boxes:", len(sorted_boxes), sorted_boxes)
        return sorted_boxes[0]

    def draw_bounding_boxes(self, img, bbs):
        for bb in bbs:
            box = bb.xyxy[0].cpu().numpy()
            x_min, y_min, x_max, y_max = box[:4]

            # bounding box
            color = (0, 0, 255)
            thickness = 2
            cv2.rectangle(
                img,
                (int(x_min), int(y_min)),
                (int(x_max), int(y_max)),
                color,
                thickness,
            )

            # confidence score
            text = f"{bb.conf[0].item():.2f}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            text_color = (255, 255, 255)
            text_thickness = 1
            (text_width, text_height), _ = cv2.getTextSize(
                text, font, font_scale, text_thickness
            )
            background_x_max = int(x_min + text_width + 6)
            background_y_max = int(y_min + text_height + 6)
            cv2.rectangle(
                img,
                (int(x_min), int(y_min)),
                (background_x_max, background_y_max),
                (0, 0, 255),
                -1,
            )
            cv2.putText(
                img,
                text,
                (int(x_min) + 3, int(y_min) + text_height + 3),
                font,
                font_scale,
                text_color,
                text_thickness,
            )

        return img

    def predict_executor(self, image, is_gk):
        model = self.gk_model if is_gk else self.gp_model
        results = model.predict(
            source=image,
            save=True,
            save_conf=True,
            save_txt=True,
            conf=0.5,
            max_det=1,
        )
        return self.get_bounding_box(results)

    def get_prediction(self, image):
        img = cv2.imread(image)
        scale_factor = 0.3
        img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor)

        gp_bb = self.predict_executor(img, False)
        gk_bb = self.predict_executor(img, True)

        bb_img = self.draw_bounding_boxes(img, [gp_bb, gk_bb])
        cv2.imshow("Bounding Boxes", bb_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        lwidth = gk_bb.xyxyn[0][0] - gp_bb.xyxyn[0][0]
        rwidth = gp_bb.xyxyn[0][2] - gk_bb.xyxyn[0][2]

        lr = fb = 0
        width_ratio = lwidth / rwidth
        if width_ratio < (1 - self.LR_THRESHOLD) or width_ratio > (
            1 + self.LR_THRESHOLD
        ):
            # invert directions for goalkeeper's perspective
            if lwidth < rwidth:
                print("Left")
                lr = 1
            else:
                print("Right")
                lr = 2

        height_ratio = gk_bb.xywhn[0][3] / gp_bb.xywhn[0][3]
        if height_ratio < (self.FB_POS - self.FB_THRESHOLD) or height_ratio > (
            self.FB_POS + self.FB_THRESHOLD
        ):
            if height_ratio < self.FB_POS:
                print("Forward")
                fb = 1
            else:
                print("Back")
                fb = 2

        print(f"Done - width: {width_ratio}; height: {height_ratio}")

        return self.get_idx(lr, fb), str(width_ratio), str(height_ratio)
