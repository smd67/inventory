<!--
This file is the vue component implementation for the issue report.
 -->
<template>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div class="outer-div">
    <v-container  class="table-container">
      <v-row>
        <div style="color: green; font-size: 24px;">
          <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
          Issue Report
        </div>
      </v-row>
      <v-row style="border: 1px solid green;">
        <!-- Data Table -->
        <v-data-table
          :headers="headers"
          :items="issueReportTable"
          :search="issueReportSearch"
          item-value="name"
          class="elevation-1"
          :key="issueReportKey"
          @dblclick:row="navigateToDetails"
        >
        </v-data-table>
      </v-row>
      <v-row>
        <v-spacer></v-spacer>
        <div class="d-flex justify-center align-center" style="padding-top: 20px; gap: 16px;">
          <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="goBack">
            Back
          </v-btn>
          <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important;" @click="exportToCSV">
            Export to CSV
          </v-btn>
        </div>
        <v-spacer></v-spacer>
      </v-row>
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
  const issueReportSearch = ref('');
  const issueReportTable = ref([]);
  const issueReportKey = ref(0);
  const itemType = ref(null);
  const queryString = ref(null);
  const startDate = ref(null);
  const endDate = ref(null);

  // Table headers
  const headers = ref([
    {title: 'Name', align: 'start', sortable: true, value: 'item_name', class: 'blue lighten-5'},
    {title: 'Type', value: 'item_type', sortable: true },
    {title: 'Match String', value: 'match_string' , sortable: true},
    {title: 'Similarity Score', value: 'sim_score', sortable: true}
  ]);
  
  // Properties passed in to component
  const props = defineProps({
    item_type: {
      type: String,
      default: "",
    },
    query_string: {
      type: String,
      default: "",
    },
    start_date: {
      type: Date,
      default: null
    },
    end_date: {
      type: Date,
      default: null
    },
  });

  // fetch the user information when params change
  watch(
    () => route.params.id,
    async refresh => {
      console.log("IN IssueReport.watch.refresh");
      itemType.value = props.item_type;
      queryString.value = props.query_string;
      startDate.value = props.start_date;
      endDate.value = props.end_date;
      await fetchIssueReport();
      issueReportKey.value += 1;
      console.log("OUT IssueReport.watch.refresh");
    }
  );

  // Initialize data when component is mounted
  onMounted(async () => {
    console.log('IN IssueReport.onMounted');
    itemType.value = props.item_type;
    queryString.value = props.query_string;
    startDate.value = props.start_date;
    endDate.value = props.end_date;
    await fetchIssueReport();
    console.log('OUT IssueReport.onMounted');
  });

  // Go back to previous page
  const goBack = () => {
    console.log("IN IssueReport.goBack");
    router.back();
    console.log("OUT IssueReport.goBack");
  };

  // Export the generated table to a csv file and download it
  const exportToCSV = () => {
    // 1. Get your data source
    const jsonData = baseUnitsTable.value;

    // 2. Convert the JSON data to CSV format using PapaParse
    const csv = Papa.unparse(jsonData);

    // 3. Create a Blob and initiate the download
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');

    link.setAttribute('href', url);
    link.setAttribute('download', 'new_feet_report.csv'); // Set the download file name
    link.click();
  };

  // Navigate to the base units detail page on double-click.
  const navigateToDetails = (event, { item }) => {
    // Prevent the default browser double-click behavior (e.g., text selection)
    console.log("IN navigateToDetails: " + JSON.stringify(item));

    event.preventDefault();

    let face_cameras = [];
    if ('face_cameras' in item && item.face_cameras != null) {
      face_cameras = item.face_cameras;
    }
    let license_plate_cameras = [];
    if ('license_plate_cameras' in item && item.license_plate_cameras != null) {
      license_plate_cameras = item.license_plate_cameras;
    }
    let widescreen_cameras = "NONE";
    if ('widescreen_cameras' in item && item.widescreen_cameras != null) {
      widescreen_cameras = item.widescreen_cameras;
    }

    router.push(
      {
        name: 'base-unit',
        query: { face_cameras: faceCameras.value, license_plate_cameras: licensePlateCameras.value, widescreen_cameras: widescreenCameras.value },
        params: {id: item.id, name: item.name, location: item.location, has_new_mast_bearing: item.has_new_mast_bearing, has_new_feet: item.has_new_feet}
      });
    console.log("OUT navigateToDetails");
  };

  // Retrieve base units from database with a REST call.
  const fetchIssueReport = async () => {
    console.log("IN IssueReport.fetchIssueReport");
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    const requestBody = {
      item_type: itemType.value,
      query_string: queryString.value,
      start_date: startDate.value,
      end_date: endDate.value
    };
    try {
        const response = await api.post('/get-issue-report', requestBody, config);
        issueReportTable.value = response.data;
        loading.value = false;
    } catch (e) {
        loading.value = false;
        const result = await errorDialog.value.open(
            'Confirm Error',
            'Error fetching data:' + e,
            { color: 'red lighten-3' }
          );
    }
    console.log("OUT IssueReport.fetchIssueReport");
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
    width: 100%;
    padding-top: 30px;
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