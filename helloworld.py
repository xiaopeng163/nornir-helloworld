from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir.core.filter import F


def hello_world(task):
    
    task.run(
        name='show ip inter brief',
        task=netmiko_send_command,
        command_string='show ip inter brief')
    task.run(
        name='show bgp sum',
        task=netmiko_send_command,
        command_string='show bgp sum')

nr = InitNornir(config_file="./config.yml")

routers = nr.filter(F(groups__contains="csr1000v"))

r = routers.run(hello_world)
print_result(r)
