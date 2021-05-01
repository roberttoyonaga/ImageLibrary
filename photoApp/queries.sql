-- find all images with a set of tags
SELECT photoID 
FROM Tags 
JOIN PhotoTags using(tagID) 
JOIN Photos using(photoID) 
GROUP BY photoID
HAVING SUM(CASE WHEN Photos.ownerID = 'someID' THEN 1 ELSE 0 END) > 0 AND
        SUM(CASE WHEN Tags.tagName = 'flower' THEN 1 ELSE 0 END) > 0 AND
       SUM(CASE WHEN Tags.tagName = 'life' THEN 1 ELSE 0 END) > 0 AND
       SUM(CASE WHEN Tags.tagName = 'unknown' THEN 1 ELSE 0 END) = 0;