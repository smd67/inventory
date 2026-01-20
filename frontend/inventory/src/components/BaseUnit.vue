<!--
This file is the vue component implementation of the base units details screen.
The screen shows all of the data associated with a base unit including any
cameras, notes, other items, or maintenance tasks.
 -->
<template>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div class="outer-div">
    <v-container class="table-container">
      <v-row>
        <div style="color: green; font-size: 24px;">
          <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
          Base Unit Details
        </div>
      </v-row>
      <v-row style="border: 1px solid green;">
        <v-sheet class="pa-4 text-right detail-sheet">
          <v-form>
            <v-text-field
              v-model="name"
              label="Name"
              readonly
            ></v-text-field>
            <v-text-field
              v-model="location"
              label="Location"
              readonly
            ></v-text-field>
            <v-checkbox
              v-model="has_new_feet"
              label="Has new feet?"
              readonly
            ></v-checkbox>
            <v-checkbox
              v-model="has_new_mast_bearing"
              label="Has new mast bearing?"
              readonly
            ></v-checkbox>
            <v-text-field
              v-model="faceCameras"
              label="Face Cameras"
              :key="faceCameraKey"
              readonly
            ></v-text-field>
            <v-text-field
              v-model="licensePlateCameras"
              label="License Plate Cameras"
              :key="licensePlateCameraKey"
              readonly
            ></v-text-field>
            <v-text-field
              v-model="widescreenCameras"
              label="Widescreen Cameras"
              :key="widescreenCameraKey"
              readonly
            ></v-text-field>
            <div class="d-flex justify-center align-center" style="padding-top: 20px;">
              <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">Back</v-btn>
            </div>
          </v-form>
        </v-sheet>
      </v-row>
    </v-container>
    <v-container  class="table-container">
      <v-row>
        <div style="color: green; font-size: 18px;">
          Cameras
        </div>
      </v-row>
      <v-row>
        <v-data-table
          :headers="cameraHeaders"
          :items="cameraTable"
          :search="cameraSearch"
          item-value="name"
          class="elevation-1"
          :key="cameraKey"
          @dblclick:row="navigateToCameraDetails"
        >
          <!-- If you still want the default pagination controls alongside the search -->
          <template v-slot:footer.prepend>
            <v-text-field
              v-model="cameraSearch"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              bg-color="#f5f5f5"
              hide-details
              class="flex-grow-1 mr-4"
            ></v-text-field>
            <!-- Add a v-spacer if needed to align items correctly with default footer content -->
            <v-spacer></v-spacer>
            <v-btn color="primary" dark small class="ma-2" @click="createCamera">
              <v-icon left>mdi-plus</v-icon>
              Add
            </v-btn>
          </template>
          <!-- Use the specific slot name 'item.actions' -->
          <template v-slot:item.actions="{ item }">
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn icon v-bind="props">
                  <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item @click="removeCamera(item)">
                  <v-list-item-title>Remove</v-list-item-title>
                </v-list-item>
                <v-list-item @click="updateCamera(item)">
                  <v-list-item-title>Update</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
        </v-data-table>
      </v-row>
    </v-container>
    <v-container  class="table-container">
      <v-row>
        <div style="color: green; font-size: 18px;">
          Other Items
        </div>
      </v-row>
      <v-row>
        <v-data-table
          :headers="otherHeaders"
          :items="otherTable"
          :search="otherSearch"
          item-value="name"
          class="elevation-1"
          :key="otherKey"
          @dblclick:row="navigateToOtherItemsDetails"
        >
          <!-- If you still want the default pagination controls alongside the search -->
          <template v-slot:footer.prepend>
            <v-text-field
              v-model="otherSearch"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              bg-color="#f5f5f5"
              hide-details
              class="flex-grow-1 mr-4"
            ></v-text-field>
            <!-- Add a v-spacer if needed to align items correctly with default footer content -->
            <v-spacer></v-spacer>
            <v-btn color="primary" dark small class="ma-2" @click="createOtherItem">
              <v-icon left>mdi-plus</v-icon>
              Add
            </v-btn>
          </template>
          <!-- Use the specific slot name 'item.actions' -->
          <template v-slot:item.actions="{ item }">
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn icon v-bind="props">
                  <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item @click="removeOtherItem(item)">
                  <v-list-item-title>Remove</v-list-item-title>
                </v-list-item>
                <v-list-item @click="updateOtherItem(item)">
                  <v-list-item-title>Update</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
        </v-data-table>
      </v-row>
    </v-container>
    <v-container  class="table-container">
      <v-row>
        <div style="color: green; font-size: 18px;">
          Notes
        </div>
      </v-row>
      <v-row>
        <v-data-table
          :headers="headers"
          :items="notesTable"
          :search="notesSearch"
          item-value="date"
          class="elevation-1"
          :key="notesKey"
        >
          <!-- If you still want the default pagination controls alongside the search -->
          <template v-slot:footer.prepend>
            <v-text-field
              v-model="notesSearch"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              bg-color="#f5f5f5"
              hide-details
              class="flex-grow-1 mr-4"
            ></v-text-field>
            <!-- Add a v-spacer if needed to align items correctly with default footer content -->
            <v-spacer></v-spacer>
            <v-btn color="primary" dark small class="ma-2" @click="addNote">
              <v-icon left>mdi-plus</v-icon>
              Add
            </v-btn>
          </template>
          <!-- Use the specific slot name 'item.actions' -->
          <template v-slot:item.actions="{ item }">
            <td class="text-right">
              <v-menu>
                <template v-slot:activator="{ props }">
                  <v-btn icon v-bind="props">
                    <v-icon>mdi-dots-vertical</v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item @click="deleteNote(item)">
                    <v-list-item-title>Delete</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </td>
          </template>
          <template v-slot:item.description="{ item }">
            <div class="pre-wrap-cell">
              {{ item.description }}
            </div>
          </template>
        </v-data-table>
      </v-row>
    </v-container>
    <v-container  class="table-container">
      <v-row>
        <div style="color: green; font-size: 18px;">
          Maintenance Tasks
        </div>
      </v-row>
      <v-row>
        <v-data-table
          :headers="maintHeaders"
          :items="maintTable"
          :search="maintSearch"
          item-value="description"
          class="elevation-1"
          :key="maintKey"
        >
          <!-- If you still want the default pagination controls alongside the search -->
          <template v-slot:footer.prepend>
            <v-text-field
              v-model="maintSearch"
              label="Search"
              prepend-inner-icon="mdi-magnify"
              density="compact"
              variant="outlined"
              bg-color="#f5f5f5"
              hide-details
              class="flex-grow-1 mr-4"
            ></v-text-field>
            <!-- Add a v-spacer if needed to align items correctly with default footer content -->
            <v-spacer></v-spacer>
            <v-btn color="primary" dark small class="ma-2" @click="addMaintenanceTask">
              <v-icon left>mdi-plus</v-icon>
              Add
            </v-btn>
          </template>
          <!-- Use the specific slot name 'item.actions' -->
          <template v-slot:item.actions="{ item }">
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn icon v-bind="props">
                  <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item @click="deleteMaintenanceTask(item)">
                  <v-list-item-title>Delete</v-list-item-title>
                </v-list-item>
                <v-list-item @click="updateMaintenanceTask(item)">
                  <v-list-item-title>Update</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
        </v-data-table>
      </v-row>
    </v-container>
    <ConfirmDialog ref="confirmDialog"></ConfirmDialog>
    <ErrorDialog ref="errorDialog"></ErrorDialog>
  </div>
