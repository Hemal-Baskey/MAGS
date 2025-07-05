import cv2
import numpy as np
import utils

########################################################################
# Webcam feed code removed
#pathImage = "D:/My_Project/mags-main/omr_img1.jpg"
pathImage = "omr_img1.jpg"

heightImg = 350
widthImg = 300
questions = 5
choices = 5
ans = [1, 2, 0, 2, 3]
########################################################################

count = 0

while True:
    img = cv2.imread(pathImage)
    if img is None:
        print(f"Error: Could not load image from {pathImage}")
        break
    print("Image loaded successfully")
    img = cv2.resize(img, (widthImg, heightImg))
    imgFinal = img.copy()
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 10, 50)
    imgThresh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 1)

    try:
        imgContours = img.copy()
        imgBigContour = img.copy()
        contours1, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours1 + contours2
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 2)
        rectCon = utils.rectContour(contours)
        if len(rectCon) < 2:
            print("Error: Not enough rectangle contours found")
            imageArray = ([img, imgGray, imgCanny, imgContours],
                         [imgThresh, imgBlank, imgBlank, imgBlank])
            stackedImage = utils.stackImages(imageArray, 0.5, [["Original", "Gray", "Edges", "Contours"],
                                                             ["Threshold", "Blank", "Blank", "Blank"]])
            cv2.imshow("Result", stackedImage)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
        biggestPoints = utils.getCornerPoints(rectCon[0])
        gradePoints = utils.getCornerPoints(rectCon[1])
        if biggestPoints.size != 0 and gradePoints.size != 0:
            biggestPoints = utils.reorder(biggestPoints)
            cv2.drawContours(imgBigContour, biggestPoints, -1, (0, 255, 0), 20)
            pts1 = np.float32(biggestPoints)
            pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
            cv2.drawContours(imgBigContour, gradePoints, -1, (255, 0, 0), 20)
            gradePoints = utils.reorder(gradePoints)
            ptsG1 = np.float32(gradePoints)
            ptsG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])
            matrixG = cv2.getPerspectiveTransform(ptsG1, ptsG2)
            imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150))
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(imgWarpGray, 120, 255, cv2.THRESH_BINARY_INV)[1]
            boxes = utils.splitBoxes(imgThresh)
            countR = 0
            countC = 0
            myPixelVal = np.zeros((questions, choices))
            for image in boxes:
                totalPixels = cv2.countNonZero(image)
                myPixelVal[countR][countC] = totalPixels
                countC += 1
                if (countC == choices): countC = 0;countR += 1
            myIndex = []
            for x in range(0, questions):
                arr = myPixelVal[x]
                myIndexVal = np.where(arr == np.amax(arr))
                myIndex.append(myIndexVal[0][0])
            grading = []
            for x in range(0, questions):
                if ans[x] == myIndex[x]:
                    grading.append(1)
                else:
                    grading.append(0)
            score = (sum(grading) / questions) * 100
            utils.showAnswers(imgWarpColored, myIndex, grading, ans)
            utils.drawGrid(imgWarpColored)
            imgRawDrawings = np.zeros_like(imgWarpColored)
            utils.showAnswers(imgRawDrawings, myIndex, grading, ans)
            invMatrix = cv2.getPerspectiveTransform(pts2, pts1)
            imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (widthImg, heightImg))
            imgRawGrade = np.zeros_like(imgGradeDisplay, np.uint8)
            cv2.putText(imgRawGrade, str(int(score)) + "%", (70, 100)
                        , cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 255), 3)
            invMatrixG = cv2.getPerspectiveTransform(ptsG2, ptsG1)
            imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg, heightImg))
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1, 0)
            imageArray = ([img, imgGray, imgCanny, imgContours],
                          [imgBigContour, imgThresh, imgWarpColored, imgFinal])
            cv2.imshow("Final Result", imgFinal)
    except:
        imageArray = ([img, imgGray, imgCanny, imgContours],
                      [imgBlank, imgBlank, imgBlank, imgBlank])
    lables = [["Original", "Gray", "Edges", "Contours"],
              ["Biggest Contour", "Threshold", "Warped", "Final"]]
    cv2.namedWindow("OMR Scanner Results", cv2.WINDOW_NORMAL)
    window_width = 1600
    window_height = 1000
    cv2.resizeWindow("OMR Scanner Results", window_width, window_height)
    canvas = np.full((window_height, window_width, 3), 240, dtype=np.uint8)
    img_width = window_width // 4
    img_height = window_height // 2
    font_scale = 1.0
    font_thickness = 2
    font_color = (0, 0, 0)
    font = cv2.FONT_HERSHEY_COMPLEX
    for i in range(2):
        for j in range(4):
            current_img = imageArray[i][j]
            if len(current_img.shape) == 2:
                current_img = cv2.cvtColor(current_img, cv2.COLOR_GRAY2BGR)
            x1 = j * img_width
            y1 = i * img_height
            x2 = (j + 1) * img_width
            y2 = (i + 1) * img_height
            h, w = current_img.shape[:2]
            scale = min((img_width-40)/w, (img_height-80)/h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            resized_img = cv2.resize(current_img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            x_offset = x1 + (img_width - new_w) // 2
            y_offset = y1 + (img_height - new_h) // 2 + 20
            cv2.rectangle(canvas, (x_offset-5, y_offset-5), 
                         (x_offset+new_w+5, y_offset+new_h+5), (255, 255, 255), -1)
            canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_img
            cv2.rectangle(canvas, (x1, y1), (x2, y2), (220, 220, 220), 2)
            label = lables[i][j]
            text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
            text_x = x1 + (img_width - text_size[0]) // 2
            text_y = y1 + 45
            padding = 10
            cv2.rectangle(canvas, 
                         (text_x - padding, text_y - text_size[1] - padding),
                         (text_x + text_size[0] + padding, text_y + padding),
                         (255, 255, 255), -1)
            cv2.putText(canvas, label, (text_x+2, text_y+2), 
                       font, font_scale, (200, 200, 200), font_thickness, cv2.LINE_AA)
            cv2.putText(canvas, label, (text_x, text_y), 
                       font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    cv2.imshow("OMR Scanner Results", canvas)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        cv2.imwrite("Scanned/myImage" + str(count) + ".jpg", imgFinal)
        save_msg_x = int(window_width / 2) - 100
        save_msg_y = int(window_height / 2)
        cv2.rectangle(canvas, (save_msg_x - 20, save_msg_y - 30),
                     (save_msg_x + 200, save_msg_y + 30), (0, 255, 0), cv2.FILLED)
        cv2.putText(canvas, "Scan Saved", (save_msg_x, save_msg_y),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow('OMR Scanner Results', canvas)
        count += 1
    elif key == ord('q'):
        break
cv2.destroyAllWindows()
        