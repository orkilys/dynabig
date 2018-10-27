
import subprocess
import json
import time


def List_lbs():
    # List_lbs
    lb_push_string = 'aws elbv2 describe-load-balancers'
    print(lb_push_string)
    lb_push = subprocess.check_output(lb_push_string, bufsize=-1, shell=True)
    lb_formed = lb_push.decode('UTF-8')
    load_balancers_all = json.loads(lb_formed)
    '''load_balancers_all is built like \
    {"LoadBalancers" : [lb1, lb2, ..., lbn]} where lbi is a dict''' 
    load_balancers = {} #The returned dictionary
    #  i indexes the list of lbs inside load_balancers_all
    list_of_lb = [{}]
    i = 0
    for lb in load_balancers_all['LoadBalancers']:
        # 1 dictionary for each LB - each "aux" dict is meant to contain the expected key value pair
        aux = {}
        aux["LoadBalancerArn"] = lb["LoadBalancerArn"]
        aux["DNSName"] = lb["DNSName"]
        aux["LoadBalancerName"] = lb["LoadBalancerName"]
        aux["Scheme"] = lb["Scheme"]
        print(aux)
        print(i)
        list_of_lb[i] = aux
        i += 1 #Going to the next lb of the list
    load_balancers["LoadBalancers"] = list_of_lb
    return load_balancers

def list_target_groups(load_balancer):
    '''
    This function lists the target groups belonging to a list of loadbalancers
    Input : Dictionary of Loadbalancers
    Output : Dictionary of Targetgroups
    '''
    tg_push_string = 'aws elbv2 describe-target-groups --load-balancer-arn '+ load_balancer['LoadBalancerArn']
    tg_push = subprocess.check_output(tg_push_string, bufsize=-1, shell=True)
    TargetGroups_all = json.loads(tg_push.decode('UTF-8'))
    TargetGroups = {} #The returned dictionary
    #  i indexes the list of lbs inside load_balancers_all
    list_of_tg = [{}]
    i = 0
    for tg in TargetGroups_all['TargetGroups']:
        # 1 dictionary for each tg - each "aux" dict is meant to contain the expected key value pair
        aux = {}
        aux["TargetGroupArn"] = tg["TargetGroupArn"]
        aux["TargetGroupName"] = tg["TargetGroupName"]
        aux["Protocol"] = tg["Protocol"]
        aux["Port"] = tg["Port"]
        list_of_tg[i] = aux
        i += 1 #Going to the next tg of the list
    TargetGroups['TargetGroups'] = list_of_tg
    return TargetGroups

def list_TargetHealth(TargetGroup):
    '''Lister les instances pour le TG'''
    type(TargetGroup['TargetGroupArn'])
    tgh_string = 'aws elbv2 describe-target-health --target-group-arn '+TargetGroup['TargetGroupArn']
    tgh_push = subprocess.check_output(tgh_string, bufsize=-1, shell=True)
    tgh_all = json.loads(tgh_push.decode('UTF-8'))
    i = 0
    list_of_tgh = [{}]
    TargetHealthDescriptions = {}
    for tgh in tgh_all['TargetHealthDescriptions']:
        # 1 dictionary for each tgh - each "aux" dict is meant to contain the expected key value pair
        aux = {}
        aux["Target"] = tgh["Target"]
        aux["HealthCheckPort"] = tgh["HealthCheckPort"]
        aux["TargetHealth"] = tgh["TargetHealth"]
        list_of_tgh[i] = aux
        i += 1 #Going to the next tgh of the list
    TargetHealthDescriptions['TargetHealthDescriptions'] = list_of_tgh
    return TargetHealthDescriptions

def nested_lbs_tgs_tgh():
    lbs = List_lbs()
    out_dict = {}
    i = 0
    j = 0
    list_of_lbs = []
    list_of_tgs = []
    for lb in lbs["LoadBalancers"]:
        lb["TargetGroups"] = list_target_groups(lb)
        print(lb)
        for tg in lb["TargetGroups"]:
            tg["TargetHealthDescriptions"] = list_TargetHealth(tg)
            list_of_tgs[j] = tg
            j += 1
        lb[i]["TargetGroups"] = list_of_tgs
        list_of_lbs[i] = lb
        i += 1
    out_dict["LoadBalancers"] = list_of_lbs

    return out_dict

def list_instances():
    inst = 'aws ec2 describe-instances'
    print(inst)
    push = subprocess.check_output(inst, bufsize=-1, shell=True)
    out2 = push.decode('UTF-8')
    instances = json.loads(out2)
    print(instances)
    print('\n')
    return instances

def get_aws_info():
    '''
    gets the load balancers, the instances and the instances information
    args :
    returns : 
    dictionnaries : load balancers, instances and instances statuses
    '''
    load_balancers = List_lbs()
    list_target_groups(load_balancers)
    # instances = list_instances()
    
    # print('\n')
    # insta = 'aws ec2 describe-instance-status'
    # print(insta)
    # push2 = subprocess.check_output(insta, bufsize=-1, shell=True)
    # out3 = push2.decode('UTF-8')
    # instances_status = json.loads(out3)
    # # print(instances_status)
    print('\n')
    # return load_balancers, instances, instances_status
    # return load_balancers, instances
    return load_balancers


#out=json.load(push.stdout)


def buildgraph(load_balancers, instances, instances_status):
    from graphviz import Digraph
    g = Digraph('G', filename='mydesign.gv')
    g.attr('node', shape='box')


# Instance

# status
    # az = instances_status['InstanceStatuses'][0]['AvailabilityZone']
    # instance0 = instances_status['InstanceStatuses'][0]['InstanceId']
    # instance0_status = instances_status['InstanceStatuses'][0]['SystemStatus']['Status']


def buildhtml():
    pass

if __name__=='__main__':
    load_balancers = get_aws_info()
    # load_balancers, instances = get_aws_info()
    # load_balancers, instances, instances_status = get_aws_info()
    # buildgraph(load_balancers, instances, instances_status)

