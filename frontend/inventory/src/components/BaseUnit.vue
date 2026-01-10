<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 225px;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Base Unit Details
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div v-if="!error" style="padding-right: 250px;">
    <v-container style="border: 1px solid green" width="700">
      <v-sheet class="pa-4 text-right" width="600">
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
            v-model="face_camera"
            label="Face Camera"
            readonly
          ></v-text-field>
          <v-text-field
            v-model="license_plate_camera"
            label="License Plate Camera"
            readonly
          ></v-text-field>
           <v-text-field
            v-model="widescreen_camera"
            label="Widescreen Camera"
            readonly
          ></v-text-field>
          <div class="d-flex justify-center align-center" style="padding-top: 20px;">
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">Back</v-btn>
          </div>
        </v-form>
      </v-sheet>
    </v-container>
    <v-container  width="800">
      <div style="color: green; font-size: 18px; padding-top: 10px">
        Cameras
      </div>
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
              <v-list-item @click="deleteCamera(item)">
                <v-list-item-title>Delete</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-data-table>
    </v-container>
    <v-container  width="800">
      <div style="color: green; font-size: 18px; padding-top: 10px">
        Other Items
      </div>
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
              <v-list-item @click="deleteOtherItem(item)">
                <v-list-item-title>Delete</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-data-table>
    </v-container>
    <v-container  width="800">
      <div style="color: green; font-size: 18px; padding-top: 10px">
        Notes
      </div>
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
        </template>
      </v-data-table>
    </v-container>
    <v-container  width="800">
      <div style="color: green; font-size: 18px; padding-top: 10px">
        Maintenance Tasks
      </div>
      <v-data-table
        :headers="maintHeaders"
        :items="maintTable"
        :search="maintSearch"
        item-value="status"
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
            </v-list>
          </v-menu>
        </template>
      </v-data-table>
    </v-container>
    <ConfirmDialog ref="confirmDialog"></ConfirmDialog>
  </div>
  
  <div v-else class="error-banner" style="color: red;">
    {{ error }}
  </div>
</template>

