# hello.py - http://www.graphviz.org/content/hello

from graphviz import Digraph
g = Digraph('G', filename='graph.gv')
g.attr('node', shape='box')


def drawgraph(dict):
    for lb in dict["LoadBalancers"]:
        lbname = lb["LoadBalancerName"]
        lbdnsname = lb["DNSName"]
        Scheme = lb["Scheme"]
        # autres info à intégrer au node : DNSName, Scheme
        for tg in lb["TargetGroups"]:
            tgname = tg["TargetGroupName"]
            Protocol = tg["Protocol"]
            Port = tg["Port"]
            HealthCheckProtocol = tg["HealthCheckProtocol"]
            # autres info à intégrer au node : Protocol, Port, HealthCheckProtocol
            g.edge(lbname,tgname)
            for th in tg["TargetHealthDescriptions"]:
                instance = th["Target"]["Id"]
                ServicePort = th["Target"]["Port"]
                HealthCheckPort = th["HealthCheckPort"]
                TargetHealth = th["TargetHealth"]["State"]
                g.edge(tgname,instance)

if __name__ == '__main__':
    dict = {
    "LoadBalancers": [
            {
            "LoadBalancerArn": "arn:aws:elasticloadbalancing:eu-west-3:362841654686:loadbalancer/app/weblb1/d559c4a8387d887e",
            "DNSName": "weblb1-1903986404.eu-west-3.elb.amazonaws.com",
            "LoadBalancerName": "weblb1",
            "Scheme": "internet-facing",
            "TargetGroups": [
        		{
            		"TargetGroupArn": "arn:aws:elasticloadbalancing:eu-west-3:362841654686:targetgroup/test-lb-1/be96dad79e5b2dbf",
            		"TargetGroupName": "test-lb-1",
            		"Protocol": "HTTP",
            		"Port": 80,
            		"HealthCheckProtocol": "HTTP",
		            "TargetHealthDescriptions": [
			            {
            				"Target": {
                				"Id": "i-0bec0c5070ce13794",
                				"Port": 80
            				},
            				"HealthCheckPort": "80",
            				"TargetHealth": {
                				"State": "healthy"
            				}
        				}
    				]
        		}
		]
	        }
            ]
            }
    drawgraph(dict)
    g.view()


