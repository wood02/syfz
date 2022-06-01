def check(content, split_str=","):
    """

    :return:
    """
    port_list = []
    err_list = []
    ports = content.strip().split(split_str)
    for port in ports:
        try:
            port = int(port)
            if 0 <= port <= 65535:
                port_list.append(port)
            else:
                err_list.append(port)
        except ValueError:
            if "-" not in port:
                err_list.append(port)
            else:
                ports_m = port.strip().split("-")
                if len(ports_m) != 2:
                    err_list.append(port)
                else:
                    try:
                        ports_m1 = int(ports_m[0])
                        ports_m2 = int(ports_m[1])
                        if 0 <= ports_m1 <= 65535 and 0 <= ports_m2 <= 65535 and ports_m1 < ports_m2:
                            port_list.append(port)
                        else:
                            err_list.append(port)
                    except ValueError:
                        err_list.append(port)
    return port_list, err_list


if __name__ == '__main__':
    a, b = check("1")
    print(a, b)
