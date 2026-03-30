UPDATE activity_log
SET description = REPLACE(description, 'Widescreen', 'Windscreen')
WHERE description LIKE '%Widescreen%';

ALTER TABLE base_units RENAME COLUMN wide_screen_camera_ref TO wind_screen_camera_ref;

UPDATE cameras
SET type = REPLACE(type, 'WIDE_SCREEN_CAMERA', 'WIND_SCREEN_CAMERA')
WHERE type = 'WIDE_SCREEN_CAMERA';

UPDATE issues
SET description = REPLACE(description, 'Widescreen', 'Windscreen')
WHERE description LIKE '%Widescreen%';

UPDATE maintenance
SET description = REPLACE(description, 'Widescreen', 'Windscreen')
WHERE description LIKE '%Widescreen%';

UPDATE notes
SET description = REPLACE(description, 'Widescreen', 'Windscreen')
WHERE description LIKE '%Widescreen%';