#!/usr/bin/env python3

import argparse

import numpy  # Make sure NumPy is loaded before it is used in the callback
import sounddevice as sd

assert numpy  # avoid "imported but unused" message (W0611)


class AudioWiring():
    def __init__(self):
        self.parser = argparse.ArgumentParser(add_help=False)
        self.parser.add_argument(
            '-l', '--list-devices', action='store_true',
            help='show list of audio devices and exit')
        self.args, self.remaining = self.parser.parse_known_args()
        if self.args.list_devices:
            print(sd.query_devices())
            self.parser.exit(0)
        self.parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[self.parser])
        self.parser.add_argument(
            '-i', '--input-device', type=AudioWiring.int_or_str,
            help='input device (numeric ID or substring)')
        self.parser.add_argument(
            '-o', '--output-device', type=AudioWiring.int_or_str,
            help='output device (numeric ID or substring)')
        self.parser.add_argument(
            '-c', '--channels', type=int, default=2,
            help='number of channels')
        self.parser.add_argument('--dtype', help='audio data type')
        self.parser.add_argument(
            '--samplerate', type=float, help='sampling rate')
        self.parser.add_argument('--blocksize', type=int, help='block size')
        self.parser.add_argument(
            '--latency', type=float, help='latency in seconds')
        self.args = self.parser.parse_args(self.remaining)

    @staticmethod
    def int_or_str(text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    def callback(self, indata, outdata, frames, time, status):
        if status:
            print(status)
        outdata[:] = indata

    def run(self):
        try:
            with sd.Stream(device=(self.args.input_device, self.args.output_device),
                           samplerate=self.args.samplerate, blocksize=self.args.blocksize,
                           dtype=self.args.dtype, latency=self.args.latency,
                           channels=self.args.channels, callback=self.callback):
                print('#' * 80)
                print('press Return to quit')
                print('#' * 80)
                input()
        except KeyboardInterrupt:
            self.parser.exit('')
        except Exception as e:
            self.parser.exit(type(e).__name__ + ': ' + str(e))
