import cv2
import time


def scan_barcode():

    detector = cv2.barcode_BarcodeDetector()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Could not open camera.")
        return None

    # Try higher camera resolution
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print()
    print("========================================")
    print("GreenTill Barcode Scanner")
    print("========================================")
    print("Show the product barcode to the camera.")
    print("Press Q to cancel.")
    print()

    last_message_time = 0

    while True:

        success, frame = camera.read()

        if not success:
            print("ERROR: Could not read camera frame.")
            break

        barcode_found = None

        try:

            # ==================================================
            # METHOD 1 - ORIGINAL FRAME
            # ==================================================

            decoded_info, points, straight_code = (
                detector.detectAndDecode(frame)
            )

            if isinstance(decoded_info, str):

                if decoded_info.strip():

                    barcode_found = decoded_info.strip()

            # ==================================================
            # METHOD 2 - GRAYSCALE + UPSCALE
            # ==================================================

            if barcode_found is None:

                gray = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2GRAY
                )

                # Increase contrast
                gray = cv2.equalizeHist(gray)

                # Make barcode larger
                enlarged = cv2.resize(
                    gray,
                    None,
                    fx=1.5,
                    fy=1.5,
                    interpolation=cv2.INTER_CUBIC
                )

                decoded_info_2, points_2, straight_code_2 = (
                    detector.detectAndDecode(enlarged)
                )

                if isinstance(decoded_info_2, str):

                    if decoded_info_2.strip():

                        barcode_found = (
                            decoded_info_2.strip()
                        )

            # ==================================================
            # BARCODE FOUND
            # ==================================================

            if barcode_found:

                print()
                print("========================================")
                print("BARCODE DETECTED!")
                print("Barcode:", barcode_found)
                print("========================================")

                cv2.putText(
                    frame,
                    "Barcode Detected!",
                    (30, 45),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 255, 0),
                    3
                )

                cv2.putText(
                    frame,
                    barcode_found,
                    (30, 85),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2
                )

                cv2.imshow(
                    "GreenTill Barcode Scanner",
                    frame
                )

                cv2.waitKey(1200)

                camera.release()
                cv2.destroyAllWindows()

                return barcode_found

        except Exception as error:

            # Don't continuously print the same error
            current_time = time.time()

            if current_time - last_message_time > 2:

                print(
                    "Scanner processing error:",
                    error
                )

                last_message_time = current_time

        # ======================================================
        # CAMERA INSTRUCTIONS
        # ======================================================

        cv2.rectangle(
            frame,
            (50, 130),
            (1230, 600),
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Place the PRODUCT BARCODE inside the box",
            (70, 175),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Move closer or farther until the barcode is clear",
            (70, 210),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Press Q to cancel",
            (70, 250),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "GreenTill Barcode Scanner",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):

            break

    camera.release()
    cv2.destroyAllWindows()

    return None


if __name__ == "__main__":

    barcode = scan_barcode()

    if barcode:

        print()
        print("FINAL BARCODE:", barcode)

    else:

        print()
        print("No barcode detected.")