drop trigger if exists update_person ;
DELIMITER $$

CREATE
    TRIGGER update_person BEFORE INSERT
    ON applicant
    FOR EACH ROW
    BEGIN


    IF NEW.gpa =1 or NEW.gpa=2 or NEW.gpa =3 or NEW.gpa >5.0 or NEW.gpa <2.5 and NEW.gpa <70 or NEW.gpa >100 THEN
        set NEW.gpa = NULL;
    END IF;
    IF NEW.gre<300 or NEW.gre >340 THEN
        set NEW.gre = NULL;
    END IF;
    IF NEW.gre_aw <2.0 or NEW.gre_aw >6 THEN
        set NEW.gre_aw = NULL;
    END IF;
    IF NEW.toefl>120 or NEW.toefl <70 THEN
        set NEW.toefl = NULL;
    END IF;
    END$$

DELIMITER ;


drop trigger if exists TRIGGER_person ;
DELIMITER $$

CREATE
    TRIGGER TRIGGER_person BEFORE UPDATE
    ON applicant
    FOR EACH ROW
    BEGIN
    IF NEW.gpa =1 or NEW.gpa=2 or NEW.gpa =3 or NEW.gpa >5.0 or NEW.gpa <2.5 and NEW.gpa <70 or NEW.gpa >100 THEN
        set NEW.gpa = NULL;
    END IF;
    IF NEW.gre<300 or NEW.gre >340 THEN
        set NEW.gre = NULL;
    END IF;
    IF NEW.gre_aw <2.0 or NEW.gre_aw >6 THEN
        set NEW.gre_aw = NULL;
    END IF;
    IF NEW.toefl>120 or NEW.toefl <70 THEN
        set NEW.toefl = NULL;
    END IF;
    END$$

DELIMITER ;
