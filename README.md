# CureNet
A web-based appointment booking system to streamline scheduling and manage appointments for both patient and healthcare providers.

## Screenshots
### Homepage
![2](https://github.com/user-attachments/assets/ea3dae94-9806-45e4-9c1f-41a0322e6e86)
### Login Page
![1](https://github.com/user-attachments/assets/233858ba-55bf-4688-b58a-d2b70247fe10)
### Doctors's Profile Page
![4](https://github.com/user-attachments/assets/b8de95c2-1433-41e1-93f4-39832f0fbf10)
### Appointment Page
![6](https://github.com/user-attachments/assets/261df607-f54f-4bf4-8825-0f0bc5d0c26f)
### Doctor's Dashboard Page
![10](https://github.com/user-attachments/assets/f834c420-0c23-40d4-8446-500625ae5a04)

## Functions
### Doctor
1. Administrative functionalities for Medical Experts to manage their appointments and view appointment history.
2. Able to edit profile details.

### Patient
1. Search and filtering options for patients to find available doctors based on specialization and availability.
2. Able to edit profile details.
3. Manage or cancel appointment at any time.
4. Generate Invoice
5. Patient can add stories about their experience with the doctor on their profile and also able to see other patient's stories and reviews.

## How to run this project
- Install Python (Dont Forget to Tick Add to Path while installing Python)
- Open Terminal and Execute Following Commands :
``` python -m pip install -r requirements.txt ```
- Move to project folder in Terminal. Then run following Commands:
```
py manage.py makemigrations 
py manage.py migrate 
py manage.py runserver
``` 
- Now enter following URL in Your Browser Installed On Your Pc
## Note
This project is developed for demo purpose and it's not supposed to be used in real application.


