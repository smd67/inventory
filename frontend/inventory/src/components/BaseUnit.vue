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
    <v-container  width="750">
      <div style="color: green; font-size: 18px; padding-top: 10px">
        Cameras
      </div>
      <v-data-table
        :headers="cameraHeaders"
        :items="cameraTable"
        :search="cameraSearch"
        item-value="name"
        class="elevation-1"
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
        </template>
      </v-data-table>
    </v-container>
    <v-container  width="750">
      <div style="color: green; font-size: 18px; padding-top: 10px">
        Other Items
      </div>
      <v-data-table
        :headers="otherHeaders"
        :items="otherTable"
        :search="otherSearch"
        item-value="name"
        class="elevation-1"
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
        </template>
      </v-data-table>
    </v-container>
    <v-container  width="750">
      <div style="color: green; font-size: 18px; padding-top: 10px">
        Notes
      </div>
      <v-data-table
        :headers="headers"
        :items="notesTable"
        :search="notesSearch"
        item-value="date"
        class="elevation-1"
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
        </template>
      </v-data-table>
    </v-container>
    <v-container  width="750">
      <div style="color: green; font-size: 18px; padding-top: 10px">
        Maintenance Tasks
      </div>
      <v-data-table
        :headers="maintHeaders"
        :items="maintTable"
        :search="maintSearch"
        item-value="status"
        class="elevation-1"
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
        </template>
      </v-data-table>
    </v-container>
  </div>
  
  <div v-else class="error-banner" style="color: red;">
    {{ error }}
  </div>
</template>

<script setup>
  import { ref, onMounted, defineProps } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';

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
  const notesTable = ref([]);
  const maintTable = ref([]);
  const cameraTable = ref([]);
  const otherTable = ref([]);
  const maintSearch = ref('')
  const cameraSearch = ref('')
  const otherSearch = ref('')
  const notesSearch = ref('')

  const headers = ref([
    {title: 'Date', align: 'start', value: 'date', sortable: true, value: 'date', class: 'blue lighten-5'},
    {title: 'Description', value: 'description' , sortable: true}
  ]);

  const maintHeaders = ref([
    {title: 'Description', align: 'start', value: 'description', sortable: true, value: 'description', class: 'blue lighten-5'},
    {title: 'Status', value: 'status' , sortable: true},
    {title: 'Last Done', value: 'last_done_date' , sortable: true},
  ]);

  const cameraHeaders = ref([
    {title: 'Name', align: 'start', value: 'name', sortable: true, value: 'name', class: 'blue lighten-5'},
    {title: 'Type', value: 'type' , sortable: true}
  ]);

  const otherHeaders = ref([
    {title: 'Name', align: 'start', value: 'name', sortable: true, value: 'name', class: 'blue lighten-5'},
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
    fetchNotes();
    fetchMaintTasks();
    fetchOther();
    console.log('OUT onMounted id=' + id.value + '; location=' + location.value + '; has_new_feet=' + has_new_feet.value + '; has_new_mast_bearing=' + has_new_mast_bearing.value + '; face_camera=' + face_camera.value);
  });

  const navigateToCameraDetails = (event, { item }) => {
    // Prevent the default browser double-click behavior (e.g., text selection)
    console.log("IN navigateToCameraDetails: " + JSON.stringify(item));

    event.preventDefault();
    router.push({name: 'camera', params: {id: item.id, name: item.name, location: item.location, base_unit: item.base_unit, camera_type: item.type}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT navigateToCameraDetails");
  }

  const navigateToOtherItemsDetails = (event, { item }) => {
    // Prevent the default browser double-click behavior (e.g., text selection)
    console.log("IN navigateToOtherItemsDetails: " + JSON.stringify(item));

    event.preventDefault();
    router.push({name: 'other-items', params: {id: item.id, name: item.name, location: item.location, base_unit: item.base_unit}}).catch(failure => {
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

  const fetchNotes = async () => {
    const apiUrl = 'http://127.0.0.1:8001/get-notes/';
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
        const response = await axios.post(apiUrl, requestBody, config);
        notesTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        error.value = 'Error fetching data:' + e;
    }
  };

  const fetchMaintTasks = async () => {
    const apiUrl = 'http://127.0.0.1:8001/get-maint-tasks/';
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
        const response = await axios.post(apiUrl, requestBody, config);
        maintTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        error.value = 'Error fetching data:' + e;
    }
  };

  const fetchCameras = async () => {
    const apiUrl = 'http://127.0.0.1:8001/get-cameras-for-bu/';
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      base_unit_ref: id.value,
    };
    try {
        const response = await axios.post(apiUrl, requestBody, config);
        cameraTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        console.log("error=" + e)
        error.value = 'Error fetching data:' + e;
    }
  };

  const fetchOther = async () => {
    const apiUrl = 'http://127.0.0.1:8001/get-other-items-for-bu/';
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      base_unit_ref: id.value,
    };
    try {
        const response = await axios.post(apiUrl, requestBody, config);
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