import subprocess
import time
import serial

DEVICE = "/dev/tty.usbmodem114401"  # TODO: Replace with actual path
CHECK_INTERVAL = 30  # seconds

def get_unread_mail_count():
    script = 'tell application "Mail" to unread count of inbox'
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    try:
        return int(result.stdout.strip())
    except ValueError:
        return 0

def main():
    try:
        ser = serial.Serial(DEVICE, 9600, timeout=1)
        print("Connected to ANAVI Macro Pad.")
    except serial.SerialException as e:
        print(f"Could not open serial device: {e}")
        return

    last_status = None
    while True:
        unread = get_unread_mail_count()
        status = "EMAIL" if unread > 0 else "NOEMAIL"

        if status != last_status:
            ser.write(f"{status}\n".encode())
            print(f"Sent status: {status}")
            last_status = status

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
