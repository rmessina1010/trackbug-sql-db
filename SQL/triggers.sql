--FUNCTIONS:
	--TECH
CREATE FUNCTION remove_tech()
RETURNS TRIGGER
AS $$
    BEGIN
		UPDATE  skills SET tech = NULL WHERE  tech = OLD.tech_id;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

	--SKILLS *******
CREATE FUNCTION remove_skill()
RETURNS TRIGGER
AS $$
    BEGIN
		DELETE  FROM bug_skills WHERE  skill_id = OLD.skill_id;
		DELETE  FROM dev_skills WHERE  skill_id = OLD.skill_id;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;


	--PROJECT *******
CREATE FUNCTION remove_proj()
RETURNS TRIGGER
AS $$
    BEGIN
		DELETE  FROM reports WHERE  in_project = OLD.proj_id;
		DELETE  FROM bugs WHERE  in_proj = OLD.proj_id;
		--if not cascadable, delete coments on projects
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;


	--BUG *******
CREATE FUNCTION remove_bug()
RETURNS TRIGGER
AS $$
    BEGIN
		DELETE  FROM reports WHERE  defined_as = OLD.bug_id;
		DELETE  FROM comments WHERE  refers_to = OLD.bug_id;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;





--TRIGGERS:
	--TECHS
CREATE TRIGGER tech_rel 
BEFORE DELETE ON  techs
FOR EACH ROW
EXECUTE FUNCTION remove_tech();

	--SKILLS  ******
CREATE TRIGGER skill_rel 
BEFORE DELETE ON  skills
FOR EACH ROW
EXECUTE FUNCTION remove_skill();


	--PROJECTS  ******
CREATE TRIGGER proj_rel 
BEFORE DELETE ON  projects
FOR EACH ROW
EXECUTE FUNCTION remove_proj();


	--BUGS  ******
CREATE TRIGGER bug_rel 
BEFORE DELETE ON  bugs
FOR EACH ROW
EXECUTE FUNCTION remove_bug();


