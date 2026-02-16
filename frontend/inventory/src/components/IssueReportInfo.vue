<!--
This file is the vue component implementation of a screen to gather information
prior to performing an issue report.
 -->
<template>
  <div class="my-division">
      <div class="spinner" v-if="loading"></div>
  </div>
  <div class="outer-div">
    <v-container class="table-container">
      <v-row>
        <div style="color: green; font-size: 24px">
          <img width="75" height="75" alt="Asset Tracker" src="../assets/asset_tracker.jpg">
          Information for an Issue Report
        </div>
      </v-row>
      <v-row style="border: 1px solid green;">
        <v-sheet class="pa-4 text-right detail-sheet">
          <v-text-field
            v-model="queryString"
            label="Query"
          ></v-text-field>
          <v-select
            v-model="itemType"
            :items="itemTypes"
            label="Item Type"
          ></v-select>
          <v-date-input v-model="startDate" label="Start Date"></v-date-input>
          <v-date-input v-model="endDate" label="End Date"></v-date-input>

          <div class="d-flex justify-center align-center" style="padding-top: 20px; ; gap: 16px;">
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC !important; padding-right: 10px;" @click="goBack">Back</v-btn>
            <v-btn variant="outlined" color="green" style="background-color: #F5F5DC;"  @click="goNext">Next</v-btn>
          </div>
        </v-sheet>
      </v-row>
    </v-container>
    <ErrorDialog ref="errorDialog"></ErrorDialog>
  </div>
</template>

<script setup>
  // Imports
  import { ref, onMounted, watch } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import { VDateInput } from 'vuetify/labs/VDateInput'
  import api from "../api";
  import ErrorDialog from './ErrorDialog.vue';

  // Data
  const loading = ref(true);
  const queryString = ref(null);
  const startDate = ref(null);
  const endDate = ref(new Date().toISOString().slice(0, 10));
  const itemType = ref(null);
  const itemTypes = ref([]);
  const router = useRouter();
  const route = useRoute();
  const errorDialog = ref(null);
  
  // Watch method to reset cached data 
  watch(
    () => route.fullPath,
    async (newFullPath, oldFullPath) => {
      console.log("IN IssueReportInfo.watch.refresh. newFullPath=" + newFullPath + "; oldFullPath=" + oldFullPath);
      if(oldFullPath.includes("/prototype")){
        queryString.value = null;
        itemType.value = null;
        startDate.value = null;
        endDate.value = new Date().toISOString().slice(0, 10);
      }
      await fetchItemTypes();
      console.log('OUT IssueReportInfo.watch.refresh');
    }
  );

  // Initialize data on mount of component
  onMounted(async () => {
    console.log('IN IssueReportInfo.onMounted');
    queryString.value = null;
    itemType.value = null;
    startDate.value = null;
    endDate.value = new Date().toISOString().slice(0, 10);
    await fetchItemTypes();
    console.log("OUT IssueReportInfo.onMounted");
  });

  // Method to return to the previous page.
  const goBack = () => {
    console.log("IN IssueReportInfo.goBack");
    router.back()
    console.log("OUT IssueReportInfo.goBack");
  }

  const goNext = async () => {
    console.log("IN IssueReportInfo.goNext");
    router.push({
      name: "issue-report", 
      params: {item_type: itemType.value, query_string: queryString.value, start_date: startDate.value, end_date: endDate.value },
    });
    console.log("OUT IssueReportInfo.goNext");
  }

  // Retrieve item type values.
  const fetchItemTypes= async () => {
    const config = {
      headers: {
          'Content-Type': 'application/json'
      }
    };

    try {
      const response = await api.get('/get-item-types', config);
      itemTypes.value = response.data;
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
<style scoped>
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