""" Habits views """

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Serializers
from hobbify.habits.serializers import HabitModelSerializer
from hobbify.habits.serializers import RecurrenceModelSerializer

# Dateutil
from dateutil.rrule import rrule, DAILY, MONTHLY, WEEKLY

# Models
from hobbify.habits.models import Habit
from hobbify.users.models import User
from hobbify.habits.models import RecurrentInstance

# Utils
import datetime


class HabitViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """ Habit view set """

    lookup_field = 'id'
    serializer_class = HabitModelSerializer

    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ('created', 'end_date', 'start_date')
    ordering_fields = ('created', 'end_date', 'modified', 'start_date')
    search_fields = ('name', 'description')
    filter_fields = ('paused', 'is_private')

    def dispatch(self, request, *args, **kwargs):
        """ Verify that the user exists """
        username = kwargs['username']
        self.user = get_object_or_404(User, username=username)
        return super(HabitViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        """ Add user to serializer context """
        context = super(HabitViewSet, self).get_serializer_context()
        context['user'] = self.user
        return context

    def get_queryset(self):
        """ Return not hidden habits """
        queryset = Habit.objects.filter(is_hidden=False)
        if self.action == 'list':
            username = self.kwargs['username']
            return Habit.objects.filter(is_hidden=False, owner__username=username)
        return queryset

    def get_permissions(self):
        """ Assign permission based on action """
        permissions = [IsAuthenticated,]
        return [p() for p in permissions]

    @action(methods=['get', 'patch'], detail=True)
    def instance(self, request, *args, **kwargs):
        """ Return and partial update instance by id """
        instance = RecurrentInstance.objects.filter(habit=self.kwargs['id'], is_hidden=False, id=self.kwargs['r_id'])
        if request.method == 'PATCH':
            instance.done = request.data.done
        return Response(instance, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def recurrences(self, request, *args, **kwargs):
        """ Return the past recurrences of an habit """
        recurrences = RecurrentInstance.objects.filter(habit=self.kwargs['id'], is_hidden=False)
        data = [RecurrenceModelSerializer(r).data for r in recurrences]
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def recurrence(self, request, *args, **kwargs):
        """ Create today's instance of an habit """
        habit_id = self.kwargs['id']
        habit = Habit.objects.filter(id=habit_id, is_hidden=False).first()
        rule = self.set_rule(habit_id)
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        all_recurrences = RecurrentInstance.objects.filter(habit=habit, is_hidden=False)

        for s in all_recurrences:
            date = str(s.recurrence).partition(' ')[0]
            if date == today:
                return Response(
                    "Recurrence alredy exists in database, please retrieve it.",
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

        all_instances = [{"date": s} for s in rule]
        todays_intance = ""

        for obj in all_instances:
            date = str(obj['date']).partition(' ')[0]
            if today == date:
                todays_intance = obj['date']
                break

        if todays_intance == "":
            return Response(
                "Cannot create an instance if it does not match its recurrent rule",
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        instance = RecurrentInstance.objects.create(
            habit=habit,
            done=False,
            rule=str(rule),
            recurrence=str(todays_intance)
        )
        data = RecurrenceModelSerializer(instance).data

        return Response(
            data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['get'])
    def today(self, request, *args, **kwargs):
        """ Return today's instance of an habit """
        habit_id = self.kwargs['id']
        rule = self.set_rule(habit_id)
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        instances = RecurrentInstance.objects.filter(is_hidden=False, habit=habit_id)
        instances_data = [RecurrenceModelSerializer(instance).data for instance in instances]
        todays_intance = {}

        for info in instances_data:
            instance_date = str(info['recurrence']).partition(' ')[0]
            print(instance_date, today)
            if instance_date == today and str(info['rule']) == str(rule):
                todays_intance = info

        return Response(todays_intance, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def all(self, request, *args, **kwargs):
        """ Return all recurrences of a habit """
        rule = self.set_rule(self.kwargs['id'])
        temp = [{"date": s} for s in rule]

        data = {
            "rule": str(rule),
            "instances": temp
        }

        return Response(data, status=status.HTTP_200_OK)

    def get_today_instance(self, id):
        """ Return today's recurrent instance """
        rule = self.set_rule(id)
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        todays_intance = ""

        for s in rule:
            instance_date = str(s).partition(' ')[0]
            if instance_date == today:
                todays_intance = s
                break

        return todays_intance

    def set_rule(self, habit_id):
        """ Set a rrule based on database habit information """
        habit = Habit.objects.filter(id=habit_id).first()

        start = habit.start_date
        freq = DAILY
        inter = 1
        end = habit.end_date if habit.end_date is not None else habit.start_date + datetime.timedelta(days=21)

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
