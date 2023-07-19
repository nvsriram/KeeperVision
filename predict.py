from ultralytics import YOLO
import cv2

GP_MODEL_PATH = "./gp_model.pt"
GK_MODEL_PATH = "./gk_model.pt"
FB_POS = 0.8
FB_THRESHOLD = 0.2
LR_THRESHOLD = 0.35


def get_idx(lr, fb):
    # F :1
    # B :2
    # L :3
    # LF:4
    # LB:5
    # R :6
    # RF:7
    # RB:8
    return lr * 3 + fb


def get_bounding_box(results):
    if len(results) > 1:
        print(results)
    boxes = results[0].boxes
    sorted_boxes = sorted(boxes, key=lambda x: x.conf, reverse=True)
    return sorted_boxes[0].xyxyn[0]


def get_prediction(image):
    gp_model = YOLO(GP_MODEL_PATH)
    gk_model = YOLO(GK_MODEL_PATH)

    img = cv2.imread(image)
    gp_results = gp_model.predict(
        source=img,
        show=True,
        conf=0.5,
        max_det=1,
    )
    gk_results = gk_model.predict(
        source=img,
        show=True,
        conf=0.5,
        max_det=1,
    )

    gp_bb = get_bounding_box(gp_results)
    gk_bb = get_bounding_box(gk_results)

    gp_height = gp_bb[3] - gp_bb[1]
    gk_height = gk_bb[3] - gk_bb[1]
    lwidth = gk_bb[0] - gp_bb[0]
    rwidth = gp_bb[2] - gk_bb[2]

    lr = fb = 0
    width_ratio = lwidth / rwidth
    if width_ratio < (1 - LR_THRESHOLD) or width_ratio > (1 + LR_THRESHOLD):
        # invert directions for goalkeeper's perspective
        if lwidth < rwidth:
            print("Left")
            lr = 1
        else:
            print("Right")
            lr = 2

    height_ratio = gk_height / gp_height
    if height_ratio < (FB_POS - FB_THRESHOLD) or height_ratio > (FB_POS + FB_THRESHOLD):
        if height_ratio < FB_POS:
            print("Forward")
            fb = 1
        else:
            print("Back")
            fb = 2

    print(f"Done - width: {width_ratio}; height: {height_ratio}")

    return get_idx(lr, fb), str(width_ratio), str(height_ratio)
