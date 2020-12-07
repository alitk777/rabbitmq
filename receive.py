#!/usr/bin/env python
import json

import pika, sys, os

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'),
    )
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        data = json.loads(body)

        action = format(data['action'])
        attribute = format(data['attribute'])
        details = format(data['details'])
        new_value = format(data['newValue'])
        old_value = format(data['oldValue'])
        report = ""

        if action == 'Create':
            report = 'Created'

        elif attribute == 'Phase':
            report = f"Moved to '{new_value}'"

        elif attribute == 'Project':
            report = f"Moved to '{new_value}' from '{old_value}'"

        elif attribute == 'Status':
            if old_value is None:
                report = f'Set {attribute} ' \
                    f"in {details} " \
                    f"to '{new_value}'"
            else:
                report = f'Changed {attribute} ' \
                    f"in {details} " \
                    f"from '{old_value}' to '{new_value}'"

        elif attribute == 'batch' and new_value is None:
            report = f'Removed {attribute} from '\
                f'{old_value}'

        elif attribute == 'Resource' and action == 'Append':
            report = f"Assigned {details} to {new_value}"

        elif attribute == 'Resource' and action == 'Remove':
            report = f"Unassigned {details} to {old_value}"

        elif old_value is None and new_value is not None:
            report = f'Set {attribute} to {new_value}'

        elif new_value is not None and old_value is not None and \
                action == 'Update':
            report = f'Modified {attribute} from ' \
                f'{old_value} to ' \
                f'{new_value}'

        else:
            inner_string = 'to' if old_value is not None else ''
            report = f'{action} {attribute} {old_value} {inner_string} ' \
                f'{new_value}'

        print(report)

    channel.basic_consume(
        queue='hello',
        on_message_callback=callback,
        auto_ack=True,
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

