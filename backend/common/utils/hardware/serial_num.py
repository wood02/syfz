# -*- coding: utf-8 -*-
import subprocess
import platform


def disk():
    serial_num = ''
    if platform.system().lower() == "windows":
        # todo Django调用报错  pywintypes.com_error: (-2147221020, '无效的语法', None, None)
        # import wmi
        # c = wmi.WMI()
        # # # 硬盘序列号
        # for physical_disk in c.Win32_DiskDrive():
        #     serial_num = physical_disk.SerialNumber
        #     break
        serial_num = 'SD0L02320L1TH6510CS8'
    else:
        # lsblk 查看
        lsblk = subprocess.check_output("lsblk", shell=True).decode()
        lsblk = lsblk.strip().split("\n")[1].strip().split(" ")[0]
        shell = "udevadm info --query=all --name=/dev/" + lsblk + " | grep ID_SERIAL"
        serial = subprocess.check_output(shell, shell=True)
        serial = serial.strip().decode()
        serial_num = serial.split('=')[-1]
    return serial_num.upper()


if __name__ == '__main__':
    print(disk())
