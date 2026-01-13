
# def create_event(resquest):
#   if request.method == "POST":
#           event_name = request.POST.get("event_name")
#           category = request.POST.get("category")
#           first_name = request.POST.get("first_name")
#           second_name = request.POST.get("second_name")
#           description = request.POST.get("description")
#           fecha_selected = request.POST.get("close_date")

#           fecha_selected = datetime.strptime(fecha_selected, "%Y-%m-%dT%H:%M")

#           fecha_selected = timezone.make_aware(fecha_selected)

#           server_date = timezone.now()
#           if fecha_selected > server_date:
#               Evento.objects.create(
#                 creator = request.user,
#                 event_name = event_name,
#                 category=category,
#                 first_name=first_name,
#                 second_name=second_name,
#                 description=description,
#                 close_date=fecha_selected
#               )
#               print("Evento creado con éxito")
#               return redirect("profile")
#           else:
#               print("La fecha de cierre no puede ser pasada")
