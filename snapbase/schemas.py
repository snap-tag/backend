'''
This file contains the schema for the database tables in raw strings.

Images: image_id primarykey, image_path, favorite bool, created_at, updated_at
Tags: tag_id primarykey, tag_name
ImageTags: image_id, tag_id
'''

IMAGES_SCHEMA = '''
CREATE TABLE IF NOT EXISTS images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    image_path VARCHAR(255),
    favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
'''

TAGS_SCHEMA = '''
CREATE TABLE IF NOT EXISTS tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(255)
)
'''

IMAGE_TAG_SCHEMA = '''
CREATE TABLE IF NOT EXISTS image_tags (
    image_id INT,
    tag_id INT,
    FOREIGN KEY (image_id) REFERENCES images(image_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
)
'''