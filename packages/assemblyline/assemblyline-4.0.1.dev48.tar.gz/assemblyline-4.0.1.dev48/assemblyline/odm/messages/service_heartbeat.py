from assemblyline import odm

MSG_TYPES = {"ServiceHeartbeat"}
LOADER_CLASS = "assemblyline.odm.messages.service_heartbeat.ServiceMessage"


@odm.model()
class Metrics(odm.Model):
    cache_hit = odm.Integer()
    cache_miss = odm.Integer()
    cache_skipped = odm.Integer()
    execute = odm.Integer()
    fail_recoverable = odm.Integer()
    fail_nonrecoverable = odm.Integer()
    scored = odm.Integer()
    not_scored = odm.Integer()


@odm.model()
class Activity(odm.Model):
    busy = odm.Integer()
    idle = odm.Integer()


@odm.model()
class Heartbeat(odm.Model):
    activity = odm.Compound(Activity)
    instances = odm.Integer()
    metrics = odm.Compound(Metrics)
    queue = odm.Integer()
    service_name = odm.Keyword()


@odm.model()
class ServiceMessage(odm.Model):
    msg = odm.Compound(Heartbeat)
    msg_loader = odm.Enum(values={LOADER_CLASS}, default=LOADER_CLASS)
    msg_type = odm.Enum(values=MSG_TYPES, default="ServiceHeartbeat")
    sender = odm.Keyword()
