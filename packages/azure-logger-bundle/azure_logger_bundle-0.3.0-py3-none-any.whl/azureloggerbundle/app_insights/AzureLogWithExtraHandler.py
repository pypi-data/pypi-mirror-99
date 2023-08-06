from opencensus.ext.azure.log_exporter import AzureLogHandler, Envelope, Message
from loggerbundle.extra.ExtraKeysResolver import ExtraKeysResolver


class AzureLogWithExtraHandler(AzureLogHandler):
    def log_record_to_envelope(self, record):
        envelope: Envelope = super().log_record_to_envelope(record)

        message: Message = envelope.data.baseData

        record_dict = record.__dict__
        extra_keys = ExtraKeysResolver.get_extra_keys(record)

        message.properties["loggerName"] = record.name

        for k in extra_keys:
            if k != "message":
                message.properties["extra_{}".format(k)] = str(record_dict[k])

        return envelope
