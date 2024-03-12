from users.models import RegisteredHospital


def approve_reg_application():
    return True


def get_registered_hospitals():
    registered_hospitals = RegisteredHospital.objects.all()
    registered_hospital_dict = {}
    for i in registered_hospitals:
        registered_hospital_dict[i.hospital_name] = i.hospital_name
    return registered_hospital_dict