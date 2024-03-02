import mysql.connector as mysql
import snapbase.schemas as schemas

class Database:
    def __init__(self):
        self.db = mysql.connect(
            host="localhost",
            user="root",
            password="root"
        )

        if self.db.is_connected():
            print("Connected to the database!")

        self.mycursor = self.db.cursor()
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS snaptag_db")
        self.mycursor.execute("USE snaptag_db")

        self.mycursor.execute(schemas.IMAGES_SCHEMA)
        self.mycursor.execute(schemas.TAGS_SCHEMA)
        self.mycursor.execute(schemas.IMAGE_TAG_SCHEMA)

        print("Database and tables are ready!")
    

    def insert_image(self, image_path, tags):
        self.mycursor.execute("INSERT INTO images (image_path) VALUES (%s)", (image_path,))
        image_id = self.mycursor.lastrowid

        for tag in tags:
            self.mycursor.execute("SELECT tag_id FROM tags WHERE tag_name = %s", (tag,))
            tag_id = self.mycursor.fetchone()
            if tag_id:
                tag_id = tag_id[0]
            else:
                self.mycursor.execute("INSERT INTO tags (tag_name) VALUES (%s)", (tag,))
                tag_id = self.mycursor.lastrowid
            
            self.mycursor.execute("INSERT INTO image_tags (image_id, tag_id) VALUES (%s, %s)", (image_id, tag_id))
        
        self.db.commit()
        print("Done uploading an image")
        return image_id
    
    def get_images(self, tag):
        self.mycursor.execute("SELECT images.image_id, images.image_path FROM images JOIN image_tags ON images.image_id = image_tags.image_id JOIN tags ON tags.tag_id = image_tags.tag_id WHERE tags.tag_name = %s", (tag,))
        images_list = self.mycursor.fetchall()
        print(images_list)
        return images_list

    def get_recent_images(self):
        self.mycursor.execute("SELECT image_id, image_path FROM images ORDER BY created_at DESC LIMIT 5")
        images_list = self.mycursor.fetchall()
        return images_list

    def get_favorite_images(self):
        self.mycursor.execute("SELECT image_id, image_path FROM images WHERE favorite = TRUE")
        images_list = self.mycursor.fetchall()
        return images_list
    
    def delete_image(self, image_id):
        self.mycursor.execute("DELETE FROM images WHERE image_id = %s", (image_id,))
        self.db.commit()
        print("Done deleting an image")
    
    def drop_tables(self):
        self.mycursor.execute("DROP TABLE image_tags")
        self.mycursor.execute("DROP TABLE images")
        self.mycursor.execute("DROP TABLE tags")
        print("Done dropping tables")
    
    def create_tables(self):
        self.mycursor.execute(schemas.IMAGES_SCHEMA)
        self.mycursor.execute(schemas.TAGS_SCHEMA)
        self.mycursor.execute(schemas.IMAGE_TAG_SCHEMA)
        print("Done creating tables")
    
    def set_favorite(self, image_id):
        self.mycursor.execute("UPDATE images SET favorite = TRUE WHERE image_id = %s", (image_id,))
        self.db.commit()
        print("Done setting favorite")