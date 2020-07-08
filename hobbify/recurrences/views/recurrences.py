""" Recurrences views """

# Django REST Framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Dateutil
from dateutil.rrule import rrule, DAILY, MONTHLY, WEEKLY

# Model
from hobbify.habits.models import Habit
from hobbify.recurrences.models import RecurrentInstance

# Utils
import datetime


def set_rule(habit_id):
    """ Set a rrule based on database habit information """
    habit = Habit.objects.filter(id=habit_id).first()

    start = habit.start_date
    end = habit.end_date
    freq = DAILY
    inter = 1

    if habit.frequency == 1:
        freq = DAILY
    elif habit.frequency == 2:
        freq = WEEKLY
    elif habit.frequency == 3:
        freq = MONTHLY
    elif habit.frequency == 4:
        freq = WEEKLY
        inter = 3
    else:
        freq = WEEKLY
        inter = 5

    habit_recurrences_rule = rrule(
        freq,
        dtstart=start,
        until=end,
        interval=inter,
        cache=True
    )

    return habit_recurrences_rule


def get_today_instance(id):
    """ Return today's recurrent instance """
    rule = set_rule(id)
    today = datetime.datetime.now().strftime("%Y-%d-%m")
    todays_intance = ""

    for s in rule:
        instance_date = str(s).partition(' ')[0]
        if instance_date == today:
            todays_intance = s
            break

    return todays_intance


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def list_recurrences(request, id):
    """ List all recurrences of a habit """
    rule = set_rule(id)

    temp = {}
    temp = [{"date": s} for s in rule]
    recurrences = [{"done": False, "date": s} for s, i in zip(rule, temp)]

    data = {
        "rule": str(rule),
        "instances": recurrences
    }

    return Response(
        data,
        status=status.HTTP_200_OK
    )


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def retrieve_today_recurrence(request, id):
    """ Return an object with today's recurrence """
    rule = set_rule(id)
    todays_intance = get_today_instance(id)

    if request.method == "GET":
        data = {
            "rule": str(rule),
            "done": False,
            "instance": todays_intance
        }

        return Response(
            data,
            status=status.HTTP_200_OK
        )
    elif request.method == "POST":
        today = datetime.datetime.now().strftime("%Y-%d-%m")
        habit = Habit.objects.filter(id=id).first()

        all_recurrences = RecurrentInstance.objects.filter(habit=habit)

        for s in all_recurrences:
            date = str(s.recurrence).partition(' ')[0]
            if date == today:
                return Response(
                    "Recurrence alredy exists in database, please retrieve it.",
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

        instance = RecurrentInstance.objects.create(
            habit=habit,
            done=False,
            rule=str(rule),
            recurrence=str(todays_intance)
        )

        data = {
            "id": instance.id,
            "rule": instance.rule,
            "instance": instance.recurrence,
            "done": instance.done
        }

        return Response(
            data,
            status=status.HTTP_201_CREATED
        )


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def retrieve_today_recurrence_by_id(request, id, r_id):
    """ Return today's recurrent instance by instance id """
    rule = set_rule(id)
    recurrence_instance = RecurrentInstance.objects.filter(id=r_id).first()
    todays_intance = get_today_instance(id)

    data = {
        "rule": str(rule),
        "done": recurrence_instance.done,
        "instance": todays_intance
    }

    return Response(
        data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def list_habit_recurrences(request, id):
    """ List all the recurrences of an habit """
    habit = Habit.objects.filter(id=id).first()
    recurrences = RecurrentInstance.objects.filter(habit=habit)
    data = []

    for r in recurrences:
        obj = {}
        obj['rule'] = r.rule
        obj['recurrence'] = r.recurrence
        obj['done'] = r.done
        data.append(obj)

    return Response(
        data,
        status=status.HTTP_200_OK
    )


@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
def update_recurrent_instance(request, id, r_id):
    """ Update an instance """
    rule = set_rule(id)
    if request.method == "PUT":
        todays_intance = get_today_instance(id)
        recurrence_instance = RecurrentInstance.objects.filter(id=r_id).first()

        recurrence_instance.done = request.data['done']
        recurrence_instance.save()

        data = {
            "rule": str(rule),
            "done": recurrence_instance.done,
            "date": todays_intance
        }

        return Response(
            data,
            status=status.HTTP_206_PARTIAL_CONTENT
        )

    return Response(status=status.HTTP_400_BAD_REQUEST) 
