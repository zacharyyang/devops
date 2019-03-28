create table instances(
    id int(11)  primary key auto_increment,
    instance_id  varchar(40) not null,
    hostname varchar(40) not null,
    cpu_corecount int(10),
    instance_type   varchar(40),
    state  varchar(40),
    private_ip_address varchar(40),
    public_ip_address varchar(40),
    subnet_id varchar(40),
    vpc_id varchar(40),
    vender varchar(40),
    project varchar(40)
);

create table volumes(
    id int(11)  primary key auto_increment,
    volume_id  varchar(40) not null,
    attached_instance_id varchar(40),
    attached_device  varchar(40),
    attached_state  varchar(40),
    volume_name    varchar(40),
    volume_type    varchar(40),
    volume_size    int(10),
    iops    int(10),
    state varchar(40),
    zone   varchar(40),
    snapshot_id  varchar(40)
);