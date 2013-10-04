#!/usr/bin/env python3
"""Get trains times to various destinations from your local train station."""
import sys
import re
import itertools
import threading

PY3 = sys.version_info[0] >= 3
if not PY3:
    print("Train Times only works with `python3`.")
    sys.exit(1)

import urllib.request
from time import sleep
from bs4 import BeautifulSoup
import pifacecommon
import pifacecad


UPDATE_INTERVAL = 60  # seconds

DEFAULT_DEPARTURE_STATION = "MAN"

TRAIN_STATIONS = [
    {'name': 'Manchester Piccadilly', 'code': 'MAN'},
    {'name': 'Manchester Oxford Road', 'code': 'MCO'},
    {'name': 'Manchester Airport', 'code': 'MIA'},
    {'name': 'London Euston', 'code': 'EUS'},
    {'name': 'Wigan Wallgate', 'code': 'WGW'},
    {'name': 'Stockport', 'code': 'SPT'},
    {'name': 'Southport', 'code': 'SOP'},
    {'name': 'Blackpool North', 'code': 'BPN'},
    {'name': 'Liverpool Lime Street', 'code': 'LIV'},
    {'name': 'Birmingham New Street', 'code': 'BHM'},
    {'name': 'Crewe via Stockport', 'code': 'CRE'},
    {'name': 'Crewe', 'code': 'CRE'},
    {'name': 'Macclesfield', 'code': 'MAC'},
    {'name': 'York', 'code': 'YRK'},
    {'name': 'Buxton', 'code': 'BUX'},
    {'name': 'Chester', 'code': 'CTR'},
    {'name': 'Wilmslow', 'code': 'WML'},
    {'name': 'Alderley Edge', 'code': 'ALD'},
]

# Pattern for live departure board information
LDB_URL = \
    'http://ojp.nationalrail.co.uk/service/ldbboard/dep/{depart}/{arrive}/To'

LATER_TIMES_PAGE_SIZE = 3


class StationError(Exception):
    pass


class NoTrainsError(Exception):
    pass


class TrainDepartureBoard(object):
    def __init__(self, departing_station, destination_station):
        self.departing_station = departing_station
        self.destination_station = destination_station
        self._times = None

    @property
    def times(self):
        if self._times is None:
            self.update_times()
        return self._times

    def update_times(self):
        # thanks sean https://github.com/seanbechhofer/raspberrypi/blob/master/
        # python/trains.py
        timeshtml = urllib.request.urlopen(LDB_URL.format(
            depart=self.departing_station['code'],
            arrive=self.destination_station['code'])).read()
        soup = BeautifulSoup(timeshtml)
        self._times = list()
        for div in soup.find_all('div'):
            if 'class' in div.attrs and "tbl-cont" in div['class']:
                body = div.table.tbody
                for row in body.find_all('tr'):
                    cells = row.find_all('td')
                    time = dict()
                    time['time'] = cells[0].contents[0].strip()
                    #time['dest'] = cells[1].contents[0].strip()
                    # Collapse all white space
                    #time['dest'] = re.sub(r"\s+", ' ', time['dest'])
                    time['report'] = cells[2].contents[0].strip()
                    if re.match('[0-9][0-9]:[0-9][0-9]', time['report']):
                        time['estimated'] = time['report']
                    else:
                        time['estimated'] = ""
                    self._times.append(time)

    @property
    def later_times(self):
        return self.times[1:]

    @property
    def later_times_pages(self):
        if len(self.later_times) <= LATER_TIMES_PAGE_SIZE:
            return [self.later_times]  # just one page
        else:
            return list(itertools.zip_longest(
                self.later_times[0::LATER_TIMES_PAGE_SIZE],
                self.later_times[1::LATER_TIMES_PAGE_SIZE],
                self.later_times[2::LATER_TIMES_PAGE_SIZE],
                fillvalue={'time': '', 'report': '', 'estimated': ''}
            ))


