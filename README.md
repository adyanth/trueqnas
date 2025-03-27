# trueqnas

## Steps

* Privileged, `/dev/`, `/lib/modules`, `/usr/src`
* `apt install -y git make gcc libelf-dev kmod`
* git clone https://github.com/0xGiddi/qnap8528.git && cd qnap8528
* make -C src
* insmod src/qnap8528.ko