<script setup>
  import { ref, onMounted, defineProps, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api from "../api";
  import ConfirmDialog from './ConfirmDialog.vue';

  const error = ref(null);
  const loading = ref(true);
  const id = ref(null);
  const name = ref(null);
  const location = ref(null);
  const has_new_feet = ref(false);
  const has_new_mast_bearing = ref(false);
  const face_camera = ref(null);
  const license_plate_camera = ref(null);
  const widescreen_camera = ref(null);
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
  const notesKey = ref(0);
  const maintKey = ref(0);
  const otherKey = ref(0);
  const cameraKey = ref(0);

  const headers = ref([
    {title: 'Date', align: 'start', value: 'date', sortable: true, value: 'date', class: 'blue lighten-5'},
    {title: 'Description', value: 'description' , sortable: true},
    // ... other headers
    { text: 'Actions', value: 'actions', sortable: false }, // New actions column
  ]);

  const maintHeaders = ref([
    {title: 'Description', align: 'start', value: 'description', sortable: true, value: 'description', class: 'blue lighten-5'},
    {title: 'Status', value: 'status' , sortable: true},
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
    },
    face_camera: {
      type: String,
      default: "",
    },
    license_plate_camera : {
      type: String,
      default: "",
    },
    widescreen_camera : {
      type: String,
      default: "",
    },
  });

  // fetch the user information when params change
  watch(
    () => route.params.id,
    async refresh => {
      console.log("IN BaseUnit.watch.refresh");
      fetchCameras();
      cameraKey.value += 1;
      fetchNotes();
      notesKey.value += 1;
      fetchMaintTasks();
      maintKey.value += 1;
      fetchOther();
      otherKey.value += 1;
      console.log("cameraTable=" + JSON.stringify(cameraTable.value));
      for (const camera of cameraTable.value) {
        if(camera.type === "Face Camera"){
          face_camera.value = camera.name;
        } else if(camera.type === "License Plate Camera") {
          license_plate_camera.value = camera.name;
        } else if(camera.type === "Widescreen Camera") {
          widescreen_camera.value = camera.name;
        }
      }
      console.log("OUT BaseUnit.watch.refresh");
    }
  )
  onMounted(async () => {
    console.log('IN onMounted');
    id.value = props.id;
    name.value = props.name;
    location.value = props.location;
    has_new_feet.value = (props.has_new_feet === 'true');
    has_new_mast_bearing.value = (props.has_new_mast_bearing === 'true');
    face_camera.value = props.face_camera;
    license_plate_camera.value = props.license_plate_camera;
    widescreen_camera.value = props.widescreen_camera;
    fetchCameras();
    cameraKey.value += 1;
    fetchNotes();
    notesKey.value += 1;
    fetchMaintTasks();
    maintKey.value += 1;
    fetchOther();
    otherKey.value += 1;
    console.log('OUT onMounted id=' + id.value + '; location=' + location.value + '; has_new_feet=' + has_new_feet.value + '; has_new_mast_bearing=' + has_new_mast_bearing.value + '; face_camera=' + face_camera.value);
  });

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

  const goBack = () => {
    console.log("IN goBack");
    router.push({name: 'prototype'}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT goBack");
  };

  const createCamera = () => {
    console.log("IN createCamera");
    router.push({name: 'create-camera', params: {base_unit: name.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT createCamera");
  };

  const deleteCamera = async (item) => {
    console.log("IN deleteCamera item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Deletion',
      'Are you sure you want to delete this camera?',
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
          const response = await api.post('/delete-camera/', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          error.value = 'Error fetching data:' + e;
      }
      fetchCameras();
      console.log('Camera deleted!');
      // Perform deletion logic here
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT deleteCamera");
  };
  const createOtherItem = () => {
    console.log("IN createOtherItem");
    router.push({name: 'create-other-item', params: {base_unit: name.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT createOtherItem");
  };

  const deleteOtherItem = async (item) => {
    console.log("IN deleteOtherItem item=" + JSON.stringify(item));
    // Call the dialog's open function using the template ref
    const result = await confirmDialog.value.open(
      'Confirm Deletion',
      'Are you sure you want to delete this other item?',
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
          const response = await api.post('/delete-other-item/', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          error.value = 'Error fetching data:' + e;
      }
      fetchOther();
      console.log('Other Item deleted!');
      // Perform deletion logic here
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT deleteOtherItem");
  };

  const addMaintenanceTask = () => {
    console.log("IN addMaintenanceTask");
    router.push({name: 'add-maintenance-task', params: {item_type: 'BASE_UNIT', item_ref: id.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT addMaintenanceTask");
  }

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
          const response = await api.post('/delete-maintenance-task/', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          error.value = 'Error fetching data:' + e;
      }
      fetchMaintTasks();
      console.log('Maintenance Task deleted!');
      // Perform deletion logic here
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT deleteMaintenanceTask");
  };

  const addNote = () => {
    console.log("IN addNote");
    router.push({name: 'add-note', params: {item_type: 'BASE_UNIT', item_ref: id.value}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT addNote");
  }

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
          const response = await api.post('/delete-note/', requestBody, config);
          loading.value = false;
      } catch (e) {
          loading.value = false;
          console.log("error=" + e)
          error.value = 'Error fetching data:' + e;
      }
      console.log('Note deleted!');
      fetchNotes();
    } else {
      console.log('Deletion cancelled.');
    }
    console.log("OUT deleteNote");
  };

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
        const response = await api.post('/get-notes/', requestBody, config);
        notesTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        error.value = 'Error fetching data:' + e;
    }
  };

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
        const response = await api.post('/get-maint-tasks/', requestBody, config);
        maintTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        error.value = 'Error fetching data:' + e;
    }
  };

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
        const response = await api.post('/get-cameras-for-bu/', requestBody, config);
        cameraTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        error.value = 'Error fetching data:' + e;
    }
  };

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
        const response = await api.post('/get-other-items-for-bu/', requestBody, config);
        otherTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        error.value = 'Error fetching data:' + e;
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
  .my-button {
    cursor: pointer;
    padding: 8px 20px;
    border: 1px solid transparent;
    border-radius: 6px; /* */
    font-weight: 700;
  }
</style>