class TrainDepartureBoardDisplay(object):
    def __init__(self, cad, departure_boards, board_index=0):
        self.departure_boards = departure_boards
        self.board_index = board_index
        self.later_times_page = 0
        self.timer = threading.Timer(UPDATE_INTERVAL, self.auto_update)
        self.timer.start()
        self.cad = cad
        self.cad.lcd.backlight_on()
        self.cad.lcd.blink_off()
        self.cad.lcd.cursor_off()

    @property
    def current_board(self):
        """Returns the current board."""
        return self.departure_boards[self.board_index]

    def next_board(self, event=None):
        self.board_index = (self.board_index + 1) % len(self.departure_boards)
        self.update()

    def previous_board(self, event=None):
        self.board_index = (self.board_index - 1) % len(self.departure_boards)
        self.update()

    def update(self):
        self.cad.lcd.clear()
        self.print_loading()
        self.later_times_page = 0
        self.update_board()

    def update_board(self):
        self.current_board.update_times()
        try:
            self.print_next_train_time()
        except NoTrainsError:
            self.cad.lcd.clear()
            self.cad.lcd.write("No trains for\n{}".format(
                self.current_board.destination_station['name']))
        else:
            self.print_later_train_times()

    def auto_update(self):
        print("Updating.")
        self.update_board()
        self.timer = threading.Timer(UPDATE_INTERVAL, self.auto_update)
        self.timer.start()

    def print_loading(self):
        self.cad.lcd.write("Loading times to\n{}".format(
            self.current_board.destination_station['name'][:16]))

    def print_next_train_time(self):
        try:
            next_time_string = self.current_board.times[0]['time']
            estimated_time_string = self.current_board.times[0]['estimated']
        except IndexError:
            raise NoTrainsError()

        self.cad.lcd.clear()
        self.cad.lcd.write(
            "{next_time} {station_code} {estimated_time}".format(
                next_time=next_time_string,
                station_code=self.current_board.destination_station['code'],
                estimated_time=estimated_time_string,
            )
        )

    def print_later_train_times(self):
        later_times = \
            self.current_board.later_times_pages[self.later_times_page]
        if len(later_times) >= 3:
            later_times_string = " ".join(
                [t['time'].replace(":", "") for t in later_times]
            )
        elif len(later_times) > 0:
            later_times_string = " ".join([t['time'] for t in later_times])
        else:
            later_times_string = "No more trains."

        self.cad.lcd.set_cursor(0, 1)
        self.cad.lcd.write(later_times_string.ljust(pifacecad.lcd.LCD_WIDTH))

    def next_later_times_page(self, event=None):
        total_pages = len(self.current_board.later_times_pages)
        self.later_times_page = (self.later_times_page + 1) % total_pages
        self.print_later_train_times()

    def close(self):
        if self.timer is not None:
            self.timer.cancel()
        self.cad.lcd.clear()
        self.cad.lcd.backlight_off()


def get_station_from_code(code):
    for station in TRAIN_STATIONS:
        if station['code'] == code:
            return station
    else:
        raise StationError("Invalid station code", code)

if __name__ == "__main__":
    try:
        departure_station = get_station_from_code(sys.argv[1].upper())
    except IndexError:
        departure_station = get_station_from_code(DEFAULT_DEPARTURE_STATION)

    departure_boards = [
        TrainDepartureBoard(departure_station, station)
        for station in TRAIN_STATIONS
        if station is not departure_station
    ]

    cad = pifacecad.PiFaceCAD()

    global traintimedisplay
    traintimedisplay = TrainDepartureBoardDisplay(cad, departure_boards)
    traintimedisplay.update()

    # listener cannot deactivate itself so we have to wait until it has
    # finished using a barrier.
    global end_barrier
    end_barrier = threading.Barrier(2)

    # wait for button presses
    global switchlistener
    switchlistener = pifacecad.SwitchEventListener(chip=cad)
    switchlistener.register(4, pifacecad.IODIR_ON, end_barrier.wait)
    switchlistener.register(
        5, pifacecad.IODIR_ON, traintimedisplay.next_later_times_page)
    switchlistener.register(
        6, pifacecad.IODIR_ON, traintimedisplay.previous_board)
    switchlistener.register(
        7, pifacecad.IODIR_ON, traintimedisplay.next_board)

    switchlistener.activate()
    end_barrier.wait()  # wait unitl exit

    # exit
    traintimedisplay.close()
    switchlistener.deactivate()
