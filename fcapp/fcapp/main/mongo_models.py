from django.contrib.auth.models import User
from django.db.models import Manager
from django_mongoengine import Document, EmbeddedDocument, fields, queryset
from mongoengine.base import datastructures
import datetime
import re


class System(EmbeddedDocument):
    companyName = fields.StringField(blank=True)
    model = fields.StringField()
    fullModel = fields.StringField()
    osVersion = fields.StringField()
    patches = fields.ListField(fields.StringField(), blank=True)
    """
    "patches" : [ "P01", "P02", "P04" ],
    """
    sp = fields.DictField(blank=True)
    """
    "sp" : {
      "spId" : "8094306",
      "spModel" : "ProLiant DL120 Gen9",
      "spVersion" : "5.0.0.0-22913 (5.0 GA)"
    },
    """
    productSKU = fields.StringField(blank=True, null=True)
    productFamily = fields.StringField(blank=True, null=True)
    recommended = fields.DictField(blank=True)
    """
    "recommended" : {
      "criticalPatches" : [ "P20" ],
      "conditionalPatches" : [ "P12", "P05" ],
      "spVersion" : "5.0.2.0-23974"
    }
    """


class Capacity(EmbeddedDocument):
    """
        "dataRateKBPSAvg" : 77135,
        "dataRateKBPSMax" : 187243,
        "dataRateKBPSMin" : 582,
        "iopsAvg" : 1049,
        "iopsMax" : 2209,
        "iopsMin" : 145,
        "ioSizeAvg" : 59.896141052246094,
        "ioSizeMax" : 178,
        "ioSizeMin" : 0,
        "queueLengthAvg" : 0,
        "queueLengthMax" : 2,
        "queueLengthMin" : 0,
        "serviceTimeMSAvg" : 1.4903336763381958,
        "serviceTimeMSMax" : 4,
        "serviceTimeMSMin" : 0
    """
    total = fields.DictField()
    byType = fields.DictField()
    arrayType = fields.StringField()


class PerformanceBandwidth(EmbeddedDocument):
    total = fields.DictField(blank=True)
    read = fields.DictField(blank=True)
    write = fields.DictField(blank=True)

class PerformanceSummary(EmbeddedDocument):
    """
    "readServiceTimeColMillis" : 1.050376296043396,
        "writeServiceTimeColMillis" : 1.0604130029678345,
        "totalServiceTimeColMillis" : 1.4903336763381958
    """
    portInfo = fields.DictField(blank=True)


class Performance(EmbeddedDocument):
    portBandwidthData = fields.EmbeddedDocumentField(PerformanceBandwidth, blank=True)
    summary = fields.EmbeddedDocumentField(PerformanceSummary)


class DisksByType(EmbeddedDocument):
    ssd = fields.DictField(blank=True)
    fc = fields.DictField(blank=True)
    nl = fields.DictField(blank=True)


class Disks(EmbeddedDocument):
    total = fields.DictField()
    byType = fields.EmbeddedDocumentField(DisksByType)
    state = fields.StringField()


class Authorized(EmbeddedDocument):
    tenants = fields.ListField(fields.StringField())


class Device(Document):
    serialNumberInserv = fields.StringField()
    system = fields.EmbeddedDocumentField(System)
    capacity = fields.EmbeddedDocumentField(Capacity)
    performance = fields.EmbeddedDocumentField(Performance)
    disks = fields.EmbeddedDocumentField(Disks)
    nodes = fields.DictField()
    authorized = fields.EmbeddedDocumentField(Authorized)
    updated = fields.DateTimeField()
    date = fields.DateTimeField()

    def __str__(self):
        if self.system and self.system.fullModel:
            return "{} ({})".format(self.system.fullModel, self.serialNumberInserv)
        return "{}".format(self.serialNumberInserv)

    @staticmethod
    def for_user(user_id):
        tenant = Tenant.id_for_user(user_id)
        d = Device.objects.filter(authorized__tenants=tenant)
        d._user_id = user_id
        return d

    def has_triggered(self):
        user_ids = Tenant.objects.filter(tenant_id__in=self.authorized.tenants).values_list('user_id')
        statuses = Status.objects.filter(device_id=str(self.id), user_id__in=user_ids)
        for s in statuses:
            if s.current_check():
                return True
        return False

class Tenant(Document):
    user_id = fields.IntField()
    tenant_id = fields.StringField()

    @property
    def user(self):
        return User.objects.get(id=self.user_id)

    def __str__(self):
        return "{} <=> {}".format(self.user_id, self.tenant_id)

    @staticmethod
    def for_user(user_id):
        return Tenant.objects.filter(user_id=user_id)

    @staticmethod
    def id_for_user(user_id):
        try:
            return Tenant.objects.get(user_id=user_id).tenant_id
        except Tenant.DoesNotExist:
            return None

