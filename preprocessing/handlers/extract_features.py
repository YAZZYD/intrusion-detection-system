import numpy as np
import pandas as pd
from scapy.all import *
from scapy.layers.inet import IP, TCP,UDP

def extract_features(pcap_file:str)->pd.DataFrame:
    print(f"Processing {pcap_file}...")
    packets = rdpcap(pcap_file)
    features= []
    flows={}
    for packet in packets:
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            proto = packet[IP].proto
            if TCP in packet:
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                flow_id = f"{src_ip}:{src_port}-{dst_ip}:{dst_port}-TCP"
            elif UDP in packet:
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
                flow_id = f"{src_ip}:{src_port}-{dst_ip}:{dst_port}-UDP"
            else:
                continue
            packet_info={
                'timestamp':packet.time,
                'size':len(packet)
            }

        

            if flow_id not in flows:
                flows[flow_id]={
                    'src_ip':src_ip,
                    'dst_ip':dst_ip,
                    'protocol':None,
                    'tcp_packets':0,
                    'udp_packets':0,
                    'packets':[packet_info],
                    'start_time':packet.time,
                    'bytes':len(packet),
                    'packet_count':1
                }
            else:
                flows[flow_id]['packets'].append(packet_info)
                flows[flow_id]['bytes']+=len(packet)
                flows[flow_id]['packet_count']+=1
            if proto == 6: #TCP
                flows[flow_id]['tcp_packets']+=1
            elif proto ==17: #UDP
                flows[flow_id]['udp_packets']+=1

    for flow_id,flow in flows.items():
        if len(flow['packets'])<3:
            continue
        
        src_ip = flow['src_ip']
        dst_ip = flow['dst_ip']
        protocol = 'TCP' if flow['tcp_packets'] > flow['udp_packets'] else 'UDP'
        duration = flow['packets'][-1]['timestamp'] - flow['start_time']
        if duration == 0:
            duration = 0.001
        
        packet_sizes = [packet['size'] for packet in flow['packets']]
        inter_arrival_times =[]
        for i in range(1,len(flow['packets'])):
            iat = float(flow['packets'][i]['timestamp'] - flow['packets'][i-1]['timestamp'])
            inter_arrival_times.append(iat)
        flow_features ={
            'flow_id':flow_id,
            'src_ip':src_ip,
            'dst_ip':dst_ip,
            'protocol':protocol,
            'duration':float(duration),
            'packet_count':int(flow['packet_count']),  
            'bytes':int(flow['bytes']),
            'packets_per_second':float(flow['bytes'] / duration),
            'bytes_per_second': float(flow['bytes'] / duration),
            'avg_packet_size': float(np.mean(packet_sizes)),
            'std_packet_size': float(np.std(packet_sizes)),
            # 'min_packet_size': int(np.min(packet_sizes)),
            # 'max_packet_size': int(np.max(packet_sizes))
            }


    if len(inter_arrival_times) > 0:
        flow_features.update({
            'avg_inter_arrival_times': float(np.mean(inter_arrival_times)),
            'std_inter_arrival_times': float(np.std(inter_arrival_times)),
            # 'min_inter_arrival_times': float(np.min(inter_arrival_times)),
            # 'max_inter_arrival_times': float(np.max(inter_arrival_times)),
        })
    else:
        flow_features.update({
            'avg_inter_arrival_times': 0,
            'std_inter_arrival_times': 0,
            # 'min_inter_arrival_times': 0,
            # 'max_inter_arrival_times': 0,
        })
        
    features.append(flow_features)
    return pd.DataFrame(features)
