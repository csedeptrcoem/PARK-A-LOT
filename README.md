# PARK-A-LOT
Aiming to develop an approach and design a framework to tackle the problem of manual monitoring of the institute entrances and parking lots by automatically tracking parking occupancies and providing alternate parking spaces along with providing automated security for vehicle entrance in institution or company campuses.

The Projec has been divided in TWO Modules : 

                                             1. Public Spaces

                                             2. Private Spaces
                                             
1) Public Spaces

  Shows available parking spaces and guides you to alternate parking spaves in case of full parking lots.

  Hardware used:

               IR Sensor 
              
               Arduino Uno
              
               Servo Motor
              
               LEDs
              
    Empty/Full Parking Spaces are shown via LEDS

    Servo Motor used for Gate

    Sensors used to detect vehicles infront of gate and in parking spaces.
    
    Check arduinocodeforhardware.txt

  Nearby Parking Spaces:

    These are shown in app. (Run NearByParking Android Application)

2) Private Spaces

  Gates open for registered vehicles of the employees by detecting the licence number off the registered car (Verifies through Database).

  Incase an employee gets a new vehicle, it can be registered in the DataBase (max 2).

  Licence Plate Detection

  Run the mainfile.py

    Step1: Take the original image and convert into gray scale using open cv library (GrayScaleImage.png)

    Step2: Apply bilateral filter to the gray scale image. Bilateral filter is used to preserve images when various operations are done on image (ImageAfterBilateralFilter.png)

    Step3: Apply Canny Edge detection method to detect edges in images (ImageAfterCannyEdgeDetection.png)

    Step4: Then use contours method to find all continuous points having same intensity. The contours are useful for object detection, shape analysis and recognition.

    Step5: Mask the other part other than number plate and show only the license plate part. Convert all other pixels to black. (LicencePlateDetection.png)

  Number Extraction

    Step6: Then use teserract engine for detecting number plate characters by specifying the languages

  QR CODE
    
    Run the qrcodescanandprint.py 

    An employee might not always bring the registered vehicle to the institution.
    To keep log of these vehicles for future uses. We make use of the unique IDs (QR Codes) that are provided to the employees by the organization. 
    We have used the pyzbar library of python for detection and decoding of the QR codes. 
    The decode function identifies the points that form a quad and mark that region as the QR code. 
    It returns the following details present in the QR Code: type, data and location. 
    Type indicates the kind of code that has been scanned ie whether it is a barcode or a QR code, Data indicates the ID in our case and location provides the coordinates of the quad that is detected around the QR Code (Fig 1). 
    Let’s say an employee gets an unregistered vehicle to the institute. 
    The gate won’t open as the vehicle is not registered. Instead, a scanner will pop up on the screen asking the employee to scan his ID. 
    Once the QR Code is scanned, the ID is extracted from it in the form of a string and it is then verified for its presence in the database. 
    If the ID provided by the employee is a valid ID, the vehicle number will be stored against this ID as an alternate vehicle and the gate will be opened for the vehicle to enter. 
    This will also ensure security as a person, who isn’t a member of the institution, will not be allowed entry as their ID will not be available in the database.
