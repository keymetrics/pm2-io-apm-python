from opencensus.common.utils import check_str_length
from opencensus.common.utils import timestamp_to_microseconds
from opencensus.trace.exporters import base
import time

SPAN_KIND_MAP = {
    0: None,  # span kind unspecified
    1: "SERVER",
    2: "CLIENT",
}

SUCCESS_STATUS_CODE = (200, 202)

class CustomExporter(base.Exporter):
    def __init__(self, transporter):
        self.transporter = transporter
        self.service_name = 'service_name'

    def emit(self, span_datas):
        pass
    
    def export(self, span_datas):
        """Send SpanData tuples to Zipkin server, default using the v2 API.
        :type span_datas: list of :class:
            `~opencensus.trace.span_data.SpanData`
        :param list of opencensus.trace.span_data.SpanData span_datas:
            SpanData tuples to emit
        """

        try:
            zipkin_spans = self.translate_to_zipkin(span_datas)
            for span in zipkin_spans:
              self.transporter.sendJson({
                'channel': 'trace-span',
                'payload': span
              })
        except Exception as e:  # pragma: NO COVER
            print(getattr(e, 'message', e))

    def translate_to_zipkin(self, span_datas):
        """Translate the opencensus spans to zipkin spans.
        :type span_datas: list of :class:
            `~opencensus.trace.span_data.SpanData`
        :param span_datas:
            SpanData tuples to emit
        :rtype: list
        :returns: List of zipkin format spans.
        """

        local_endpoint = {
            'serviceName': self.service_name
        }

        zipkin_spans = []

        for span in span_datas:
            # Timestamp in zipkin spans is int of microseconds.
            start_timestamp_mus = timestamp_to_microseconds(span.start_time)
            end_timestamp_mus = timestamp_to_microseconds(span.end_time)
            duration_mus = end_timestamp_mus - start_timestamp_mus

            zipkin_span = {
                'traceId': span.context.trace_id,
                'id': str(span.span_id),
                'name': span.name,
                'timestamp': int(round(start_timestamp_mus)),
                'duration': int(round(duration_mus)),
                'localEndpoint': local_endpoint,
                'tags': _extract_tags_from_span(span.attributes),
                'annotations': _extract_annotations_from_span(span),
                'process': {
                  'pm_id': 0,
                  'name': self.transporter.config.name,
                  'server': self.transporter.config.serverName,
                  'rev': None,
                },
            }

            span_kind = span.span_kind
            parent_span_id = span.parent_span_id

            if span_kind is not None:
                kind = SPAN_KIND_MAP.get(span_kind)
                # Zipkin API for span kind only accept
                # enum(CLIENT|SERVER|PRODUCER|CONSUMER|Absent)
                if kind is not None:
                    zipkin_span['kind'] = kind

            if parent_span_id is not None:
                zipkin_span['parentId'] = str(parent_span_id)

            zipkin_spans.append(zipkin_span)

        return zipkin_spans

def _extract_tags_from_span(attr):
    if attr is None:
        return {}
    tags = {}
    for attribute_key, attribute_value in attr.items():
        if isinstance(attribute_value, (int, bool)):
            value = str(attribute_value)
        elif isinstance(attribute_value, str):
            res, _ = check_str_length(str_to_check=attribute_value)
            value = res
        else:
            print('Could not serialize tag {}'.format(attribute_key))
            continue
        tags[attribute_key] = value
    return tags


def _extract_annotations_from_span(span):
    """Extract and convert time event annotations to zipkin annotations"""
    if span.time_events is None:
        return []

    annotations = []
    for time_event in span.time_events:
        annotation = time_event.annotation
        if not annotation:
            continue

        event_timestamp_mus = timestamp_to_microseconds(time_event.timestamp)
        annotations.append({'timestamp': int(round(event_timestamp_mus)),
                            'value': annotation.description})

    return annotations
