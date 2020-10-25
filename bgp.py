from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_config, netmiko_send_command
from nornir_jinja2.plugins.tasks import template_file

def config_bgp(task):

    cmd = task.run(
        task=template_file,
        template="bgp.j2", path="",
        asn=task.host.data['asn'],
        neighbor_addr=task.host.data['neighbor_addr'],
        neighbor_asn=task.host.data['neighbor_asn'],
        networks=task.host.data['networks'],
        GigabitEthernet1=task.host.data['GigabitEthernet1'])
    task.run(
        name='configure bgp',
        task=netmiko_send_config,
        config_commands=cmd.result.split('\n'))
    task.run(
        name='show bgp sum',
        task=netmiko_send_command,
        command_string='show bgp sum')
nr = InitNornir(config_file="./config.yml")
routers = nr.filter(F(groups__contains="csr1000v"))

r = routers.run(config_bgp)
print_result(r)
