"""
This file contains a common database class.
"""

import os
from typing import Any, Dict, List, Optional

import model
import psycopg
from common import get_secret


class Database:
    """
    Database class.
    """

    def __init__(self):
        """
        Constructor for the Database class.

        Raises
        ------
        e
            Will rethrow any exceptions encountered connecting to the database.
        """

        db_user = os.getenv("DB_USER")
        db_name = os.getenv("DB_NAME")
        deploy_type = os.getenv("DEPLOY_TYPE")
        try:
            if deploy_type == "dev":
                db_host = os.getenv("DB_HOST")
                db_port = os.getenv("DB_PORT")
                db_password = get_secret(os.getenv("DB_PWD"))
                conn = psycopg.connect(
                    dbname=db_name,
                    user=db_user,
                    password=db_password,
                    host=db_host,
                    port=db_port,
                )
            else:
                # The production deploy uses a unix socket
                db_password = os.getenv("DB_PWD")
                instance_socket = os.getenv("INSTANCE_SOCKET")
                print(f"instance_socket={instance_socket}")
                conn = psycopg.connect(
                    dbname=db_name,
                    user=db_user,
                    password=db_password,
                    host=instance_socket,  # unix socket path here
                )
            print("Connection successful using manual socket path!")
            self.connection = conn
        except psycopg.OperationalError as e:
            print(f"Database connection failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    def get_base_units(self) -> List[model.BaseUnitQueryResult]:
        """
        This method returns a list of all of the rows in the base_units table.

        Returns
        -------
        List[model.BaseUnitQueryResult]
            A list of all of the rows in the base_units table.
        """
        print("IN Database.get_base_units")
        bu_dict: Dict[Any, Any] = {}
        # Open a cursor to perform database operations
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(
                "select (base_units.id, base_units.name, base_units.location, "
                + "base_units.has_new_mast_bearing, base_units.has_new_feet,"
                + "cameras.name, "
                + "cameras.type) from base_units LEFT OUTER JOIN cameras ON "
                + "base_units.id=cameras.base_unit_ref;"
            )
            # Fetch the results
            for row in cur:
                print(f"row={row}")
                if row[0][1] in bu_dict:
                    bu_results = bu_dict[row[0][1]]
                else:
                    bu_results = model.BaseUnitQueryResult(
                        id=row[0][0],
                        name=row[0][1],
                        location=row[0][2],
                        has_new_mast_bearing=row[0][3],
                        has_new_feet=row[0][4],
                    )
                    bu_dict[row[0][1]] = bu_results
                camera_type = model.CameraType.from_str(row[0][6])
                if camera_type == model.CameraType.FACE_CAMERA:
                    bu_results.face_camera = row[0][5]
                elif camera_type == model.CameraType.LICENSE_PLATE_CAMERA:
                    bu_results.license_plate_camera = row[0][5]
                elif camera_type == model.CameraType.WIDE_SCREEN_CAMERA:
                    bu_results.widescreen_camera = row[0][5]

        print(f"OUT Database.get_base_units: {list(bu_dict.values())}")
        return list(bu_dict.values())

    def get_notes(self, item_type: str, item_ref: int) -> List[model.Notes]:
        """
        This method returns all of the notes associated with a single item.

        Parameters
        ----------
        item_type : str
            The type of item (base unit, camera, or other)
        item_ref : int
            The integer identifier of the object.

        Returns
        -------
        List[model.Notes]
            A list of all of the notes associated with an item.
        """
        print(
            f"IN Database.get_notes. item_type={item_type}; item_ref={item_ref}"
        )
        note_list = []
        # Open a cursor to perform database operations
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(
                f"SELECT * from notes WHERE item_type='{item_type}' AND "
                + f"item_ref={item_ref}"
            )
            # Fetch the results
            for row in cur:
                note = model.Notes(
                    id=row[0],
                    description=row[1],
                    date=row[2],
                    item_type=model.ItemType.from_str(row[3]),
                    item_ref=row[4],
                )
                note_list.append(note)
        print(f"OUT Database.get_notes. note_list={note_list}")
        return note_list

    def get_maintenance_tasks(
        self, item_type: str, item_ref: int
    ) -> List[model.MaintenanceTask]:
        """
        Get all of the maintenance tasks associated with an item.

        Parameters
        ----------
        item_type : str
            The type of item (base unit, camera, or other)
        item_ref : int
            The integer identifier of the item.

        Returns
        -------
        List[model.MaintenanceTask]
            A list of all maintenance tasks associated with an item.
        """
        print("IN Database.get_maintenance_tasks")
        maint_list = []
        # Open a cursor to perform database operations
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(
                f"SELECT * from maintenance WHERE item_type='{item_type}' "
                + f"AND item_ref={item_ref}"
            )
            # Fetch the results
            for row in cur:
                maint_task = model.MaintenanceTask(
                    id=row[0],
                    description=row[1],
                    last_done_date=row[2],
                    item_type=model.ItemType.from_str(row[3]),
                    item_ref=row[4],
                )
                maint_list.append(maint_task)
        print("OUT Database.get_maintenance_tasks")
        return maint_list

    def get_cameras(self) -> List[model.CameraQueryResult]:
        """
        This method returns a list of all cameras.

        Returns
        -------
        List[model.CameraQueryResult]
            a list of all cameras
        """
        # Open a cursor to perform database operations
        print("IN get_cameras")
        camera_list = []
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(
                "select (cameras.id, cameras.name, cameras.type, "
                + "base_units.name, base_units.location) "
                + "from cameras LEFT OUTER join base_units on "
                + "cameras.base_unit_ref = base_units.id;"
            )
            # Fetch the results
            for curr_row in cur:
                row = curr_row[0]
                print(f"row={row}")
                camera_type = model.CameraType.from_str(row[2])
                camera = model.CameraQueryResult(
                    id=row[0],
                    name=row[1],
                    type=camera_type.value,
                    base_unit=row[3],
                    location=row[4],
                )
                camera_list.append(camera)

        print("OUT get_cameras")
        return camera_list

    def get_cameras_for_bu(
        self, base_unit_ref: int
    ) -> List[model.CameraQueryResult]:
        """
        This method returns all of the cameras for a base unit.

        Parameters
        ----------
        base_unit_ref : int
            The integer identifier for the base unit.

        Returns
        -------
        List[model.CameraQueryResult]
            A list of all of the cameras for the base unit.
        """
        # Open a cursor to perform database operations
        camera_list: List[Any] = []
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(
                "select (cameras.id, cameras.name, cameras.type, "
                + "base_units.name, base_units.location) "
                + "from cameras INNER join base_units on "
                + "cameras.base_unit_ref = base_units.id where "
                + f"cameras.base_unit_ref={base_unit_ref}"
            )
            # Fetch the results
            camera_list = []
            for curr_row in cur:
                row = curr_row[0]
                camera_type = model.CameraType.from_str(row[2])
                camera = model.CameraQueryResult(
                    id=row[0],
                    name=row[1],
                    type=camera_type.value,
                    base_unit=row[3],
                    location=row[4],
                )
                camera_list.append(camera)
            return camera_list

        return camera_list

    def get_other_items(self) -> List[model.OtherItemQueryResult]:
        """
        Returns a list of all of the other items.

        Returns
        -------
        List[model.OtherItemQueryResult]
            A list of all of the other items.
        """
        # Open a cursor to perform database operations
        other_list = []
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(
                "select (other_items.id, other_items.name, base_units.name, "
                + "base_units.location) "
                + "from other_items LEFT OUTER join base_units on "
                + "other_items.base_unit_ref = base_units.id;"
            )
            # Fetch the results
            for curr_row in cur:
                row = curr_row[0]
                other = model.OtherItemQueryResult(
                    id=row[0], name=row[1], base_unit=row[2], location=row[3]
                )
                other_list.append(other)

        return other_list

    def get_other_items_for_bu(
        self, base_unit_ref: int
    ) -> List[model.OtherItemQueryResult]:
        """
        Get all of the other items for a base unit.

        Parameters
        ----------
        base_unit_ref : int
            Integer idetifier for the target base unit.

        Returns
        -------
        List[model.OtherItemQueryResult]
            A list of all of the other items for the base unit.
        """
        # Open a cursor to perform database operations
        other_list = []
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(
                "select (other_items.id, other_items.name, base_units.name, "
                + "base_units.location) "
                + "from other_items INNER join base_units on "
                + "other_items.base_unit_ref = base_units.id where "
                + f"other_items.base_unit_ref={base_unit_ref}"
            )
            # Fetch the results
            for curr_row in cur:
                row = curr_row[0]
                other = model.OtherItemQueryResult(
                    id=row[0], name=row[1], base_unit=row[2], location=row[3]
                )
                other_list.append(other)

        return other_list

    def create_base_unit(
        self,
        name: str,
        location: int,
        has_new_mast_bearing: Optional[bool] = False,
        has_new_feet: Optional[bool] = False,
        face_camera: Optional[str] = None,
        license_plate_camera: Optional[str] = None,
        widescreen_camera: Optional[str] = None,
    ):
        """
        Create a base unit in the database.

        Parameters
        ----------
        name : str
            The name of the base unit.
        location : int
            An integer value associated with a location.
        has_new_mast_bearing : Optional[bool], optional
            True if base unit has a new mast bearing.
        has_new_feet : Optional[bool], optional
            True if base unit has a new feet.
        face_camera : Optional[str], optional
            The name of the face camera in the base unit
        license_plate_camera : Optional[str], optional
            The name of the license plate camera in the base unit.
        widescreen_camera : Optional[str], optional
            the name of the widescreen camer in the base unit.
        """
        print("IN create_base_unit")
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute(
                "insert into base_units (name, location, "
                + "has_new_mast_bearing, has_new_feet) "
                + f"values('{name}', {location}, {has_new_mast_bearing}, "
                + f"{has_new_feet})"
            )
            self.connection.commit()

            cursor.execute(
                f"SELECT id from base_units WHERE name='{name}' LIMIT 1"
            )
            record = cursor.fetchone()
            bu_id = record[0]

            if face_camera:
                cursor.execute(
                    f"update cameras set base_unit_ref={bu_id} WHERE "
                    + f"name='{face_camera}'"
                )
                cursor.execute(
                    f"select id from cameras WHERE name='{face_camera}' LIMIT 1"
                )
                record = cursor.fetchone()
                camera_id = record[0]
                cursor.execute(
                    f"update base_units set face_camera_ref={camera_id} "
                    + f"WHERE id={bu_id}"
                )
            if license_plate_camera:
                cursor.execute(
                    f"update cameras set base_unit_ref={bu_id} WHERE "
                    + f"name='{license_plate_camera}'"
                )
                cursor.execute(
                    "select id from cameras WHERE "
                    + f"name='{license_plate_camera}' LIMIT 1"
                )
                record = cursor.fetchone()
                camera_id = record[0]
                cursor.execute(
                    "update base_units set "
                    + f"license_plate_camera_ref={camera_id} WHERE id={bu_id}"
                )
            if widescreen_camera:
                cursor.execute(
                    f"update cameras set base_unit_ref={bu_id} "
                    + f"WHERE name='{widescreen_camera}'"
                )
                cursor.execute(
                    "select id from cameras WHERE "
                    + f"name='{widescreen_camera}' LIMIT 1"
                )
                record = cursor.fetchone()
                camera_id = record[0]
                cursor.execute(
                    "update base_units set "
                    + f"wide_screen_camera_ref={camera_id} WHERE id={bu_id}"
                )
            self.connection.commit()
        print("OUT create_base_unit")

    def create_camera(
        self, name: str, camera_type: str, base_unit: Optional[str] = None
    ):
        """
        Create a camera item in the database.

        Parameters
        ----------
        name : str
            The name of the camera
        camera_type : str
            The type of the camera (ie; face, license plate, widescreen.)
        base_unit : Optional[str], optional
            An integer reference to the base unit where the camera is installed.

        """
        print("IN create_camera")
        with self.connection.cursor() as cursor:
            try:
                # Execute a command
                camera_type_enum = model.CameraType.from_str_value(camera_type)
                cursor.execute(
                    "insert into cameras (name, type) "
                    + f"values('{name}', '{camera_type_enum.name}') "
                    + "RETURNING id"
                )

                record = cursor.fetchone()
                camera_id = record[0]

                if base_unit:
                    cursor.execute(
                        "select id from base_units WHERE "
                        + f"name='{base_unit}' LIMIT 1"
                    )
                    record = cursor.fetchone()
                    bu_id = record[0]

                    cursor.execute(
                        f"update cameras set base_unit_ref={bu_id} "
                        + f"WHERE id={camera_id}"
                    )
                    if camera_type_enum == model.CameraType.FACE_CAMERA:
                        cursor.execute(
                            "update base_units set "
                            + f"face_camera_ref={camera_id} WHERE id={bu_id}"
                        )
                    elif (
                        camera_type_enum
                        == model.CameraType.LICENSE_PLATE_CAMERA
                    ):
                        cursor.execute(
                            "update base_units set "
                            + f"license_plate_camera_ref={camera_id} "
                            + f"WHERE id={bu_id}"
                        )
                    elif (
                        camera_type_enum == model.CameraType.WIDE_SCREEN_CAMERA
                    ):
                        cursor.execute(
                            "update base_units set "
                            + f"wide_screen_camera_ref={camera_id} "
                            + f"WHERE id={bu_id}"
                        )
            except Exception as e:
                # If any statement fails, roll back all changes within
                # the transaction
                self.connection.rollback()
                print(f"Transaction failed: {e}")
                raise e
            finally:
                self.connection.commit()
        print("OUT create_camera")

    def create_other_item(self, name: str, base_unit: Optional[str] = None):
        """
        Create an other item object in the database.

        Parameters
        ----------
        name : str
            The name of the other object.
        base_unit : Optional[str], optional
            The name of the base unit where the item is installed.

        Raises
        ------
        e
        """
        print("IN create_other_item")
        with self.connection.cursor() as cursor:
            try:
                # Execute a command
                cursor.execute(
                    "insert into other_items (name) "
                    + f"values('{name}') RETURNING id"
                )

                record = cursor.fetchone()
                other_id = record[0]
                print(f"other_id={other_id}")

                if base_unit:
                    cursor.execute(
                        f"select id from base_units WHERE name='{base_unit}' "
                        + "LIMIT 1"
                    )
                    record = cursor.fetchone()
                    bu_id = record[0]
                    print(f"bu_id={bu_id}")
                    cursor.execute(
                        f"update other_items set base_unit_ref={bu_id} "
                        + f"WHERE id={other_id}"
                    )
            except Exception as e:
                # If any statement fails, roll back all changes within the
                # transaction
                self.connection.rollback()
                print(f"Transaction failed: {e}")
                raise e
            finally:
                self.connection.commit()

        print("OUT create_other_item")

    def add_maintenance_task(
        self, description: str, last_done: str, item_type: str, item_ref: int
    ) -> None:
        """
        Add a maintenance task to the database.

        Parameters
        ----------
        description : str
            The name of the maintenance task
        last_done : str
            The date the task was last done in string format
        item_type : str
            The type of item the task is associated with.
        item_ref : int
            An integer reference to the associated object.
        """
        print("IN add_maintenance_task")

        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute(
                "insert into maintenance (description, last_done, item_type, "
                + "item_ref) "
                + f"values('{description}', '{last_done}', '{item_type}', "
                + f"{item_ref})"
            )
            self.connection.commit()

        print("OUT add_maintenance_task")

    def add_note(self, description: str, item_type: str, item_ref: int) -> None:
        """
        Add a note to the given item.

        Parameters
        ----------
        description : str
            The text of the note.
        item_type : str
            The type of item associated with the note.
        item_ref : int
            An integer reference to the item assciated with the note.
        """
        print("IN add_note")
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute(
                "insert into notes (description, date, item_type, item_ref) "
                + f"values('{description}', now(), '{item_type}', {item_ref})"
            )
            self.connection.commit()

        print("OUT add_note")

    def delete_note(self, id: int) -> None:
        """
        Delete a note.

        Parameters
        ----------
        id : int
            The integer identifier of the Note object.
        """
        print("IN delete_note")
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute(f"delete from notes where id={id}")
            self.connection.commit()
        print("OUT delete_note")

    def delete_maintenance_task(self, id: int) -> None:
        """
        Delete the maintenance task assocated with the item identified by id.

        Parameters
        ----------
        id : int
            The identifier of the associated item.
        """
        print("IN delete_maintenance_task")
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute(f"delete from maintenance where id={id}")
            self.connection.commit()
        print("OUT delete_maintenance_task")

    def delete_other_item(self, other_id: int) -> None:
        """
        Delete an othe item.

        Parameters
        ----------
        other_id : int
            The identifier of the associated item.
        """
        print("IN delete_other_item")
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute(f"delete from other_items where id={other_id}")
            cursor.execute(
                "delete from notes where item_type="
                + f"'{model.ItemType.OTHER.name}' and item_ref={other_id}"
            )
            cursor.execute(
                "delete from maintenance where item_type="
                + f"'{model.ItemType.OTHER.name}' and item_ref={other_id}"
            )
            self.connection.commit()
        print("OUT delete_other_item")

    def delete_camera(
        self, camera_id: int, type: str, base_unit: Optional[str] = None
    ) -> None:
        """
        Delete a camera object.

        Parameters
        ----------
        camera_id : int
            Integer identifier of the object.
        type : str
            The type of camera (face, widescreen, license plate, etc)
        base_unit : Optional[str], optional
            The base unit where the camera is installed
        """
        print("IN delete_camera")
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute(f"delete from cameras where id={camera_id}")
            cursor.execute(
                "delete from notes where item_type="
                + f"'{model.ItemType.CAMERA.name}' and item_ref={camera_id}"
            )
            cursor.execute(
                "delete from maintenance where item_type="
                + f"'{model.ItemType.CAMERA.name}' and item_ref={camera_id}"
            )
            camera_type = model.CameraType.from_str_value(type)
            if base_unit and camera_type == model.CameraType.FACE_CAMERA:
                cursor.execute(
                    "update base_units set face_camera_ref=NULL where "
                    + f"name='{base_unit}'"
                )
            elif (
                base_unit
                and camera_type == model.CameraType.LICENSE_PLATE_CAMERA
            ):
                cursor.execute(
                    "update base_units set license_plate_camera_ref=NULL "
                    + f"where name='{base_unit}'"
                )
            elif (
                base_unit and camera_type == model.CameraType.WIDE_SCREEN_CAMERA
            ):
                cursor.execute(
                    "update base_units set wide_screen_camera_ref=NULL "
                    + f"where name='{base_unit}'"
                )
            self.connection.commit()
        print("OUT delete_camera")

    def delete_base_unit(
        self,
        bu_id: int,
        face_camera: Optional[str] = None,
        license_plate_camera: Optional[str] = None,
        widescreen_camera: Optional[str] = None,
    ) -> None:
        """
        Deleta a base unit object from the database.

        Parameters
        ----------
        bu_id : int
            An integer identifier of the base unit.
        face_camera : Optional[str], optional
            The name of the face camera installed in the base unit.
        license_plate_camera : Optional[str], optional
            The name of the license plate installed in the base unit
        widescreen_camera : Optional[str], optional
            The name of the wide screen camera installed in the base unit
        """
        print("IN delete_base_unit")
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute(f"delete from base_units where id={bu_id}")
            cursor.execute(
                "delete from notes where item_type="
                + f"'{model.ItemType.BASE_UNIT.name}' and item_ref={bu_id}"
            )
            cursor.execute(
                "delete from maintenance where item_type="
                + f"'{model.ItemType.BASE_UNIT.name}' and item_ref={bu_id}"
            )
            if face_camera:
                cursor.execute(
                    "update cameras set base_unit_ref=NULL where name="
                    + f"'{license_plate_camera}' and type="
                    + f"'{model.CameraType.LICENSE_PLATE_CAMERA.name}'"
                )
            if license_plate_camera:
                cursor.execute(
                    "update cameras set base_unit_ref=NULL where "
                    + f"name='{face_camera}' and type="
                    + f"'{model.CameraType.FACE_CAMERA.name}'"
                )
            if widescreen_camera:
                cursor.execute(
                    "update cameras set base_unit_ref=NULL where "
                    + f"name='{widescreen_camera}' and type="
                    + f"'{model.CameraType.WIDE_SCREEN_CAMERA.name}'"
                )
            cursor.execute(
                "update other_items set base_unit_ref=NULL where "
                + f"base_unit_ref={bu_id}"
            )
            self.connection.commit()
        print("OUT delete_base_unit")

    def update_other_item(self, name: str, base_unit: str) -> None:
        """
        Update select fields of an other item.

        Parameters
        ----------
        name : str
            The name of the other item
        base_unit : str
            The name of the base unit where the item is installed.
        """
        print("IN update_other_item")
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"SELECT id from base_units WHERE name='{base_unit}' LIMIT 1"
            )
            record = cursor.fetchone()
            bu_id = record[0]

            # Execute a command
            cursor.execute(
                f"update other_items set base_unit_ref={bu_id} where "
                + f"name='{name}'"
            )
            self.connection.commit()
        print("OUT update_other_item")

    def update_camera(self, name: str, base_unit: str) -> None:
        """
        Update select information about a camera.

        Parameters
        ----------
        name : str
            The name of the camera.
        base_unit : str
            The name of the base unit where the camera is installed.
        """
        print("IN update_camera")
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"SELECT id from base_units WHERE name='{base_unit}' LIMIT 1"
            )
            record = cursor.fetchone()
            bu_id = record[0]

            # Execute a command
            cursor.execute(
                f"update cameras set base_unit_ref={bu_id} where name='{name}'"
            )
            self.connection.commit()
        print("OUT update_camera")

    def update_base_unit(
        self,
        id: int,
        name: str,
        location: int,
        has_new_feet: bool,
        has_new_mast_bearing: bool,
    ) -> None:
        """
        Update a base unit object

        Parameters
        ----------
        id : int
            An integer identifier of the base unit
        name : str
            The name of the base unit
        location : int
            The location of the base unit
        has_new_feet : bool
            An indicator of if the base unit has new feet
        has_new_mast_bearing : bool
            An indicator of if the base unit has a new mast bearing.
        """
        print("IN update_base_unit")
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute(
                f"update base_units set location={location}, "
                + f"has_new_feet={has_new_feet}, "
                + f"has_new_mast_bearing={has_new_mast_bearing} where id={id}"
            )
            self.connection.commit()
        print("OUT update_base_unit")

    def get_has_new_mast_bearing(self) -> List[model.BaseUnitQueryResult]:
        """
        Returns a list of base units that have a new mast bearing.

        Returns
        -------
        List[model.BaseUnitQueryResult]
            A list of base units with a new mast bearing.
        """
        print("IN Database.get_has_new_mast_bearing")
        bu_dict: Dict[Any, Any] = {}
        # Open a cursor to perform database operations
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(
                "select (base_units.id, base_units.name, base_units.location, "
                + "base_units.has_new_mast_bearing, base_units.has_new_feet,"
                + "cameras.name, "
                + "cameras.type) from base_units LEFT OUTER JOIN cameras ON "
                + "base_units.id=cameras.base_unit_ref WHERE "
                + "base_units.has_new_mast_bearing=true"
            )
            # Fetch the results
            for row in cur:
                print(f"row={row}")
                if row[0][1] in bu_dict:
                    bu_results = bu_dict[row[0][1]]
                else:
                    bu_results = model.BaseUnitQueryResult(
                        id=row[0][0],
                        name=row[0][1],
                        location=row[0][2],
                        has_new_mast_bearing=row[0][3],
                        has_new_feet=row[0][4],
                    )
                    bu_dict[row[0][1]] = bu_results
                camera_type = model.CameraType.from_str(row[0][6])
                print(
                    f"camera_type={camera_type} "
                    + f"{model.CameraType.FACE_CAMERA.name}"
                )
                if camera_type == model.CameraType.FACE_CAMERA:
                    bu_results.face_camera = row[0][5]
                elif camera_type == model.CameraType.LICENSE_PLATE_CAMERA:
                    bu_results.license_plate_camera = row[0][5]
                elif camera_type == model.CameraType.WIDE_SCREEN_CAMERA:
                    bu_results.widescreen_camera = row[0][5]

        print(
            f"OUT Database.get_has_new_mast_bearing: {list(bu_dict.values())}"
        )
        return list(bu_dict.values())

    def get_has_new_feet(self) -> List[model.BaseUnitQueryResult]:
        """
        Returns a list of base units that have new feet.

        Returns
        -------
        List[model.BaseUnitQueryResult]
            A list of base units with new feet.
        """
        print("IN Database.get_has_new_feet")
        bu_dict: Dict[Any, Any] = {}
        # Open a cursor to perform database operations
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(
                "select (base_units.id, base_units.name, base_units.location, "
                + "base_units.has_new_mast_bearing, base_units.has_new_feet,"
                + "cameras.name, "
                + "cameras.type) from base_units LEFT OUTER JOIN cameras ON "
                + "base_units.id=cameras.base_unit_ref WHERE "
                + "base_units.has_new_feet=true"
            )
            # Fetch the results
            for row in cur:
                print(f"row={row}")
                if row[0][1] in bu_dict:
                    bu_results = bu_dict[row[0][1]]
                else:
                    bu_results = model.BaseUnitQueryResult(
                        id=row[0][0],
                        name=row[0][1],
                        location=row[0][2],
                        has_new_mast_bearing=row[0][3],
                        has_new_feet=row[0][4],
                    )
                    bu_dict[row[0][1]] = bu_results
                camera_type = model.CameraType.from_str(row[0][6])
                print(
                    f"camera_type={camera_type} "
                    + f"{model.CameraType.FACE_CAMERA.name}"
                )
                if camera_type == model.CameraType.FACE_CAMERA:
                    bu_results.face_camera = row[0][5]
                elif camera_type == model.CameraType.LICENSE_PLATE_CAMERA:
                    bu_results.license_plate_camera = row[0][5]
                elif camera_type == model.CameraType.WIDE_SCREEN_CAMERA:
                    bu_results.widescreen_camera = row[0][5]

        print(f"OUT Database.get_has_new_feet: {list(bu_dict.values())}")
        return list(bu_dict.values())

    def get_expired_maintenance_tasks(self) -> List[model.MaintenanceTask]:
        """
        Returns a list of maintenance tasks with last done dates >= 6 months.

        Returns
        -------
        List[model.MaintenanceTask]
            A list of maintenance tasks with last done dates >= 6 months.
        """
        print("IN Database.get_expired_maintenance_tasks")
        maint_list = []
        # Open a cursor to perform database operations
        with self.connection.cursor() as cur:
            # Execute a command
            cur.execute(
                "SELECT * from maintenance WHERE last_done <= CURRENT_DATE "
                + "- INTERVAL '6 months'"
            )
            # Fetch the results
            for row in cur:
                item_name = ""
                item_type_enum = model.ItemType.from_str(row[3])
                if item_type_enum == model.ItemType.BASE_UNIT:
                    cur.execute(
                        f"SELECT name from base_units WHERE id='{row[4]}' "
                        + "LIMIT 1"
                    )
                elif item_type_enum == model.ItemType.CAMERA:
                    cur.execute(
                        f"SELECT name from cameras WHERE id='{row[4]}' "
                        + "LIMIT 1"
                    )
                elif item_type_enum == model.ItemType.OTHER:
                    cur.execute(
                        f"SELECT name from other_items WHERE id='{row[4]}' "
                        + "LIMIT 1"
                    )
                record = cur.fetchone()
                item_name = record[0]
                maint_task = model.MaintenanceTaskQueryResult(
                    id=row[0],
                    description=row[1],
                    last_done_date=row[2],
                    item_type=model.ItemType.from_str(row[3]).value,
                    item_name=item_name,
                )
                maint_list.append(maint_task)
        print("OUT Database.get_expired_maintenance_tasks")
        return maint_list

    def complete_maintenance_task(self, id: int) -> None:
        """
        Complete a maintenance task by updating the last done date to the 
        current date (now).

        Parameters
        ----------
        id : int
            The integer identifier of the maintenance task.
        """
        print("IN complete_maintenance_task")
        with self.connection.cursor() as cursor:
            # Execute a command
            cursor.execute(
                f"update maintenance set last_done=now() where id={id}"
            )
            self.connection.commit()
        print("OUT complete_maintenance_task")
