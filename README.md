# TrakBugDB
### _A bug reporting/tracking API_

https://github.com/rmessina1010/trackbug-sql-db

TrakbugDB a the back-end bug reporting and tracking solution. This API will allow you to:
- Register personel
- Create projects
- Define technologies
- Define skills (a level of expertise, combined with a technology)
- Maintain a list of Devs and their corresponding skills
- Report issues on projects
- Define bugs connected to related reported issues and  attach skill requirements to each bug
- Assign Devs to work on bugs
- Comment on bugs
- and of course keep track status of Bugs/Projects


## Features

- All functions listed above have CRUD capabilities
- GET index endpoints employ for query strings;  allowing  you to mix and match parameters to filter the info desired

## Enpoints
##### personel
GET
- _/personel_   ...returns all personel records, can be filtered by any combination of the following params
   - ?fn= first_name
   - ?ln= last_name
   - ?id= person_id
   - ?mng= reports_to
   - ?stat = work_stat
   - ?role = p_role
   - ?age = age
   - ?sex = sex
- _/personel/{id}_  ...retrieves the personel record for the corresponding _id_
PUT
- _/personel/{id}_ ...updates the corresponding personel record any field passed in the body as JSON, except person_id, for the corresponding _id_
DEL/{id}
- _/personel/{id}_ ...deletes the corresponding personel _id_
POST
- _/personel/_ ... creates a new personel 
	- { first_name, last_name, [ reports_to, work_stat,p_role , age, sex ] }

##### projects
GET
- _/projects_   ...returns all project records, can be filtered by any combination of the following params
    - ?name= proj_title
    - ?id= project_id
    - ?mng= managed_by
    - ?stat = proj_status
- _/projects/{id}_  ...retrieves the project record for the corresponding _id_
PUT
- _/projects/{id}_ ...updates the corresponding project record any field passed in the body as JSON, except person_id, for the corresponding _id_
DEL/{id}
- _/projects/{id}_ ...deletes the corresponding project _id_
POST
- _/projects/_ ... creates a new project
	- { proj_title, [ managed_by, proj_status, proj_excerpt ] }


##### reports
GET
- _/reports_   ...returns all report records, can be filtered by any combination of the following params
    - ?sub= subject
    - ?id= report_id
    - ?by= reported_by
    - ?on= reported_on (date, feature pending)
    - ?in = in_project
    - ?bug = defined_as (which bug the reports corresponds to)
- _/reports/{id}_  ...retrieves the report record for the corresponding _id_
PUT
- _/reports/{id}_ ...updates the corresponding report record any field passed in the body as JSON, except report_id  , reported_on, and  in_project for the corresponding _id_
- _/reports/{id}/define_ ...updates the corresponding report record  for the corresponding _id_, sets the  in_project to the value passed in body as JSON; requires user_id in body
DEL/{id}
- _/reports/{id}_ ...deletes the corresponding report _id_; requires user_id in body
POST
- _/reports/_ ... creates a new report  
	- {subject, reported_by, in_project, [description]}
	
##### tech
GET
- _/tech_   ...returns all tech records, can be filtered by any combination of the following params
    - ?name= tech_name
    - ?id= tech_id
- _/tech/{id}_  ...retrieves the tech record for the corresponding _id_
PUT
- _/tech/{id}_ ...updates the corresponding tech record any field passed in the body as JSON, except tech_id   for the corresponding _id_
DEL/{id}
- _/tech/{id}_ ...deletes the corresponding tech _id_
POST
- _/tech/_ ... creates a new tech  
	- {tech_name}
	
##### skill
GET
- _/skills_   ...returns all skill records, can be filtered by any combination of the following params
   - ?lev= lev
   - ?name= skill_name
   - ?id= skill_id
   - ?tech= tech
- _/skills/{id}_  ...retrieves the skill record for the corresponding _id_
PUT
- _/skills/{id}_ ...updates the corresponding skill record any field passed in the body as JSON, except skill_id, for the corresponding _id_
DEL/{id}
- _/skills/{id}_ ...deletes the corresponding skill _id_
POST
- _/skills/_ ... creates a new skill 
	- { lev, name, [tech] }
	
##### bugs
GET
- _/bugs_   ...returns all bug records, can be filtered by any combination of the following params
    - ?stat= bug_status
    - ?id= bug_id
    - ?on= definded_on (date, feature pending)
    - ?dev = assigned_to
    - ?in = in_proj
- _/bugs/{id}_  ...retrieves the bug record for the corresponding _id_
PUT
- _/bugs/{id}_ ...updates the corresponding bug record any field passed in the body as JSON, except bug_id  , buged_on, and  in_project for the corresponding _id_; requires  user_id in in body
- _/bugs/{id}/assigns ...updates the corresponding bug record  for the corresponding _id_, sets the  assigned_to to the value passed in body as JSON ; requires  user_id in in body
DEL/{id}
- _/bugs/{id}_ ...deletes the corresponding bug _id_; requires  user_id in in body
POST
- _/bugs/_ ... creates a new bug  
	- {bug_title, bug_summary, in_project, [assigned_to, bug_status]}

##### comments
GET
- _/comments_   ...returns all comment records, can be filtered by any combination of the following params
    - ?by= comm_author
    - ?id= comment_id
    - ?on= comm_date (date, feature pending)
    - ?abt = refers_to (bug_id)
 - _/comments/{id}_  ...retrieves the comment record for the corresponding _id_
PUT
- _/comments/{id}_ ...updates the corresponding comment record any field passed in the body as JSON, except comment_id   and  comm_date for the corresponding _id_; requires  user_id in in body
DEL/{id}
- _/comments/{id}_ ...deletes the corresponding comment _id_; requires  user_id in in body
POST
- _/comments/_ ... creates a new comment  
	- {comm_author, text, refers_to}

##### dev_skill
GET
- _/personel/skills_   ...returns all skill records can be filtered by:
    - ?personel= person_id
    - ?sk= skill_id
- _/personel/{id}/skills_   ...returns all skill records for the corresponding _id_
DEL/{id}
- _/personel/{id}/skills ...deletes the  corresponding dev-skill requirement for _id_
	- {skill_id}
POST
- _/personel/{id}/skills ... creates a dev-skill requirement for _id_  
	- {skill_id}
	

##### bug_skill
GET
- _/bugs/skills_   ...returns all skill records can be filtered by:
    - ?bug= bug_id
    - ?sk= skill_id
- _/bugs/{id}/skills_   ...returns all skill records for the corresponding _id_
DEL/{id}
- _/bugs/{id}/skills ...deletes the  corresponding bug-skill requirement for _id_
	- {skill_id}

POST
- _/bugs/{id}/skills ... creates a bug-skill requirement for _id_  
	- {skill_id}
