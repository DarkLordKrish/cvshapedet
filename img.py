import cv2 as cv
import numpy as np


from collections import Counter
frame = cv.imread("img.png")



gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

blurred = cv.GaussianBlur(gray, (3, 3), cv.BORDER_DEFAULT)
canny = cv.Canny(blurred, 50, 150, apertureSize=3)

contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cv.imshow('frame', canny)
cv.drawContours(frame, contours, -1, (255, 0, 0))

ldic = {}
for idx, contour in enumerate(contours):
    if idx == 0:
        continue
    if cv.contourArea(contour) < 1200:
        continue

    epsilon = 0.01 * cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, epsilon, True)

    M = cv.moments(approx)

    sides = len(approx)
    if sides == 3:
        label = "triangle"
    elif sides == 4:
        label = "square"
    elif sides == 5:
        label = "pentagon"
    elif sides == 6:
        label = "hexagon"
    else:
        continue

    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        mask = np.zeros(frame.shape[:2],dtype = np.uint8)
        cv.drawContours(mask,[approx],-1,255,-1)
        mean_bgr = cv.mean(frame, mask = mask)[:3]
        b,g,r = mean_bgr
        if r > b+40:
            majority_col = "red"
        elif b > r+40:
            majority_col = "blue"
        else:
            pass
        cont_dict = {
            "id": idx,
            "shape": label,
            "hierarchy_shit": hierarchy[0][idx],
            "area": M['m00'],
            "color": majority_col
        }
        ldic[idx] = cont_dict

        for key, val in ldic.items():
            parent_idx = int(val["hierarchy_shit"][3])
            if parent_idx != -1 and parent_idx in ldic and parent_idx in ldic and val["shape"] != \
                    ldic[val["hierarchy_shit"][3]]["shape"] and ldic[val["hierarchy_shit"][3]]["area"] > val[
                "area"]:
                cv.putText(frame,
                           f"{val["color"]} {val["shape"]} inside {ldic[val["hierarchy_shit"][3]]["color"]} {ldic[val["hierarchy_shit"][3]]["shape"]}",
                           (cx-300, cy), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv.FILLED)
                print(
                    f"{val["color"]} {val["shape"]} inside {ldic[val["hierarchy_shit"][3]]["color"]} {ldic[val["hierarchy_shit"][3]]["shape"]}")
    cv.imshow('frame1', frame)

print(ldic)

cv.waitKey(0)
cv.destroyAllWindows()
