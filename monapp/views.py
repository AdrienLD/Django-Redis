from django.shortcuts import render, redirect, get_object_or_404
import redis
import json
from monapp.initial_config import get_redis_client

def select_student(request):
    r = get_redis_client()
    liste_students = r.keys('etudiant:*')
    student_keys = [key.decode('utf-8') for key in liste_students]
    students = []
    for key in student_keys:
        student_data = r.hgetall(key)
        student_info = {k.decode('utf-8'): v.decode('utf-8') for k, v in student_data.items()}
        students.append(student_info)

    return render(request, 'etudiants.html', {'students': students})

def manage_student(request, id_etudiant):
    r = get_redis_client()
    student_key = f"etudiant:{id_etudiant}"
    student_data = r.hgetall(student_key)
    student = {k.decode('utf-8'): v.decode('utf-8') for k, v in student_data.items()}
    cours_liste = r.keys('cours:*')
    student_keys = [key.decode('utf-8') for key in cours_liste]
    cours_details = []
    for key in student_keys:
        cours_data = r.hgetall(key)
        cours_info = {k.decode('utf-8'): v.decode('utf-8') for k, v in cours_data.items()}
        cours_details.append(cours_info)
    return render(request, 'manage.html', {'student': student, 'cours_details': cours_details})

def delete_cours(request, id_etudiant, id_cours):
    r = get_redis_client()
    student_key = f"etudiant:{id_etudiant}"
    student_data = r.hgetall(student_key)
    student = {k.decode('utf-8'): v.decode('utf-8') for k, v in student_data.items()}
    cours_ids = json.loads(student['cours'])
    cours_ids.remove(str(id_cours))
    r.hset(student_key, 'cours', json.dumps(cours_ids))

    
    return redirect('manage_student', id_etudiant=id_etudiant)

def add_cours(request, id_etudiant, id_cours):
    r = get_redis_client()
    student_key = f"etudiant:{id_etudiant}"
    student_data = r.hgetall(student_key)
    student = {k.decode('utf-8'): v.decode('utf-8') for k, v in student_data.items()}
    cours_ids = json.loads(student['cours'])
    cours_ids.append(str(id_cours))
    r.hset(student_key, 'cours', json.dumps(cours_ids))
    
    return redirect('manage_student', id_etudiant=id_etudiant)
