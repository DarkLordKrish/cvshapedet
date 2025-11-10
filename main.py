
import cv2 as cv
import numpy as np
capture = cv.VideoCapture(0)

while True:


    isTrue, frame = capture.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    lower_red = np.array([0,])
    blurred = cv.GaussianBlur(gray, (3, 3), cv.BORDER_DEFAULT)
    canny = cv.Canny(blurred, 50, 150, apertureSize=3)

    contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.imshow('frame', canny)
    cv.drawContours(frame,contours, -1, (255,0,0))
    ldic = {}
    for idx,contour in enumerate(contours):
        if idx == 0:
            continue
        if cv.contourArea(contour) < 1200:
            continue

        epsilon = 0.01*cv.arcLength(contour, True)
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

        cont_dict = {
            "id":idx,
            "shape":label,
            "hierarchy_shit":hierarchy[0][idx],
            "area": M['m00']
        }

        ldic[idx] = cont_dict

        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01'] / M['m00'])


            for key,val in ldic.items():
                parent_idx = int(val["hierarchy_shit"][3])
                if parent_idx != -1 and parent_idx in ldic and parent_idx in ldic and val["shape"] != ldic[val["hierarchy_shit"][3]]["shape"] and ldic[val["hierarchy_shit"][3]]["area"] > val["area"]:
                    cv.putText(frame, f"{val["shape"]} inside {ldic[val["hierarchy_shit"][3]]["shape"]}",
                               (cx, cy), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv.FILLED)
                    print(f"{val["shape"]} inside {ldic[val["hierarchy_shit"][3]]["shape"]}")
        cv.imshow('frame1', frame)


    print(ldic)
    if cv.waitKey(20) == ord('q'):
        break
capture.release()
cv.destroyAllWindows()
print(cv.__version__)