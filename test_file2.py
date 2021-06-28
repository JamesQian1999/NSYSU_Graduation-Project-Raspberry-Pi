import picamera, requests, cv2

c = cv2.VideoCapture(0)
c.set(cv2.CAP_PROP_FRAME_WIDTH,1024)
c.set(cv2.CAP_PROP_FRAME_HEIGHT,768)


while True:
    ret, frame = c.read()
    cv2.imshow("preview",frame)
    if(cv2.waitKey(1) & 0xFF == ord("q")):
        break

c.release()
cv2.destroyAllWindows()