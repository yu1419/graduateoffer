update applicant set gpa = NULL where gpa = 1 or gpa =2 or gpa =3 or gpa >5.0 and gpa <70 or gpa >100;
update applicant set gre = NULL where gre<300 or gre >340;
update applicant set gre_aw = NULL where gre_aw <2.0 or gre_aw >6;
update applicant set toefl = NULL where toefl>120 or toefl <70;