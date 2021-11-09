SELECT *
FROM personel
WHERE person_id IN (
	SELECT assigned_to FROM bugs WHERE in_proj=2
	union 
	SELECT managed_by FROM projects WHERE proj_id=2
)