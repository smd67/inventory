<!--
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
          History Report for {{ item_name }}
        </div>
      </v-row>
      <v-row style="border: 1px solid green;">
        <!-- Data Table -->
        <v-data-table
          :headers="headers"
          :items="logItemsTable"
          :search="logItemsSearch"
          item-value="name"
          class="elevation-1"
          :key="logItemsKey"
          :items-per-page="20"
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

  // Properties passed into component.
  const props = defineProps({
    item_type: {
      type: String,
      default: null,
    },
    item_name: {
      type: String,
      default: null,
    },
  });

  // Data
  const errorDialog = ref(null);
  const loading = ref(true);
  const router = useRouter();
  const route = useRoute();
  const logItemsSearch = ref('');
  const logItemsTable = ref([]);
  const logItemsKey = ref(0);
  const itemType = ref(null);
  const itemName = ref(null);

  // Table headers
  const headers = ref([
    {title: 'Date', align: 'start', value: 'date', sortable: true, value: 'date', class: 'blue lighten-5'},
    {title: 'Description', value: 'description' , sortable: true},
    {title: 'Technician Name', value: 'technician_name' , sortable: true},
  ]);
  
  // fetch the user information when params change
  watch(
    () => route.params.item_name,
    async refresh => {
      console.log("IN HistoryReport.watch.refresh");
      logItemsKey.value += 1;
      itemType.value = props.item_type;
      itemName.value = props.item_name;
      fetchActivityLog();
      console.log("OUT HistoryReport.watch.refresh");
    }
  );

  // Initialize data on component mount
  onMounted(async () => {
    console.log('IN HistoryReport.onMounted');
    logItemsKey.value += 1;
    itemType.value = props.item_type;
    itemName.value = props.item_name;
    fetchActivityLog();
    console.log('OUT HistoryReport.onMounted');
  });

  // Go back to previous page
  const goBack = () => {
    console.log("IN HistoryReport.goBack");
    router.back();
    console.log("OUT HistoryReport.goBack");
  };

  // Export the generated table to a csv 
  const exportToCSV = () => {
    // 1. Get your data source
    const jsonData = logItemsTable.value;

    // 2. Convert the JSON data to CSV format using PapaParse
    const csv = Papa.unparse(jsonData);

    // 3. Create a Blob and initiate the download
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');

    link.setAttribute('href', url);
    link.setAttribute('download', 'history_report.csv'); // Set the download file name
    link.click();
  };

  // Handles retrieving the maintenance items from the database using a REST 
  // call.
  const fetchActivityLog = async () => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
     const requestBody = {
        item_type: itemType.value,
        item_name: itemName.value,
    };
    console.log("requestBody=" + JSON.stringify(requestBody));

    try {
        const response = await api.post('/get-activity-log', requestBody, config);
        logItemsTable.value = response.data;
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