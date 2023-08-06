import os
import sys
import time
import argparse

from .sximage import open_fpga, close_fpga, call_fpga

#audio_rate = 15625
audio_rate = 18750

def fpgacap():
    parser = argparse.ArgumentParser(prog='fpgacap', description='SxImage FPGA CLI')
    parser.add_argument('-d','--decimal', action='store_true', help='decimal display')
    parser.add_argument('-u','--unsigned', action='store_true', help='unsigned display')
    parser.add_argument('-r','--rgb', action='store_true', help='rgb image')
    parser.add_argument('-g','--gray', action='store_true', help='grayscale image')
    parser.add_argument('--wav', action='store_true', help='audio frame')
    parser.add_argument('-w','--width', type=int, default=None)
    parser.add_argument('-l','--loop', action='store_true')
    parser.add_argument('-o','--out', default=None)
    parser.add_argument('--interval', type=int, default=200)
    parser.add_argument('--timeout', type=int, default=2000)
    parser.add_argument('--baud', type=int, default=1000000)
    parser.add_argument('port')
    args = parser.parse_args()

    if args.rgb or args.gray:
        import cv2
        import numpy as np

    if args.wav:
        import wave

    if args.rgb or args.gray or args.wav:
        if not args.width:
            print('The width option must be present with --rgb, --gray or --wav')
            sys.exit(1)
    elif args.loop:
        if not args.width:
            print('The width option must be present with --loop')
            sys.exit(1)

    if args.loop:
        if args.wav:
            print('Cannot use --loop with --wav option')
            sys.exit(1)
            
    frameno = 0
    if args.loop and args.out:
        while frameno < 9999:
            name = "%s-%04d.tiff" % (args.out, frameno)
            if not os.path.exists(name):
                break
            frameno += 1
        if frameno >= 10000:
            print('Exceeded maximum frame series')
            sys.exit(1)
        if frameno > 0:
            print('Resuming capture series at '+name)

    def calc_size():
        if args.rgb:
            return (args.width, args.width * 3)
        elif args.gray:
            return (args.width, args.width)
        elif args.wav:
            return (args.width, 2)
        return (args.width, 1)

    def toint(b):
        if b > 127:
            return int(b) - 256
        return int(b)

    def emit(buf,split=None):
        if args.decimal:
            print('\t'.join(['%d' % toint(x) for x in buf]))
        elif args.unsigned:
            print('\t'.join(['%d' % x for x in buf]))
        elif split:
            for i in range(len(buf)//split):
                print(buf[i*split:(i+1)*split].hex())
        else:
            print(buf.hex())

    def write_img(img):
        global frameno
        if args.loop:
            name = "%s-%04d.tiff" % (args.out, frameno)
            cv2.imwrite(name, img)
            frameno += 1
        else:
            cv2.imwrite(args.out, img)

    def write_wav(ba):
        le = bytearray()
        for i in range(len(ba)//2):
            le.append(ba[1+2*i])
            le.append(ba[2*i])
        wav = wave.open(args.out, 'wb')
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(audio_rate)
        wav.setnframes(len(ba)//2)
        wav.writeframes(bytes(le))
        wav.close()

        outf = open('audio.hex','w')
        for i in range(len(ba)//2):
            outf.write(ba[i*2:(i+1)*2].hex()+'\n')
        outf.close()

    def show_rgb(ba, width, height):
        img = np.fromstring(ba, dtype=np.uint8).reshape(height, width, 3)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow('capture', img)
        if args.out:
            write_img(img)

    def show_gray(ba, width, height):
        img = np.fromstring(ba, dtype=np.uint8).reshape(height, width)
        cv2.imshow('capture', img)
        if args.out:
            write_img(img)

    def play_wav(ba):
        if args.out:
            write_wav(ba)

    timeout = args.timeout / 1000.0

    if args.loop:
        (n, sz) = calc_size()
        open_fpga(args.port, args.baud, timeout=timeout)
        while True:
            start = int(time.monotonic() * 1000)
            data = call_fpga(sz, n)
            elapsed = int(time.monotonic() * 1000) - start
            remaining = max(args.interval - start, 10)
            if len(data) == (n * sz):
                if args.rgb:
                    show_rgb(data, args.width, args.width)
                    cv2.waitKey(remaining)
                elif args.gray:
                    show_gray(data, args.width, args.width)
                    cv2.waitKey(remaining)
                else:
                    emit(data)
                    time.sleep(remaining / 1000.0)
            else:
                print('Read timeout (%d of %d)' % (len(data),n*sz))
                time.sleep(remaining / 1000.0)
    elif args.width:
        (n, sz) = calc_size()
        open_fpga(args.port, args.baud, timeout=timeout)
        data = call_fpga(sz, n)
        if len(data) == (n * sz):
            if args.rgb:
                show_rgb(data, args.width, args.width)
                cv2.waitKey(0)
            elif args.gray:
                show_gray(data, args.width, args.width)
                cv2.waitKey(0)
            elif args.wav:
                play_wav(data)
            else:
                emit(data)
        else:
            print('Read timeout (%d of %d)' % (len(data),n*sz))
    else:
        ser = open_fpga(args.port, args.baud, timeout=timeout)
        ser.write(b' ')
        while True:
            x = ser.read()
            if len(x):
                emit(x)
            else:
                break

    close_fpga()

if __name__ == '__main__':
    fpgacap()
