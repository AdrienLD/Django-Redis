import json
import redis
from django.shortcuts import render, redirect

def get_redis_client():
    r = redis.Redis
    r = redis.Redis(host='localhost', port=6379)
    return r

def create_course(course_id, titre, prof):
    r = get_redis_client()
    course_data = {
        'id': course_id,
        'titre': titre,
        'prof': prof,
        'etudiants': json.dumps([])
    }
    course_key = f"cours:{course_id}"
    for key, value in course_data.items():
        r.hset(course_key, key, value)

def create_student(student_id, nom, prenom, cours):
    r = get_redis_client()
    student_data = {
        'id': student_id,
        'nom': nom,
        'prenom': prenom,
        'cours': json.dumps(cours)
    }
    student_key = f"etudiant:{student_id}"
    for key, value in student_data.items():
        r.hset(student_key, key, value)

def create_teacher(teacher_id, nom, prenom, cours):
    r = get_redis_client()
    teacher_data = {
        'id': teacher_id,
        'nom': nom,
        'prenom': prenom,
        'cours': json.dumps(cours)
    }
    teacher_key = f"prof:{teacher_id}"
    for key, value in teacher_data.items():
        r.hset(teacher_key, key, value)



def initialize(request):
    create_course('101', 'Programmation Web', 'M. Dupont')
    create_course('102', 'Base de données', 'M. Durand')
    create_course('103', 'Réseaux', 'M. Martin')
    create_course('104', 'Intelligence Artificielle', 'Mme. Leblanc')
    create_course('105', 'Systèmes d\'exploitation', 'M. Lambert')
    create_course('106', 'Algorithmique', 'Mme. Dupuis')
    create_course('107', 'Sécurité informatique', 'M. Lefebvre')
    create_course('108', 'Analyse de données', 'Mme. Lemoine')

    create_student('201', 'Pierre', 'Jean', ['101', '102', '103'])
    create_student('202', 'Feur', 'Paul', ['101', '104', '105'])
    create_student('203', 'Chirac', 'Jacques', ['101', '102', '106'])
    create_student('204', 'Claire', 'Marie', ['101', '102', '107'])
    create_student('205', 'Castello', 'Sophie', ['101', '102', '108'])
    create_student('206', 'Merveille', 'Alice', ['101', '103', '104'])
    create_student('207', 'Armani', 'Julie', ['101', '105', '106'])
    create_student('208', 'Stylop', 'Marine', ['101', '107', '108'])


    create_teacher('301', 'Dupont', 'M.', ['101'])
    create_teacher('302', 'Durand', 'M.', ['102'])
    create_teacher('303', 'Martin', 'M.', ['103'])
    create_teacher('304', 'Leblanc', 'Mme.', ['104'])
    create_teacher('305', 'Lambert', 'M.', ['105'])
    create_teacher('306', 'Dupuis', 'Mme.', ['106'])
    create_teacher('307', 'Lefebvre', 'M.', ['107'])
    create_teacher('308', 'Lemoine', 'Mme.', ['108'])

    return redirect('select_student')
