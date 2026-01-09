import os
import psycopg

from psycopg.rows import class_row
from common import get_secret
from model import BaseUnitQueryResult, Notes, CameraType, ItemType, CameraQueryResult, OtherQueryResult
from model import  MaintenanceTask, Status
from typing import List
from datetime import datetime

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        This method is executed when a new instance is instantiated.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Constructor for the Database class.

        Raises
        ------
        e
            Will rethrow any exceptions encountered connecting to the database.
        """

        db_user = os.getenv("DB_USER")
        db_password = get_secret(os.getenv("DB_PWD"))
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        self.database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        if not hasattr(self, '_connection'):
            try:
                # Use a 'with' statement to ensure the connection is closed automatically
                conn = psycopg.connect(self.database_url)
                setattr(self, '_connection', conn)
                self.connection = conn
            except psycopg.OperationalError as e:
                print(f"Database connection failed: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            self.connection = getattr(self, '_connection')

    def get_business_units(self) -> List[BaseUnitQueryResult]:
        print("IN Database.get_business_units")
        bu_dict = {}
        # Open a cursor to perform database operations
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute("select (base_units.id, base_units.name, base_units.location, " +
                        "base_units.has_new_mast_bearing, base_units.has_new_feet,cameras.name, " +
                        "cameras.type) from base_units LEFT OUTER JOIN cameras ON " + 
                        "base_units.id=cameras.base_unit_ref;")
            # Fetch the results
            for row in cur:
                print(f"row={row}")
                if row[0][1] in bu_dict:
                    bu_results = bu_dict[row[0][1]]
                else:
                    bu_results = BaseUnitQueryResult(id=row[0][0], 
                                                     name=row[0][1], 
                                                     location=row[0][2],
                                                     has_new_mast_bearing=row[0][3],
                                                     has_new_feet=row[0][4])
                    bu_dict[row[0][1]] = bu_results
                camera_type = CameraType.from_str(row[0][6])
                print(f"camera_type={camera_type} {CameraType.FACE_CAMERA.name}")
                if camera_type == CameraType.FACE_CAMERA:
                    bu_results.face_camera = row[0][5]
                elif camera_type == CameraType.LICENSE_PLATE_CAMERA:
                    bu_results.license_plate_camera = row[0][5]
                elif camera_type == CameraType.WIDE_SCREEN_CAMERA:
                    bu_results.widescreen_camera= row[0][5]

        print(f"OUT Database.get_business_units: {list(bu_dict.values())}")
        return list(bu_dict.values())
    

    def get_notes(self, item_type: str, item_ref: int) -> List[Notes]:
        print(f"IN Database.get_notes. item_type={item_type}; item_ref={item_ref}")
        note_list = []
        # Open a cursor to perform database operations
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(f"SELECT * from notes WHERE item_type='{item_type}' AND item_ref='{item_ref}'")
            # Fetch the results
            for row in cur:
                note = Notes(id=row[0], description=row[1], date=row[2], item_type=ItemType.from_str(row[3]), item_ref=row[4])
                note_list.append(note)
        print(f"OUT Database.get_notes. note_list={note_list}")
        return note_list
    
    def get_maintenance_tasks(self, item_type: str, item_ref: int) -> List[MaintenanceTask]:
        print("IN Database.get_maintenance_tasks")
        maint_list = []
        # Open a cursor to perform database operations
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(f"SELECT * from maintenance WHERE item_type='{item_type}' AND item_ref='{item_ref}'")
            # Fetch the results
            for row in cur:
                maint_task = MaintenanceTask(id=row[0], 
                                             description=row[1], 
                                             status=Status.from_str(row[2]), 
                                             last_done_date=row[3], 
                                             item_type=ItemType.from_str(row[4]), 
                                             item_ref=row[5])
                maint_list.append(maint_task)
        print("OUT Database.get_maintenance_tasks")
        return maint_list
    
    def get_cameras(self) -> List[CameraQueryResult]:
        # Open a cursor to perform database operations
        print("IN get_cameras")
        camera_list = []
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute("select (cameras.id, cameras.name, cameras.type, base_units.name, base_units.location) " + 
                        "from cameras LEFT OUTER join base_units on " + 
                        "cameras.base_unit_ref = base_units.id;")
            # Fetch the results
            for curr_row in cur:
                row = curr_row[0]
                print(f"row={row}")
                camera_type = CameraType.from_str(row[2])
                camera = CameraQueryResult(id=row[0], name=row[1], type=camera_type.value, base_unit=row[3], location=row[4])
                camera_list.append(camera)        

        print("OUT get_cameras")
        return camera_list
    
    def get_cameras_for_bu(self, base_unit_ref: int) -> List[CameraQueryResult]:
        # Open a cursor to perform database operations
        camera_list = []
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute("select (cameras.id, cameras.name, cameras.type, base_units.name, base_units.location) " +
                        "from cameras INNER join base_units on " + 
                        f"cameras.base_unit_ref = base_units.id where cameras.base_unit_ref={base_unit_ref}")
            # Fetch the results
            camera_list = []
            for curr_row in cur:
                row = curr_row[0]
                camera_type = CameraType.from_str(row[2])
                camera = CameraQueryResult(id=row[0], name=row[1], type=camera_type.value, base_unit=row[3], location=row[4])
                camera_list.append(camera)
            return camera_list  

        return camera_list
    
    def get_other_items(self) -> List[OtherQueryResult]:
        # Open a cursor to perform database operations
        other_list = []
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute("select (other_items.id, other_items.name, base_units.name, base_units.location) " +
                        "from other_items LEFT OUTER join base_units on " +
                        "other_items.base_unit_ref = base_units.id;")
            # Fetch the results
            for curr_row in cur:
                row = curr_row[0]
                other = OtherQueryResult(id=row[0], name=row[1], base_unit=row[2], location=row[3])
                other_list.append(other)

        return other_list
    
    def get_other_items_for_bu(self, base_unit_ref: int) -> List[OtherQueryResult]:
        # Open a cursor to perform database operations
        other_list = []
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute("select (other_items.id, other_items.name, base_units.name, base_units.location) " +
                        "from other_items INNER join base_units on " +
                        f"other_items.base_unit_ref = base_units.id where other_items.base_unit_ref={base_unit_ref}")
            # Fetch the results
            for curr_row in cur:
                row = curr_row[0]
                other = OtherQueryResult(id=row[0], name=row[1], base_unit=row[2], location=row[3])
                other_list.append(other)

        return other_list
    
    def create_base_unit(self, 
                         name: str, 
                         location: int, 
                         has_new_mast_bearing: bool, 
                         has_new_feet: bool, 
                         face_camera: str = None,
                         license_plate_camera: str = None,
                         widescreen_camera: str = None):
        print("IN create_base_unit")
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute("insert into base_units (name, location, has_new_mast_bearing, has_new_feet) " +
                        f"values('{name}', {location}, {has_new_mast_bearing}, {has_new_feet})")
            self.connection.commit()

            cursor.execute(f"SELECT id from base_units WHERE name='{name}' LIMIT 1")
            record = cursor.fetchone()
            bu_id = record[0]

            if face_camera:
                cursor.execute(f"update cameras set base_unit_ref={bu_id} WHERE name='{face_camera}'")
                cursor.execute(f"select id from cameras WHERE name='{face_camera}' LIMIT 1")
                record = cursor.fetchone()
                camera_id = record[0]
                cursor.execute(f"update base_units set face_camera_ref={camera_id} WHERE id={bu_id}")
            if license_plate_camera:
                cursor.execute(f"update cameras set base_unit_ref={bu_id} WHERE name='{license_plate_camera}'")
                cursor.execute(f"select id from cameras WHERE name='{license_plate_camera}' LIMIT 1")
                record = cursor.fetchone()
                camera_id = record[0]
                cursor.execute(f"update base_units set license_plate_camera_ref={camera_id} WHERE id={bu_id}")
            if widescreen_camera:
                cursor.execute(f"update cameras set base_unit_ref={bu_id} WHERE name='{widescreen_camera}'")
                cursor.execute(f"select id from cameras WHERE name='{widescreen_camera}' LIMIT 1")
                record = cursor.fetchone()
                camera_id = record[0]
                cursor.execute(f"update base_units set wide_screen_camera_ref={camera_id} WHERE id={bu_id}")
            self.connection.commit()
        print("OUT create_base_unit")

    def create_camera(self, 
                     name: str, 
                     camera_type: str,
                     base_unit: str = None):
        print("IN create_camera")
        with self.connection.cursor() as cursor:
            # Execute a command
            camera_type_enum = CameraType.from_str_value(camera_type)
            cursor.execute("insert into cameras (name, type) " + 
                           f"values('{name}', '{camera_type_enum.name}')")
            self.connection.commit()

            cursor.execute(f"SELECT id from  cameras WHERE name='{name}' LIMIT 1")
            record = cursor.fetchone()
            camera_id = record[0]

            if base_unit:
                cursor.execute(f"select id from base_units WHERE name='{base_unit}' LIMIT 1")
                record = cursor.fetchone()
                bu_id = record[0]

                cursor.execute(f"update cameras set base_unit_ref={bu_id} WHERE id={camera_id}")
                self.connection.commit()

                if camera_type_enum == CameraType.FACE_CAMERA:
                    cursor.execute(f"update base_units set face_camera_ref={camera_id} WHERE id={bu_id}")
                    self.connection.commit()
                elif camera_type_enum == CameraType.LICENSE_PLATE_CAMERA:
                    cursor.execute(f"update base_units set license_plate_camera_ref={camera_id} WHERE id={bu_id}")
                    self.connection.commit()
                elif camera_type_enum == CameraType.WIDE_SCREEN_CAMERA:
                    cursor.execute(f"update base_units set wide_screen_camera_ref={camera_id} WHERE id={bu_id}")
                    self.connection.commit()
        print("OUT create_camera")
    
    def create_other_item(self, name: str, base_unit: str = None):
        print("IN create_other_item")
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute("insert into other_items (name) " + 
                           f"values('{name}')")
            self.connection.commit()

            cursor.execute(f"SELECT id from other_items  WHERE name='{name}' LIMIT 1")
            record = cursor.fetchone()
            other_id = record[0]

            if base_unit:
                cursor.execute(f"select id from base_units WHERE name='{base_unit}' LIMIT 1")
                record = cursor.fetchone()
                bu_id = record[0]

                cursor.execute(f"update other_items set base_unit_ref={bu_id} WHERE id={other_id}")
                self.connection.commit()

        print("OUT create_other_item")

    def add_maintenance_task(self, description: str, status: str, last_done: str, item_type: str, item_ref: int) -> None:
        print("IN add_maintenance_task")

        status_enum = Status.from_str_value(status)
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute("insert into maintenance (description, status, last_done, item_type, item_ref) " +
                           f"values('{description}', '{status_enum.name}', '{last_done}', '{item_type}', {item_ref})")
            self.connection.commit()

        print("OUT add_maintenance_task")
    
    def add_note(self, description: str, item_type: str, item_ref: int) -> None:
        print("IN add_note")
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute("insert into notes (description, date, item_type, item_ref) " +
                           f"values('{description}', now(), '{item_type}', {item_ref})")
            self.connection.commit()

        print("OUT add_note")