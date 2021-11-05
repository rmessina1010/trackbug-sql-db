-- create the database
DROP DATABASE IF EXISTS bugtrak_db;
CREATE DATABASE bugtrak_db;
-- connect via psql
\c bugtrak_db

-- database configuration
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;


---
--- CREATE tables
---

CREATE TABLE personel (
    person_id SERIAL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    reports_to INT,
    p_role VARCHAR(255),
	work_stat VARCHAR(32),
    age   SMALLINT,
    sex   VARCHAR(32),
    PRIMARY KEY(person_id)
);


CREATE TABLE projects (
    proj_id SERIAL,
    managed_by INT,
    proj_title  VARCHAR(255) NOT NULL,
    proj_status VARCHAR(255) NOT NULL DEFAULT 'Pending/Limbo',
    proj_excerpt TEXT,
    CONSTRAINT fk_manager FOREIGN KEY (managed_by) REFERENCES personel (person_id) ON DELETE SET NULL,
    PRIMARY KEY(proj_id)
);



CREATE TABLE techs (
    tech_id SERIAL,
    tech_name VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY(tech_id)
);


CREATE TABLE skills (
    skill_id SERIAL,
    tech INT,
    skill_name VARCHAR(255) NOT NULL UNIQUE,
    lev SMALLINT DEFAULT 1 ,
    PRIMARY KEY(skill_id),
    CONSTRAINT fk_tech FOREIGN KEY (tech) REFERENCES techs (tech_id) ON DELETE SET NULL
);


CREATE TABLE dev_skills (
    person_id INT,
    skill_id INT,
    CONSTRAINT fk_dev FOREIGN KEY (person_id) REFERENCES personel (person_id) ON DELETE CASCADE,
    CONSTRAINT fk_skill FOREIGN KEY (skill_id) REFERENCES skills (skill_id) ON DELETE CASCADE,
    PRIMARY KEY(person_id , skill_id)
);


CREATE TABLE bugs (
    bug_id SERIAL,
    bug_title VARCHAR(255) NOT NULL,
    bug_summary TEXT NOT NULL,
    bug_status VARCHAR(255),
    in_proj INT NOT NULL,
    bug_weight INT NOT NULL DEFAULT 1,
    assigned_to INT,
    defined_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_project FOREIGN KEY (in_proj) REFERENCES projects (proj_id) ON DELETE CASCADE,
    CONSTRAINT fk_dev FOREIGN KEY (assigned_to) REFERENCES personel (person_id) ON DELETE SET NULL ,
    PRIMARY KEY(bug_id)
);

CREATE TABLE reports (
    report_id SERIAL,
    reported_by INT NOT NULL,
    reported_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subject VARCHAR(255) NOT NULL,
    description TEXT,
    in_project INT NOT NULL,
    defined_as  INT,
    CONSTRAINT fk_project FOREIGN KEY (in_project) REFERENCES projects (proj_id) ON DELETE CASCADE,
    CONSTRAINT fk_bug FOREIGN KEY (defined_as) REFERENCES bugs (bug_id) ON DELETE CASCADE,
    CONSTRAINT fk_reporter FOREIGN KEY (reported_by) REFERENCES personel (person_id) ON DELETE SET NULL,
    PRIMARY KEY(report_id)
);



CREATE TABLE bug_skills (
    bug_id INT,
    skill_id INT,
    CONSTRAINT fk_bug FOREIGN KEY (bug_id) REFERENCES bugs (bug_id) ON DELETE CASCADE,
    CONSTRAINT fk_skill FOREIGN KEY (skill_id) REFERENCES skills (skill_id) ON DELETE CASCADE,
    PRIMARY KEY(bug_id , skill_id)
);


CREATE TABLE comments (
    comment_id SERIAL,
    text TEXT NOT NULL,
    comm_author INT NOT NULL,
    refers_to INT NOT NULL,
    comm_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_author FOREIGN KEY (comm_author) REFERENCES personel (person_id) ON DELETE SET NULL,
    CONSTRAINT fk_refers_to FOREIGN KEY (refers_to ) REFERENCES bugs (bug_id) ON DELETE CASCADE,
    PRIMARY KEY(comment_id)
);
