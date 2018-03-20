"""pm 2.5"""
import os
import serial
import traceback


def proc():
    """main proc"""
    try:
        s_handle = serial.Serial(port='com4', baudrate=9600, timeout=0.05)
        s_handle.close()
        s_handle.open()
    except Exception:
        traceback.print_exc()
        print('serial open failed.')
        os.system('pause')
        exit()

    while True:
        try:
            re_byte = s_handle.read(1)
        except Exception:
            traceback.print_exc()
            print('serial_run err quit')
            break
        if re_byte == b'\x42':
            re_data = re_byte + s_handle.read(31)
            if len(re_data) != 32:
                print('msg broken.')
            msg_list = [int('{0:02X}'.format(x), 16) for x in re_data]
            fcs = (msg_list[30] << 8) | msg_list[31]
            if sum(msg_list[:30]) != fcs:
                print('fcs err.')
                continue
            # print('standard   pm1.0: {b45}    pm2.5: {b67}    pm10: {b89}'\
            #     .format(b45=(msg_list[4] << 8) | msg_list[5],\
            #             b67=(msg_list[6] << 8) | msg_list[7],\
            #             b89=(msg_list[8] << 8) | msg_list[9]))
            print('pm1.0: {b1011}    pm2.5: {b1213}    pm10: {b1415}'\
                .format(b1011=(msg_list[10] << 8) | msg_list[11],\
                        b1213=(msg_list[12] << 8) | msg_list[13],\
                        b1415=(msg_list[14] << 8) | msg_list[15]))


if __name__ == '__main__':
    proc()
    os.system('pause')
