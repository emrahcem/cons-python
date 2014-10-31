SAMPLER_MAPPING= {
    'Original': 'Orig',
    'Random Edge Sampling': 'RE',
    'Induced Random Edge Sampling': 'IRE',
    'Induced Random Vertex Sampling' : 'IRV',
    'Random Path Sampling' : 'RP',
    'KK Path Sampling' : 'KK',
    'KM Path Sampling' : 'KM',
    'Metropolized Random Walk Sampling' : 'MRW',
    'Random Vertex Sampling' : 'RV',
    'Random Walk Sampling': 'RW'}

SAMPLER_ORDER={
               'Original':1,
               'Random Vertex Sampling':2,
               'Induced Random Vertex Sampling':3,
               'Random Edge Sampling':4,
               'Induced Random Edge Sampling':5,
               'Random Walk Sampling':6,
               'Metropolized Random Walk Sampling':7,
               'Random Path Sampling':8,
               'KK Path Sampling':9,
               'KM Path Sampling':10
               }

#SAMPLER_ORDER=['RV','IRV','RE','IRE','RW','MRW','RP','KK','KM']

LINE_STYLES = {
    'Original':'k-', 
    'Random Vertex Sampling':'g--', 
    'Induced Random Vertex Sampling':'g-.', 
    'Random Edge Sampling':'b--', 
    'Induced Random Edge Sampling':'b-.', 
    'Random Walk Sampling':'r--', 
    'Metropolized Random Walk Sampling':'r-.', 
    'Random Path Sampling':'y--', 
    'KK Path Sampling':'y-.', 
    'KM Path Sampling':'y:'}

LINE_WIDTHS = {
    'Original':4, 
    'Random Vertex Sampling':1, 
    'Induced Random Vertex Sampling':1, 
    'Random Edge Sampling':1, 
    'Induced Random Edge Sampling':1, 
    'Random Walk Sampling':1, 
    'Metropolized Random Walk Sampling':1, 
    'Random Path Sampling':1, 
    'KK Path Sampling':1, 
    'KM Path Sampling':1}


QUERY_MAPPING={
    'Backend Query':'BE',
    'Frontend Query':'FE',
     }

GRAPH_MAPPING={
    'Barabasi-Albert':'BA',
    'Erdos-Renyi':'ER',
    'Watts-Strogatz':'WS'
     }
