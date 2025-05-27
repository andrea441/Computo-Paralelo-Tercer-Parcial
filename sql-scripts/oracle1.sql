insert into sucursal	values ('S0001', 'Downtown',		'Brooklyn',	 	900000, 'A');
insert into sucursal	values ('S0002', 'Redwood',		'Palo Alto',	2100000, 'A');
insert into sucursal	values ('S0003', 'Perryridge',	'Horseneck',	1700000, 'A');
insert into sucursal	values ('S0004', 'Mianus',		'Horseneck',	 400200, 'A' );

insert into prestamo	values ('L-17',		'S0001',	1000);
insert into prestamo	values ('L-23',		'S0002',	2000);
insert into prestamo	values ('L-15',		'S0003',	1500);
insert into prestamo	values ('L-14',		'S0001',	1500);
insert into prestamo	values ('L-93',		'S0004',	500);
insert into prestamo	values ('L-16',		'S0003',	1300);

COMMIT;