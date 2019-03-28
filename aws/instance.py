# -*- coding: utf-8 -*-
# * Author        : Zachary  mail : zachary_yzh@126.com
# * Create time   : 2019-03-27 22:42
# * Description   :
import boto3
from conf import *
from db import *


class Instance():
    def __init__(self):
        self.region_name = REGION_NAME
        self.aws_access_key_id = ACCESS_KEY
        self.aws_secret_access_key = SECRET_KEY

    # 调用describe_instances函数,使用for循环去除无关信息，保留instance的各个属性并格式化,
    # 返回值是格式化后所有instance的list,单个instance为一个dict
    def instanceDetail(self):
        client = boto3.client("ec2", region_name=self.region_name, aws_access_key_id=self.aws_access_key_id,
                              aws_secret_access_key=self.aws_secret_access_key)
        response = client.describe_instances()
        instance_list = []
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                if 'PublicIpAddress' not in instance.keys():
                    instance['PublicIpAddress'] = ''
                if instance['State']['Name'] == 'terminated':
                    break
                detail = {
                    'instance_id': instance['InstanceId'],
                    'hostname': instance['Tags'][0]['Value'],
                    'cpu_corecount': instance['CpuOptions']['CoreCount'] * instance['CpuOptions']['ThreadsPerCore'],
                    'instance_type': instance['InstanceType'],
                    'state': instance['State']['Name'],
                    'private_ip_address': instance['PrivateIpAddress'],
                    'public_ip_address': instance['PublicIpAddress'],
                    'subnet_id': instance['SubnetId'],
                    'vpc_id': instance['VpcId']
                }
                instance_list.append(detail)

        return instance_list

    def volumeDetail(self):
        client = boto3.client("ec2", region_name=self.region_name, aws_access_key_id=self.aws_access_key_id,
                              aws_secret_access_key=self.aws_secret_access_key)
        response = client.describe_volumes()
        volumes_list = []
        for volume in response["Volumes"]:
            if 'Tags' not in volume.keys():
                volume['Tags'] = []
                volume['Tags'].append({'Value': ''})
            if 'Iops' not in volume.keys():
                volume['Iops'] = 0
            detail = {
                'volume_id': volume['VolumeId'],
                'attached_instance_id': volume['Attachments'][0]['InstanceId'],
                'attached_device': volume['Attachments'][0]['Device'],
                'attached_state': volume['Attachments'][0]['State'],
                'volume_name': volume['Tags'][0]['Value'],
                'volume_type': volume['VolumeType'],
                'volume_size': volume['Size'],
                'iops': volume['Iops'],
                'state': volume['State'],
                'zone': volume['AvailabilityZone'],
                'snapshot_id': volume['SnapshotId']
            }
            volumes_list.append(detail);
        return volumes_list


if __name__ == '__main__':
    ec2 = Instance()
    ec2detail = ec2.instanceDetail()
    db = MySQL()
    db.execNonQuery('truncate table instances; ')
    db.execNonQuery('truncate table volumes; ')
    for x in range(len(ec2detail)):
        sql = "INSERT INTO instances (id,instance_id,hostname,cpu_corecount,instance_type," + \
              "state,private_ip_address,public_ip_address,subnet_id,vpc_id,project,vender ) value(" + \
              str(x + 1) + ",'" + ec2detail[x]['instance_id'] + "','" + \
              ec2detail[x]['hostname'] + "'," + str(ec2detail[x]['cpu_corecount']) + ",'" + \
              ec2detail[x]['instance_type'] + "','" + ec2detail[x]['state'] + "','" + \
              ec2detail[x]['private_ip_address'] + "','" + ec2detail[x]['public_ip_address'] + "','" + \
              ec2detail[x]['subnet_id'] + "','" + ec2detail[x]['vpc_id'] + "','af','AWS');"

        db.execNonQuery(sql)
        #    print(x)

        print(sql)

    volumedetail = ec2.volumeDetail()
    for x in range(len(volumedetail)):
        v_sql = '''
        INSERT INTO volumes (volume_id,attached_instance_id,attached_device,attached_state,volume_name,volume_type,\
        volume_size,iops,state,zone,snapshot_id) \
        values ("%s", "%s", "%s","%s", "%s", "%s", %s, %s,"%s", "%s", "%s")''' % \
                (volumedetail[x]['volume_id'], volumedetail[x]['attached_instance_id'],\
                 volumedetail[x]['attached_device'],volumedetail[x]['attached_state'], \
                 volumedetail[x]['volume_name'], volumedetail[x]['volume_type'], \
                 volumedetail[x]['volume_size'], volumedetail[x]['iops'], \
                 volumedetail[x]['state'], volumedetail[x]['zone'],volumedetail[x]['snapshot_id'])

        db.execNonQuery(v_sql)
        #print(v_sql)