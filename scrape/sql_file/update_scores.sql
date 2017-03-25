update person set gpa = NULL where gpa = 1 or gpa =2 or gpa =3 or gpa >5.0 and gpa <70 or gpa >100;
update person set gre = NULL where gre<300 or gre >340;
update person set gre_aw = NULL where gre_aw <2.0 or gre_aw >6;
update person set toefl = NULL where toefl>120 or toefl <70 and toefl >10;