class StatusCriteria(EmbeddedDocument):
    metric = fields.ListField(fields.StringField())
    OPERATIONS = (
        ('neq', '!='),
        ('eq', '=='),
        ('lt', '<'),
        ('lte', '<='),
        ('gt', '>'),
        ('gte', '>='),
        ('exists', '?='),
        ('nexist', '?!='),
        ('within', '<>')
    )
    operation = fields.StringField(max_length=6, choices=OPERATIONS)
    value = fields.StringField()

    PRETTY_MAP = {
      "system,osVersion": "OS Version",
      "system,patches": "Patches",
      "system,recommended,criticalPatches": "Recommended Critical Patches",
      "system,recommended,osVersion": "Recommended OS Version",
      "capacity,total,freeTiB": "Free Space (TB)",
      "capacity,total,freePct": "Free Space (Percent)",
      "capacity,total,usedSpaceTiB": "Used Space (TB)",
      "capacity,total,failedCapacityTiB": "Failed Capacity (TB)",
      "capacity,total,dedupeRatio": "Dedupe Ratio",
      "performance,portBandwidthData,total,iopsAvg": "Average IOPS",
      "performance,portBandwidthData,total,dataRateKBPSMin": "Data Rate (KBPS)",
      "disks,state": "Disk State",
      "disks,total,diskCountNormal": "Normal Disk Count",
      "capacity,byType,ssd,lifeLeftPctMin": "SSD Life Left (%)"
    }
    def metric_pretty(self):
        if ','.join(self.metric) in self.PRETTY_MAP:
            return self.PRETTY_MAP[','.join(self.metric)]
        return self.metric[-1]

    def metric_value_for(self, device):
        obj = device
        for i in self.metric:
            if i in obj:
                obj = obj[i]
            else:
                return None

        return obj

    @property
    def operation_symbol(self):
        return dict(self.OPERATIONS)[self.operation]

    def operation_check(self, val=None):
        try:
            if self.operation == 'eq':
                return str(val) == str(self.value)
            elif self.operation == 'neq':
                return not (str(val) == str(self.value))
            elif self.operation == 'lt':
                return float(val) < float(self.value)
            elif self.operation == 'lte':
                return float(val) <= float(self.value)
            elif self.operation == 'gt':
                return float(val) > float(self.value)
            elif self.operation == 'gte':
                return float(val) >= float(self.value)
            elif self.operation == 'within':
                tokens = re.search("(\(|\[)(\d+)\ *,\ *(\d+)(\)|\])", self.value)
                lower = (float(val) >= float(tokens.group(2))) if tokens.group(1) == '[' else (float(val) > float(tokens.group(2)))
                upper = (float(val) <= float(tokens.group(3))) if tokens.group(4) == ']' else (float(val) < float(tokens.group(3)))
                return lower and upper
            elif self.operation == 'exists':
                if type(val) == datastructures.BaseList:
                    return str(self.value) in [str(i) for i in val]
                return bool(val)
            elif self.operation == 'nexist':
                if type(val) == datastructures.BaseList:
                    return str(self.value) not in [str(i) for i in val]
                return not (bool(val))
        except (ValueError, TypeError):
            return False

    def __str__(self):
        return "[{}] {} {}".format(']['.join(self.metric), self.operation_symbol, self.value)

class DefaultStatus(Document):
    criteria = fields.EmbeddedDocumentField(StatusCriteria)
    name = fields.StringField()


class Status(Document):
    user_id = fields.IntField()
    criteria = fields.EmbeddedDocumentField(StatusCriteria)
    device_id = fields.StringField()
    active = fields.BooleanField()

    @property
    def device(self):
        return Device.objects.get(id=self.device_id)

    def current_value(self):
        return self.criteria.metric_value_for(self.device)

    def current_check(self):
        return self.criteria.operation_check(self.current_value())

    def __str__(self):
        return "{}{}".format(self.device_id, self.criteria)

    @staticmethod
    def only_triggered_for(user_id):
        active = Status.objects.filter(user_id=user_id, active=True)
        triggered_ids = []
        for obj in active:
            if obj.current_check():
                triggered_ids.append(str(obj.id))


        return Status.objects.filter(id__in=triggered_ids)

    @staticmethod
    def for_user(user_id):
        return Status.objects.filter(user_id=user_id)
