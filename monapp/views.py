from django.shortcuts import render, redirect, get_object_or_404
import redis
import json
from monapp.initial_config import get_redis_client
import re
from django.http import JsonResponse

def select_student(request):
    r = get_redis_client()
    liste_students = r.keys('etudiant:*')
    student_keys = [key.decode('utf-8') for key in liste_students]
    students = []
    for key in student_keys:
        student_data = r.hgetall(key)
        student_info = {k.decode('utf-8'): v.decode('utf-8') for k, v in student_data.items()}
        students.append(student_info)

    liste_profs = r.keys('prof:*')
    prof_keys = [key.decode('utf-8') for key in liste_profs]
    profs = []
    for key in prof_keys:
        prof_data = r.hgetall(key)
        prof_info = {k.decode('utf-8'): v.decode('utf-8') for k, v in prof_data.items()}
        profs.append(prof_info)

    return render(request, 'etudiants.html', {'students': students, 'profs': profs})

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
    return render(request, 'manage_student.html', {'student': student, 'cours_details': cours_details})

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

def subscribe_cours(request, id_etudiant, id_cours):
    r = get_redis_client()
    canal_nouvelles = id_cours
    pubsub = r.pubsub()
    pubsub.subscribe(canal_nouvelles)

    nouveaux_messages = []
    for message in pubsub.listen():
        print('message', message, type(message), type(id_cours))
        if message['type'] == 'message':
            nouveaux_messages.append(message['data'].decode())

    print('nouveaux_messages', nouveaux_messages)

    return redirect('manage_student', id_etudiant=id_etudiant)

def messages(request, id_etudiant, id_cours):
    r = get_redis_client()
    nouveaux_messages = []

    pubsub = r.pubsub()
    if id_cours != '':
        pubsub.subscribe(id_cours)

        for message in pubsub.listen():
            if message['type'] == 'message':
                nouveaux_messages.append(message['data'].decode())
    else:
        # Si id_cours est une chaîne vide, nous ne nous abonnons à aucun canal
        nouveaux_messages.append("Aucun canal spécifié")

    return render(request, 'messages.html', {'nouveaux_messages': nouveaux_messages})


def rechercher(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        r = get_redis_client()

        resultat_eleves = []
        eleve_keys = r.keys('etudiant:*')
        for key in eleve_keys:
            eleve = r.hgetall(key)
            for value in eleve.values():
                if re.search(query, value.decode(), flags=re.IGNORECASE):
                    eleve_info = {k.decode(): v.decode() for k, v in eleve.items()}
                    resultat_eleves.append(eleve_info)
                    break

        resultat_cours = []
        eleve_keys = r.keys('cours:*')
        for key in eleve_keys:
            eleve = r.hgetall(key)
            for value in eleve.values():
                if re.search(query, value.decode(), flags=re.IGNORECASE):
                    eleve_info = {k.decode(): v.decode() for k, v in eleve.items()}
                    resultat_cours.append(eleve_info)
                    break

        resultat_professeurs = []
        eleve_keys = r.keys('prof:*')
        for key in eleve_keys:
            eleve = r.hgetall(key)
            for value in eleve.values():
                if re.search(query, value.decode(), flags=re.IGNORECASE):
                    eleve_info = {k.decode(): v.decode() for k, v in eleve.items()}
                    resultat_professeurs.append(eleve_info)
                    break

        return render(request, 'recherche.html', {
            'query': query,
            'resultat_eleves': resultat_eleves,
            'resultat_cours': resultat_cours,
            'resultat_professeurs': resultat_professeurs
        })
    else:
        return render(request, 'recherche.html')