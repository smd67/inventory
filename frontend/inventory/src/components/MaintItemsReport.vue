<!--
This file is the vue component implementation for a report that lists all 
maintenance tasks whose last due date is >= 6 months.
 -->
<template>
  <div style="color: green; font-size: 24px; padding-top: 30px; padding-left: 9.0%;">
    <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
    Has Expired Maintenace Tasks
  </div>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div class="outer-div">
    <v-container  class="table-container">
      <!-- Data Table -->
      <v-data-table
        :headers="headers"
        :items="maintItemsTable"
        :search="maintItemsSearch"
        item-value="name"
        class="elevation-1"
        :key="maintItemsKey"
      >
      </v-data-table>
    </v-container>
    <v-container>
      <div class="d-flex justify-center align-center" style="padding-top: 20px; gap: 16px;">
        <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">
          Back
        </v-btn>
        <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="exportToCSV">
          Export to CSV
        </v-btn>
      </div>
    </v-container>
    <ErrorDialog ref="errorDialog"></ErrorDialog>
  </div>
</template>

<script setup>
  // Imports
  import { ref, onMounted, defineProps, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api from "../api";
  import ErrorDialog from './ErrorDialog.vue';
  import Papa from 'papaparse'; // Import PapaParse

  // Data
  const errorDialog = ref(null);
  const loading = ref(true);
  const router = useRouter();
  const route = useRoute();
  const maintItemsSearch = ref('');
  const maintItemsTable = ref([]);
  const maintItemsKey = ref(0);

  // Table headers
  const headers = ref([
    {title: 'Description', align: 'start', value: 'description', sortable: true, value: 'description', class: 'blue lighten-5'},
    {title: 'Status', value: 'status' , sortable: true},
    {title: 'Last Done', value: 'last_done_date' , sortable: true},
    {title: 'Type', value: 'item_type' , sortable: true},
    {title: 'Name', value: 'item_name' , sortable: true},
  ]);
  
  // fetch the user information when params change
  watch(
    () => route.params.id,
    async refresh => {
      console.log("IN MastBearingReport.watch.refresh");
      fetchMaintItems();
      maintItemsKey.value += 1;
      console.log("OUT MastBearingReport.watch.refresh");
    }
  );

  // Initialize data on component mount
  onMounted(async () => {
    console.log('IN MastBearingReport.onMounted');
    fetchMaintItems();
    maintItemsKey.value += 1;
    console.log('OUT MastBearingReport.onMounted');
  });

  // Go back to previous page
  const goBack = () => {
    console.log("IN MastBearingReport.goBack");
    router.back();
    console.log("OUT MastBearingReport.goBack");
  };

  // Export the generated table to a csv 
  const exportToCSV = () => {
    // 1. Get your data source
    const jsonData = maintItemsTable.value;

    // 2. Convert the JSON data to CSV format using PapaParse
    const csv = Papa.unparse(jsonData);

    // 3. Create a Blob and initiate the download
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');

    link.setAttribute('href', url);
    link.setAttribute('download', 'expired_maint_tasks.csv'); // Set the download file name
    link.click();
  };

  // Navigate to base units detail on a double-click
  const navigateToDetails = (event, { item }) => {
    // Prevent the default browser double-click behavior (e.g., text selection)
    console.log("IN navigateToDetails: " + JSON.stringify(item));

    event.preventDefault();

    let face_camera = "NONE";
    if ('face_camera' in item && item.face_camera != null) {
      face_camera = item.face_camera;
    }
    let license_plate_camera = "NONE";
    if ('license_plate_camera' in item && item.license_plate_camera != null) {
      license_plate_camera = item.license_plate_camera;
    }
    let widescreen_camera = "NONE";
    if ('widescreen_camera' in item && item.widescreen_camera != null) {
      widescreen_camera = item.widescreen_camera;
    }

    router.push({name: 'base-unit', params: {id: item.id, name: item.name, location: item.location, has_new_mast_bearing: item.has_new_mast_bearing, has_new_feet: item.has_new_feet, face_camera: face_camera, license_plate_camera: license_plate_camera, widescreen_camera: widescreen_camera}}).catch(failure => {
      console.log('An unexpected navigation failure occurred:', failure);
    });
    console.log("OUT navigateToDetails");
  };

  // Handles retrieving the maintenance items from the database using a REST 
  // call.
  const fetchMaintItems = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await api.get('/get-expired-maintenance-tasks', config);
        maintItemsTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        const result = await errorDialog.value.open(
            'Confirm Error',
            'Error fetching data:' + e,
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
    padding-right: 25%;
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
      padding-right: 0%;
    }
  }
</style>