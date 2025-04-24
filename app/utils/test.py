

import cv2
import pandas as pd
from pyzbar.pyzbar import decode

def start_qr_code_scan():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Camera not found!")
        return None
    print("Scanning for QR code. Please hold the code in front of the camera.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        decoded_objects = decode(frame)

        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f"QR Code detected: {qr_data}")

            # Close the camera after reading the QR code
            cap.release()
            cv2.destroyAllWindows()
            return qr_data  
        
        cv2.imshow("QR Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None 

def check_qr_in_ticket_csv(scanned_qr):
    try:
        df = pd.read_csv("tickets.csv")
        if 'QR Image Path' in df.columns:
            matching_ticket = df[df['QR Image Path'] == scanned_qr]

            if not matching_ticket.empty:
                print("QR Code matches a ticket in the system!")
                return True
            else:
                print("No matching ticket found for this QR code.")
                return False
        else:
            print("QR Image Path column not found in tickets.csv.")
            return False

    except FileNotFoundError:
        print("Error: tickets.csv not found.")
        return False


if __name__ == "__main__":
    qr_code_data = start_qr_code_scan()

    if qr_code_data:
        # Check if the scanned QR code exists in the tickets.csv file
        if check_qr_in_ticket_csv(qr_code_data):
            print("You are all set! Ticket validated.")
        else:
            print("Ticket validation failed.")
    else:
        print("QR code scanning failed.")