</template>

<script setup>
  // Imports
  import { ref, onMounted, defineProps, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api from "../api";
  import ErrorDialog from './ErrorDialog.vue';
  import ConfirmDialog from './ConfirmDialog.vue';

  // Data
  const loading = ref(true);
  const id = ref(null);
  const name = ref(null);
  const location = ref(null);
  const has_new_feet = ref(false);
  const has_new_mast_bearing = ref(false);
  const faceCameras = ref([]);
  const licensePlateCameras = ref([]);
  const widescreenCameras = ref([]);
  const router = useRouter();
  const route = useRoute()
  const notesTable = ref([]);
  const maintTable = ref([]);
  const cameraTable = ref([]);
  const otherTable = ref([]);
  const maintSearch = ref('')
  const cameraSearch = ref('')
  const otherSearch = ref('')
  const notesSearch = ref('')
  const confirmDialog = ref(null);
  const errorDialog = ref(null);
  const notesKey = ref(0);
  const maintKey = ref(0);
  const otherKey = ref(0);
  const cameraKey = ref(0);
  const faceCameraKey = ref(0);
  const licensePlateCameraKey = ref(0);
  const widescreenCameraKey = ref(0);

  // Table headers
  const headers = ref([
    {title: 'Date', align: 'start', value: 'date', sortable: true, value: 'date', class: 'blue lighten-5'},
    {title: 'Description', value: 'description' ,  sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  const maintHeaders = ref([
    {title: 'Description', align: 'start', value: 'description', sortable: true, value: 'description', class: 'blue lighten-5'},
    {title: 'Last Done', value: 'last_done_date' , sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  const cameraHeaders = ref([
    {title: 'Name', align: 'start', value: 'name', sortable: true, value: 'name', class: 'blue lighten-5'},
    {title: 'Type', value: 'type' , sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  const otherHeaders = ref([
    {title: 'Name', align: 'start', value: 'name', sortable: true, value: 'name', class: 'blue lighten-5'},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  // Properties that are passed into the component
  const props = defineProps({
    id: {
      type: Number,
      default: 0,
    },
    name: {
      type: String,
      default: "",
    },
    location: {
      type: String,
      default: "",
    },
    has_new_feet: {
      type: Boolean,
      default: false,
    },
    has_new_mast_bearing: {
      type: Boolean,
      default: false,
    }
  });

  // Reset data on path change
  watch(
    // fetch the user information when params change
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN BaseUnit.watch.refresh newFullPath=" + newFullPath + "; oldFullPath=" + oldFullPath);
      fetchCameras();
      cameraKey.value += 1;
      fetchNotes();
      notesKey.value += 1;
      fetchMaintTasks();
      maintKey.value += 1;
      fetchOther();
      otherKey.value += 1;
      console.log("OUT BaseUnit.watch.refresh");
    }
  )

  // Initialize data on component mount
  onMounted(async () => {
    console.log('IN onMounted');
    id.value = props.id;
    name.value = props.name;
    location.value = props.location;
    has_new_feet.value = (props.has_new_feet === 'true');
    has_new_mast_bearing.value = (props.has_new_mast_bearing === 'true');
    faceCameras.value = route.query.face_cameras;
    licensePlateCameras.value = route.query.license_plate_cameras;
    widescreenCameras.value = route.query.widescreen_cameras;
    fetchCameras();
    cameraKey.value += 1;
    fetchNotes();
    notesKey.value += 1;
    fetchMaintTasks();
    maintKey.value += 1;
    fetchOther();
    otherKey.value += 1;
    console.log('OUT onMounted id=' + id.value + '; location=' + location.value + '; has_new_feet=' + has_new_feet.value + '; has_new_mast_bearing=' + has_new_mast_bearing.value + '; faceCameras=' + faceCameras.value);
  });

  // Handle double-click on a camera row
  const navigateToCameraDetails = (event, { item }) => {
    // Prevent the default browser double-click behavior (e.g., text selection)
    console.log("IN navigateToCameraDetails: " + JSON.stringify(item));
    
    event.preventDefault();
    let camera_location = -1;
    if ('location' in item && item.location != null) {
      camera_location = item.location;
    }
    let camera_bu = "NONE";
    if ('base_unit' in item && item.base_unit != null) {
      camera_bu = item.base_unit;
    }
    router.push({name: 'camera', params: {id: item.id, name: item.name, location: camera_location, base_unit: camera_bu, camera_type: item.type}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT navigateToCameraDetails");
  }

  // Handle a double-click on an other items row.
  const navigateToOtherItemsDetails = (event, { item }) => {
    // Prevent the default browser double-click behavior (e.g., text selection)
    console.log("IN navigateToOtherItemsDetails: " + JSON.stringify(item));

    event.preventDefault();
    let other_location = -1;
    if ('location' in item && item.location != null) {
      other_location = item.location;
    }
    let other_bu = "NONE";
    if ('base_unit' in item && item.base_unit != null) {
      other_bu = item.base_unit;
    }
    router.push({name: 'other-items', params: {id: item.id, name: item.name, location: other_location, base_unit: other_bu}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT navigateToOtherItemsDetails");
  }

  // Go back to previous page
  const goBack = () => {
    console.log("IN goBack");
    router.back();
    console.log("OUT goBack");
  };

  // Create a camera 
  const createCamera = () => {
    console.log("IN createCamera");
    router.push({name: 'add-camera', params: {base_unit_name: name.value, base_unit_id: id.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT createCamera");
  };

  // Remove a camera from the base unit
  const removeCamera = async (item) => {
    console.log("IN removeCamera item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Removal',
      'Are you sure you want to remove the camera ' + item.name + ' from the base unit?',
      { color: 'red lighten-3' }
    );

    if (result) {
      const config = {
        headers: {
            'Content-Type': 'application/json'
        }
      };
      const requestBody = {
        id: item.id,
        name: item.name,
        type: item.type,
        base_unit: item.base_unit
      };
      try {
          const response = await api.post('/remove-camera', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          const result = await errorDialog.value.open(
            'Confirm Error',
            'Error removing camera:' + e,
            { color: 'red lighten-3' }
          );
      }
      fetchCameras();
      console.log('Camera removed!');
      // Perform deletion logic here
    } else {
      console.log('Removal cancelled.');
    }
    console.log("OUT removeCamera");
  };

  // Update a camera 
  const updateCamera = (item) => {
    console.log("IN updateCamera");
    router.push({name: 'update-camera', params: {name: item.name}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT updateCamera");
  };

  // Create an other item
  const createOtherItem = () => {
    console.log("IN createOtherItem");
    router.push({name: 'add-other-item', params: {base_unit_name: name.value, base_unit_id: id.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT createOtherItem");
  };

  // Removce an other item
  const removeOtherItem = async (item) => {
    console.log("IN removeOtherItem item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Removal',
      'Are you sure you want to remove this other item from base unit?',
      { color: 'red lighten-3' }
    );

    if (result) {
      const config = {
        headers: {
            'Content-Type': 'application/json'
        }
      };
      const requestBody = {
        id: item.id,
      };
      try {
          const response = await api.post('/remove-other-item', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          const result = await errorDialog.value.open(
            'Confirm Error',
            'Error deleting other-item:' + e,
            { color: 'red lighten-3' }
          );
      }
      fetchOther();
      console.log('Other Item deleted!');
      // Perform deletion logic here
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT removeOtherItem");
  };
  
  // Update an other item
  const updateOtherItem = (item) => {
    console.log("IN updateOtherItem");
    router.push({name: 'update-other-item', params: {name: item.name}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT updateOtherItem");
  };

  // Add a mintenance task to database
  const addMaintenanceTask = () => {
    console.log("IN addMaintenanceTask");
    router.push({name: 'add-maintenance-task', params: {item_type: 'BASE_UNIT', item_ref: id.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT addMaintenanceTask");
  }

  // Update a maintenance task
  const updateMaintenanceTask = (item) => {
    console.log("IN updateMaintenanceTask. item=" + JSON.stringify(item));
    router.push({name: 'update-maintenance-task', params: {id: item.id, description: item.description, last_done_date: item.last_done_date}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT updateMaintenanceTask");
  };

  // Delete a maintenace task from database
  const deleteMaintenanceTask = async (item) => {
    console.log("IN deleteMaintenanceTask item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Deletion',
      'Are you sure you want to delete this task?',
      { color: 'red lighten-3' }
    );

    if (result) {
      const config = {
        headers: {
            'Content-Type': 'application/json'
        }
      };
      const requestBody = {
        id: item.id,
      };
      try {
          const response = await api.post('/delete-maintenance-task', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          const result = await errorDialog.value.open(
            'Confirm Error',
            'Error deleting maintenance task:' + e,
            { color: 'red lighten-3' }
          );
      }
      fetchMaintTasks();
      console.log('Maintenance Task deleted!');
      // Perform deletion logic here
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT deleteMaintenanceTask");
  };

  // Add a note to the database
  const addNote = () => {
    console.log("IN addNote");
    router.push({name: 'add-note', params: {item_type: 'BASE_UNIT', item_ref: id.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT addNote");
  }

  // Delete a note from the database
  const deleteNote = async (item) => {
    console.log("IN deleteNote item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Deletion',
      'Are you sure you want to delete this note?',
      { color: 'red lighten-3' }
    );

    if (result) {
      const config = {
        headers: {
            'Content-Type': 'application/json'
        }
      };
      const requestBody = {
        id: item.id,
      };
      try {
          const response = await api.post('/delete-note', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          const result = await errorDialog.value.open(
            'Confirm Error',
            'Error deleting note:' + e,
            { color: 'red lighten-3' }
          );
      }
      console.log('Note deleted!');
      fetchNotes();
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT deleteNote");
  };

  // Fetch the notes associated with the base unit from the database.
  const fetchNotes = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      item_type: 'BASE_UNIT',
      item_ref: id.value,
    };
    try {
        const response = await api.post('/get-notes', requestBody, config);
        notesTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        const result = await errorDialog.value.open(
            'Confirm Error',
            'Error fetching notes:' + e,
            { color: 'red lighten-3' }
          );
    }
  };

  // Fetch all maintenance tasks associated with the base unit.
  const fetchMaintTasks = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      item_type: 'BASE_UNIT',
      item_ref: id.value,
    };
    try {
        const response = await api.post('/get-maint-tasks', requestBody, config);
        maintTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        const result = await errorDialog.value.open(
            'Confirm Error',
            'Error fetching maint tasks:' + e,
            { color: 'red lighten-3' }
          );
    }
  };

  // Fetch all cameras associated with the base unit.
  const fetchCameras = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      base_unit_ref: id.value,
    };
    try {
        const response = await api.post('/get-cameras-for-bu', requestBody, config);
        cameraTable.value = response.data;

        console.log("cameraTable=" + JSON.stringify(cameraTable.value));
        faceCameras.value = [];
        licensePlateCameras.value = [];
        widescreenCameras.value = [];
        for (const camera of cameraTable.value) {
          if(camera.type === "Face Camera"){
            faceCameras.value.push(camera.name);
          } else if(camera.type === "License Plate Camera") {
            licensePlateCameras.value.push(camera.name);
          } else if(camera.type === "Wide Screen Camera") {
            widescreenCameras.value.push(camera.name); 
          }
        }
        faceCameraKey.value += 1;
        licensePlateCameraKey.value += 1;
        widescreenCameraKey.value += 1;

        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        const result = await errorDialog.value.open(
            'Confirm Error',
            'Error fetching cameras:' + e,
            { color: 'red lighten-3' }
          );
    }
  };

  // Fetch all other items associated with the base unit.
  const fetchOther = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      base_unit_ref: id.value,
    };
    try {
        const response = await api.post('/get-other-items-for-bu', requestBody, config);
        otherTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        const result = await errorDialog.value.open(
            'Confirm Error',
            'Error fetching other-items:' + e,
            { color: 'red lighten-3' }
          );
    }
  };
</script>

<style>
  .v-data-table {
    border: 1px solid green;
  }

  /* Set header background color */
  .theme--light.v-data-table > .v-data-table__wrapper > table > thead > tr > th {
    background: var(--v-primary-base); /* Use a CSS variable for theme color */
  }

  /* Set alternating row colors (striped table) */
  .v-table tbody tr:nth-child(odd) {
    background-color: #f5f5f5; /* Light grey for odd rows */
  }
  .v-table thead th {
    background-color:  #F5F5DC; /* White for even rows */
  }
  .v-table tbody tr:nth-child(even) {
    background-color: #ffffff; /* White for even rows */
  }
</style>
<style scoped>
  .my-button {
    cursor: pointer;
    padding: 8px 20px;
    border: 1px solid transparent;
    border-radius: 6px; /* */
    font-weight: 700;
  }

  .detail-container {
    border: 1px solid green;
    width: 70%;
  }

  .detail-sheet { 
    width: 95%;
  }

  .table-container { 
    width: 80%;
  }

  .outer-div {
    width: 80%;
    padding-top: 30px;
  }

  .pre-wrap-cell {
    white-space: pre-wrap; /* or pre-line */
  }

   /* Specific styles for screens smaller than 600px */
  @media (max-width: 600px) {
    .detail-container {
      border: 1px solid green;
      width: 100%; /* Take up full width on mobile */
      padding: 0 1em; /* Add some padding */
    }
    .detail-sheet { 
      width: 99%
    }
    .table-container { 
      width: 100%
    }
    .outer-div {
      width: 100%;
    }
  }
</style>